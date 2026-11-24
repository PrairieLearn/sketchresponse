import unittest
from typing import cast

from sketchresponse.types import SketchCanvasSize, SketchDrawing, SketchTool
from sketchresponse.utils import format_drawing

_RANGES: SketchCanvasSize = {
    "x_start": -4,
    "x_end": 4,
    "y_start": -4,
    "y_end": 4,
    "width": 400,
    "height": 400,
}


def _tool(name: str, tool_id: str = "f") -> SketchTool:
    return cast(SketchTool, {"name": name, "id": tool_id})


def _drawing(**kwargs) -> SketchDrawing:
    drawing = {"toolid": "f", "fun": None, "xrange": [-4, 4], "coordinates": []}
    drawing.update(kwargs)
    return cast(SketchDrawing, drawing)


class TestFormatDrawingLabels(unittest.TestCase):
    def assertLabelled(self, segment, label):
        self.assertEqual(segment[0]["tag"], label)
        self.assertIs(segment[0]["tagReadonly"], True)
        for point in segment[1:]:
            self.assertNotIn("tag", point)
            self.assertNotIn("tagReadonly", point)

    def assertUnlabelled(self, segment):
        for point in segment:
            self.assertNotIn("tag", point)
            self.assertNotIn("tagReadonly", point)

    def test_function_label_on_each_function_tool(self):
        for name in ["spline", "freeform", "polyline"]:
            with self.subTest(tool=name):
                result = format_drawing(
                    [_drawing(fun="x**2", xrange=[-1, 1], label="f(x)")],
                    _tool(name),
                    _RANGES,
                )
                self.assertEqual(len(result), 1)
                self.assertLabelled(result[0], "f(x)")

    def test_coordinates_label(self):
        for name in ["spline", "freeform", "polyline"]:
            with self.subTest(tool=name):
                result = format_drawing(
                    [_drawing(coordinates=[-2, 0, 0, 1, 2, 0], label="g")],
                    _tool(name),
                    _RANGES,
                )
                self.assertEqual(len(result), 1)
                self.assertLabelled(result[0], "g")

    def test_only_first_segment_of_discontinuous_function_is_labelled(self):
        result = format_drawing(
            [_drawing(fun="1/x", xrange=[-2, 2], label="h")],
            _tool("spline"),
            _RANGES,
        )
        self.assertGreater(len(result), 1)
        self.assertLabelled(result[0], "h")
        for segment in result[1:]:
            self.assertUnlabelled(segment)

    def test_each_drawing_gets_its_own_label(self):
        result = format_drawing(
            [
                _drawing(fun="x", xrange=[-1, 1], label="f"),
                _drawing(fun="x**2", xrange=[-1, 1]),
                _drawing(fun="-x", xrange=[-1, 1], label="g"),
            ],
            _tool("spline"),
            _RANGES,
        )
        self.assertEqual(len(result), 3)
        self.assertLabelled(result[0], "f")
        self.assertUnlabelled(result[1])
        self.assertLabelled(result[2], "g")

    def test_no_label_leaves_output_unchanged(self):
        for label in [None, ""]:
            with self.subTest(label=label):
                result = format_drawing(
                    [_drawing(fun="x**2", xrange=[-1, 1], label=label)],
                    _tool("spline"),
                    _RANGES,
                )
                self.assertUnlabelled(result[0])

    def test_drawings_for_other_tools_are_ignored(self):
        result = format_drawing(
            [_drawing(toolid="other", fun="x", xrange=[-1, 1], label="f")],
            _tool("spline"),
            _RANGES,
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
