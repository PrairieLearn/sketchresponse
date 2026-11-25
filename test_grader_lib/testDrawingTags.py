from typing import cast

import pytest

from sketchresponse.types import SketchCanvasSize, SketchDrawing, SketchTool
from sketchresponse.utils import format_drawing

RANGES: SketchCanvasSize = {
    "x_start": -2,
    "x_end": 2,
    "y_start": -2,
    "y_end": 2,
    "width": 400,
    "height": 400,
}


@pytest.mark.parametrize(
    ("name", "closed", "coordinates", "anchor"),
    [
        ("point", False, [-1, -1], {"x": 100, "y": 300}),
        ("line-segment", False, [-1, -1, 1, 1], {"x": 100, "y": 300}),
        ("horizontal-line", False, [-1], {"y": 300}),
        ("vertical-line", False, [-1], {"x": 100}),
        ("freeform", False, [-1, -1, 1, 1], {"x": 100, "y": 300}),
        ("spline", False, [-1, -1, 1, 1], {"x": 100, "y": 300}),
        ("polyline", False, [-1, -1, 1, 1], {"x": 100, "y": 300}),
        ("polyline", True, [-1, -1, 1, 1, 1, -1], {"x": 100, "y": 300}),
    ],
)
def test_tags_preserve_drawing_boundaries(name, closed, coordinates, anchor):
    tool = cast(SketchTool, {"id": "given", "name": name, "closed": closed})
    drawing: SketchDrawing = {
        "toolid": "given",
        "coordinates": coordinates,
        "fun": None,
        "xrange": [-1, 1],
    }
    state = format_drawing(
        [{**drawing, "tag": "A"}, drawing, {**drawing, "toolid": "other", "tag": "B"}],
        tool,
        RANGES,
    )
    points = (
        [point for curve in state for point in curve]
        if name in {"freeform", "spline", "polyline"}
        else state
    )
    assert [point for point in points if "tag" in point] == [{**anchor, "tag": "A"}]
    assert all(set(point) <= {"x", "y", "tag"} for point in points)
    assert "tag" not in drawing
    assert len(state) == (4 if name == "line-segment" else 2)


def test_discontinuous_function_has_one_tag_on_its_first_segment():
    tool = cast(SketchTool, {"id": "given", "name": "spline"})
    drawing: SketchDrawing = {
        "toolid": "given",
        "coordinates": [],
        "fun": "1/x",
        "xrange": [-1, 1],
        "tag": "f(x)",
    }
    state = format_drawing([drawing], tool, RANGES)
    assert len(state) == 2
    assert state[0][0]["tag"] == "f(x)"
    assert all("tag" not in point for curve in state[1:] for point in curve)


def test_empty_drawing_does_not_steal_the_next_drawings_tag():
    tool = cast(SketchTool, {"id": "given", "name": "spline"})
    empty: SketchDrawing = {
        "toolid": "given",
        "coordinates": [],
        "fun": None,
        "xrange": [-1, 1],
        "tag": "empty",
    }
    state = format_drawing(
        [empty, {**empty, "coordinates": [-1, -1, 1, 1], "tag": "next"}], tool, RANGES
    )
    assert state == [[], [{"x": 100, "y": 300, "tag": "next"}, {"x": 300, "y": 100}]]
