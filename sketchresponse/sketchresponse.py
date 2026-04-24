from __future__ import annotations

import base64
import inspect
import json
from collections.abc import Callable
from copy import deepcopy

from .types import (
    GraderResult,
    SketchAnswer,
    SketchConfig,
    SketchItem,
)

OkValue = bool | str | float
GraderReturn = GraderResult | tuple[OkValue] | tuple[OkValue, str]


class GradeableCollection(list[SketchItem]):
    """List of gradeable items for a single tool id, plus resolved config.

    Iterates over `SketchItem` dicts produced by that tool's plugin. The
    `params` attribute is the plugin-config fragment that matches the tool's
    id — useful for graders that need, e.g., the plugin's declared `xrange`.
    """

    identifier: str
    params: SketchConfig

    def __init__(
        self,
        identifier: str,
        config: SketchConfig,
        gradeable_list: list[SketchItem],
    ) -> None:
        super().__init__(gradeable_list)
        self.identifier = identifier
        self.params = self.resolve_params_for_id(identifier, config)

    @staticmethod
    def resolve_params_for_id(identifier: str, config: SketchConfig) -> SketchConfig:
        resolved: SketchConfig = config.copy()
        plugins = resolved.pop("plugins", [])  # Don't include plugins array

        for plugin_config in plugins:
            resolved.update(GradeableCollection.resolve_params_for_id(identifier, plugin_config))

        return resolved if resolved.get("id", None) == identifier else SketchConfig()


def grader(
    func: Callable[..., GraderReturn],
) -> Callable[[str | None, str], GraderResult]:
    """Decorator that adapts a user grading function to the JSON-in/JSON-out
    contract used by the hosting LMS.

    The wrapped callable takes `(expect, ans)` where `ans` is a JSON string
    (optionally wrapped in `{"answer": "..."}`). It parses the submission,
    builds a `GradeableCollection` per plugin id, passes the collections
    whose names match the user function's parameters, and normalizes the
    return value into a `GraderResult`.

    Historical: the `(expect, ans)` signature is the EdX customresponse
    contract this library was originally built for (`expect` was the
    expected-answer string from `<customresponse expect="...">`). The
    PrairieLearn `pl-sketch` element does not call the decorator — it uses
    `grader_lib` directly — so `expect` is effectively unused in that path.
    """

    def jsinput_grader(expect: str | None, ans: str) -> GraderResult:
        try:
            gradeable_json = json.loads(ans)["answer"]
        except ValueError:
            gradeable_json = ans

        answer: SketchAnswer = json.loads(gradeable_json)

        if answer["apiVersion"] != "0.1":
            raise TypeError("Unsupported API version: " + answer["apiVersion"])

        # have to add the data versions to the config dict so they are
        # accessible in a grader
        answer["meta"]["config"]["dataVersions"] = answer["meta"]["dataVersions"]

        all_gradeables: dict[str, GradeableCollection] = {
            identifier: GradeableCollection(identifier, answer["meta"]["config"], gradeable_list)
            for identifier, gradeable_list in list(answer["data"].items())
        }

        # create new gradeables for group plugins in the config data
        plugins = answer["meta"]["config"].get("plugins", [])
        for plugin in plugins:
            if plugin.get("name") == "group":
                data: list[SketchItem] = []
                identifier = plugin["id"]
                config = answer["meta"]["config"]
                for p in plugin.get("plugins", []):
                    data.extend(deepcopy(answer["data"][p["id"]]))
                all_gradeables[identifier] = GradeableCollection(identifier, config, data)

        # filter gradeables for what the grader script is expecting
        args = list(inspect.signature(func).parameters.keys())
        gradeables = {validkey: all_gradeables[validkey] for validkey in args}

        result = func(**gradeables)  # run the user-provided grading function

        if isinstance(result, dict) and "ok" in result:
            # This is a customresponse-style dict
            return result
        # sketchinput-style tuple response
        match result:
            case (ok,):
                return {"ok": ok, "msg": ""}
            case (ok, msg):
                return {"ok": ok, "msg": msg}
            case _:
                raise ValueError("The grader function response was not formatted correctly")

    return jsinput_grader  # the decorated function


def config(configDict: SketchConfig) -> str:
    """Base64-encode a config dict for embedding in an HTML template."""
    return (
        base64.b64encode(json.dumps(configDict).encode(), altchars=b"-_")
        .replace(b"=", b"")
        .decode()
    )
