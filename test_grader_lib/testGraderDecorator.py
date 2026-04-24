import json
import unittest
from typing import cast

from sketchresponse.sketchresponse import GradeableCollection, grader
from sketchresponse.types import SketchConfig


def _ans(data=None, plugins=None, api_version="0.1", wrap_config=True):
    """Build a minimal answer JSON string the @grader decorator accepts."""
    config: dict = {}
    if plugins is not None:
        config["plugins"] = plugins
    inner = json.dumps(
        {
            "apiVersion": api_version,
            "meta": {"config": config, "dataVersions": {}},
            "data": data if data is not None else {"pts": []},
        }
    )
    return json.dumps({"answer": inner})


class TestGraderDecoratorReturnShapes(unittest.TestCase):
    def test_one_tuple_returns_empty_msg(self):
        @grader
        def g(pts):
            return (True,)

        self.assertEqual(g(None, _ans()), {"ok": True, "msg": ""})

    def test_two_tuple_passes_msg(self):
        @grader
        def g(pts):
            return (False, "wrong")

        self.assertEqual(g(None, _ans()), {"ok": False, "msg": "wrong"})

    def test_three_tuple_raises(self):
        # Behavior change from master: master silently truncated 3-tuples to
        # (result[0], result[1]); the new match-based code raises.
        @grader
        def g(pts):
            return (True, "a", "b")

        with self.assertRaises(ValueError):
            g(None, _ans())

    def test_dict_passthrough(self):
        @grader
        def g(pts):
            return {"ok": True, "msg": "hi"}

        self.assertEqual(g(None, _ans()), {"ok": True, "msg": "hi"})


class TestGraderDecoratorConfigTolerance(unittest.TestCase):
    def test_config_without_plugins_key(self):
        # master raised KeyError on missing "plugins"; branch treats it as [].
        @grader
        def g(pts):
            return (True,)

        # _ans() with no plugins arg omits the "plugins" key entirely.
        self.assertEqual(g(None, _ans()), {"ok": True, "msg": ""})

    def test_unsupported_api_version_raises(self):
        @grader
        def g(pts):
            return (True,)

        with self.assertRaises(TypeError):
            g(None, _ans(api_version="0.2"))


class TestResolveParamsForId(unittest.TestCase):
    def test_matches_top_level_id(self):
        config = cast(SketchConfig, {"id": "outer", "xrange": [0, 10]})
        resolved = GradeableCollection.resolve_params_for_id("outer", config)
        self.assertEqual(resolved.get("xrange"), [0, 10])

    def test_matches_nested_plugin_id(self):
        config = cast(
            SketchConfig,
            {
                "id": "outer",
                "xrange": [0, 10],
                "plugins": [{"id": "inner", "yrange": [0, 5]}],
            },
        )
        resolved = GradeableCollection.resolve_params_for_id("inner", config)
        self.assertEqual(resolved.get("yrange"), [0, 5])

    def test_unknown_id_returns_empty(self):
        config = cast(SketchConfig, {"id": "outer", "xrange": [0, 10]})
        resolved = GradeableCollection.resolve_params_for_id("missing", config)
        self.assertEqual(dict(resolved), {})

    def test_collection_exposes_params(self):
        config = cast(SketchConfig, {"id": "pts", "xrange": [0, 10]})
        coll = GradeableCollection("pts", config, [])
        self.assertEqual(coll.params.get("xrange"), [0, 10])
        self.assertEqual(coll.identifier, "pts")


if __name__ == "__main__":
    unittest.main()
