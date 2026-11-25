import math
import unittest
from typing import cast

from sketchresponse.grader_lib import GradeableFunction
from sketchresponse.types import (
    SketchCanvasSize,
    SketchConfig,
    SketchGrader,
    SketchSubmission,
    SketchTool,
)
from sketchresponse.utils import format_drawing
from test_grader_lib import TestData


class TestGradeableFunctionMatchesFunction(TestData.TestData):
    """
    Coverage for matches_function / lt_function / gt_function on a spline-backed
    GradeableFunction. Uses the `constant_2` fixture — a freeform spline sitting
    at graph y ~= 2 across x in [-1, 1] — so the expected comparison outcomes
    are easy to reason about.
    """

    def _load(self):
        data = self.load_as_gradeable_collections("constant_2")
        args = data[0]["f"]
        return GradeableFunction.GradeableFunction(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )

    def test_matches_function_true_for_actual_shape(self):
        f = self._load()
        self.assertTrue(f.matches_function(lambda x: 2, -1, 1, 20))

    def test_matches_function_false_for_wrong_shape(self):
        f = self._load()
        self.assertFalse(f.matches_function(lambda x: -2, -1, 1, 20))

    def test_gt_function_true_when_curve_above(self):
        f = self._load()
        # Curve sits at y~=2, reference line at y=0 => curve is entirely greater.
        self.assertTrue(f.gt_function(lambda x: 0, -1, 1, 10))

    def test_gt_function_false_when_reference_above(self):
        f = self._load()
        self.assertFalse(f.gt_function(lambda x: 4, -1, 1, 10))

    def test_lt_function_true_when_curve_below(self):
        f = self._load()
        self.assertTrue(f.lt_function(lambda x: 4, -1, 1, 10))

    def test_neither_gt_nor_lt_when_reference_crosses(self):
        # y = 2x + 2 crosses y=2 at x=0: curve is above on [-1,0) and below on (0,1].
        f = self._load()
        self.assertFalse(f.gt_function(lambda x: 2 * x + 2, -1, 1, 10))
        self.assertFalse(f.lt_function(lambda x: 2 * x + 2, -1, 1, 10))


class TestClippedSplineGrading(unittest.TestCase):
    def test_gap_angle_with_complex_roots_at_graph_boundary(self):
        config: SketchConfig = {
            "xrange": [0, 2],
            "yrange": [-0.125, 0.125],
            "width": 200,
            "height": 100,
        }
        grader = cast(SketchGrader, {"tolerance": 10, "debug": False})

        for direction in (1, -1):
            with self.subTest(direction=direction):
                # y(t) = +/-t**3 crosses a graph boundary at t = 0.5.
                # The other two boundary roots are complex. Even the real
                # root has a complex dtype in NumPy's roots array.
                right_y = 50 - 25 * direction
                submission: SketchSubmission = {
                    "gradeable": {
                        "f": [
                            {
                                "spline": [
                                    [0, 50],
                                    [100 / 3, 50],
                                    [200 / 3, 50],
                                    [100, 50 - 400 * direction],
                                ]
                            },
                            {
                                "spline": [
                                    [150, right_y],
                                    [500 / 3, right_y],
                                    [550 / 3, right_y],
                                    [200, right_y],
                                ]
                            },
                        ]
                    }
                }
                f = GradeableFunction.GradeableFunction(grader, submission, config, "f")

                _, angle = f.get_angle_at_gap(1)

                # The clipped endpoint and the right branch are 100 pixels
                # apart horizontally and -/+25 pixels apart vertically.
                self.assertAlmostEqual(angle, math.atan2(-25 * direction, 100))

    def test_generated_piecewise_left_branch_matches_function(self):
        # pl-oer-lv101 question 1.38: y = x on [-12, endpoint], with the
        # visible domain clipped at y = -6. Exercise the solution formatter
        # and the match-function grader together.
        config: SketchConfig = {
            "xrange": [-12, 12],
            "yrange": [-6, 6],
            "width": 800,
            "height": 450,
        }
        ranges: SketchCanvasSize = {
            "x_start": -12,
            "x_end": 12,
            "y_start": -6,
            "y_end": 6,
            "width": 800,
            "height": 450,
        }
        grader = cast(SketchGrader, {"tolerance": 20, "debug": False})
        tool = cast(SketchTool, {"name": "freeform", "id": "left"})

        for endpoint in (-2, -1):
            with self.subTest(endpoint=endpoint):
                drawings = format_drawing(
                    [
                        {
                            "toolid": "left",
                            "fun": "x",
                            "xrange": [-12, endpoint],
                            "coordinates": [],
                        }
                    ],
                    tool,
                    ranges,
                )
                curves = cast(list[list[dict[str, float]]], drawings)
                submission: SketchSubmission = {
                    "gradeable": {
                        "left": [
                            {"spline": [[point["x"], point["y"]] for point in curve]}
                            for curve in curves
                        ]
                    }
                }
                f = GradeableFunction.GradeableFunction(grader, submission, config, "left")

                self.assertTrue(f.matches_function(lambda x: x, -12, endpoint, 20))
