import unittest
from typing import cast

from sketchresponse.grader_lib.Axis import Axis
from sketchresponse.grader_lib.CurveFunction import CurveFunction
from sketchresponse.grader_lib.SplineFunction import SplineFunction
from sketchresponse.types import SketchGrader


class TestSplineFunctionTolerance(unittest.TestCase):
    # Regression test for tolerance kwarg being silently passed as `functions`
    # to MultiFunction's init (positional-arg slot collision).
    def test_custom_tolerance_is_applied(self):
        xaxis = Axis([0, 10], 100)
        yaxis = Axis([10, 0], 100)
        path_info: list[list[float]] = [[10, 50], [30, 50], [50, 50], [70, 50]]
        grader = cast(SketchGrader, {"tolerance": 10, "debug": False})

        sf = SplineFunction(
            xaxis,
            yaxis,
            path_info,
            grader,
            "test-tool",
            tolerance={"straight_line": 0.9, "point_distance": 42},
        )

        self.assertEqual(sf.tolerance["straight_line"], 0.9)
        self.assertEqual(sf.tolerance["point_distance"], 42)
        self.assertEqual(len(sf.functions), 1)


class TestCurveFunction(unittest.TestCase):
    def test_get_x_for_yval_returns_real_floats(self):
        xaxis = Axis([0, 1], 100)
        yaxis = Axis([1, 0], 100)
        path_info: list[list[float]] = [
            [0, 100],
            [100 / 3, 100],
            [200 / 3, 100],
            [100, 0],
        ]
        grader = cast(SketchGrader, {"tolerance": 10, "debug": False})
        curve = CurveFunction(xaxis, yaxis, path_info, grader, "test-tool")

        xvals = curve.get_x_for_yval(0.125)

        self.assertEqual(len(xvals), 1)
        self.assertAlmostEqual(xvals[0], 0.5)
        self.assertListEqual([float] * len(xvals), [type(x) for x in xvals])

    def test_get_x_for_yval_filters_complex_roots_before_scaling(self):
        xaxis = Axis([0, 1e-6], 100)
        yaxis = Axis([1, 0], 100)
        path_info: list[list[float]] = [
            [0, 100],
            [100, 100],
            [0, 100],
            [100, 0],
        ]
        grader = cast(SketchGrader, {"tolerance": 10, "debug": False})
        curve = CurveFunction(xaxis, yaxis, path_info, grader, "test-tool")

        xvals = curve.get_x_for_yval(0.125)

        self.assertEqual(len(xvals), 1)
        self.assertAlmostEqual(xvals[0], 5e-7)


if __name__ == "__main__":
    unittest.main()
