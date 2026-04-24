"""Type definitions for the sketchresponse package.

These TypedDicts describe the dict shapes that flow between the JavaScript
sketch tool and the Python grader backend. They are advisory (nothing
validates them at runtime) and are intended to help downstream consumers —
such as PrairieLearn's `pl-sketch` element — type-check the configuration
dicts they build and the answer JSON they receive.
"""

from __future__ import annotations

from typing import TypedDict


class SketchTool(TypedDict):
    name: str
    id: str
    label: str | None
    color: str | None
    readonly: bool | None
    helper: bool | None
    limit: int | None
    group: str | None
    dashStyle: str | None
    directionConstraint: str | None
    lengthConstraint: float | None
    size: int | None
    hollow: bool | None
    opacity: float | None
    closed: (
        bool | None
    )  # Polygons are internally "closed polylines" - this flag is the only difference
    fillColor: str | None
    arrowHead: int | None


class SketchGrader(TypedDict):
    type: str
    toolid: list[SketchTool]
    x: float | str | None
    y: float | None
    endpoint: str | None
    xrange: list[float] | None
    yrange: list[float] | None
    count: int | None
    fun: str | None
    xyflip: bool | None
    mode: str | None
    allowundefined: bool | None
    weight: int
    stage: int
    tolerance: int
    feedback: str | None
    debug: bool


class SketchCanvasSize(TypedDict):
    x_start: float
    x_end: float
    y_start: float
    y_end: float
    height: int
    width: int


class SketchDrawing(TypedDict):
    toolid: str
    fun: str | None
    xrange: list[float]
    coordinates: list[float]


class SketchItem(TypedDict, total=False):
    """A single gradeable item produced by a drawing tool.

    Spline-based tools (spline, freeform, polyline, horizontal-line,
    vertical-line, line-segment, polygon) populate `spline`; point-based
    tools populate `point`. `tag` is optionally set by the user.
    """

    spline: list[list[float]]  # list of [x_px, y_px] control points
    point: list[float]  # [x_px, y_px]
    tag: str


SketchGradeableData = dict[str, list[SketchItem]]


class SketchSubmission(TypedDict, total=False):
    """The `submission` dict constructed on the backend from the answer JSON.

    Only `gradeable` is guaranteed to be present; other keys may be added by
    frontends or wrappers. `total=False` keeps the type usable by callers that
    construct submissions with extra metadata.
    """

    gradeable: SketchGradeableData


class SketchConfig(TypedDict, total=False):
    """The configuration dict for a sketch problem.

    The same shape is used at three levels — the top-level problem config,
    per-plugin config entries inside `plugins`, and the runtime config dict
    the `@grader` decorator passes to `GradeableCollection`. Because the
    required keys differ between levels, all keys are `NotRequired`.

    Canvas / axis keys:
        `xrange`, `yrange`: `[min, max]` graph-space bounds
        `width`, `height`: canvas size in pixels
    Plugin keys:
        `id`: unique identifier for a plugin instance (toolid)
        `name`: plugin type (e.g. "spline", "point", "group")
        `plugins`: nested plugin configs (top-level and "group" plugins)
        `coordinates`: "polar" to transform to polar space
    Runtime-added keys:
        `dataVersions`: injected by the grader from the answer JSON
    """

    # Canvas / axis
    xrange: list[float]
    yrange: list[float]
    width: int
    height: int
    # Plugin
    id: str
    name: str
    plugins: list[SketchConfig]
    coordinates: str
    # Runtime
    dataVersions: dict[str, str]


class SketchMeta(TypedDict):
    config: SketchConfig
    dataVersions: dict[str, str]


class SketchAnswer(TypedDict):
    apiVersion: str
    meta: SketchMeta
    data: SketchGradeableData


class GraderResult(TypedDict, total=False):
    """The dict returned from a grader function (or from the decorator)."""

    ok: bool | str | float
    msg: str
