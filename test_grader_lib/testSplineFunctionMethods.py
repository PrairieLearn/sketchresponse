import unittest

from sketchresponse.grader_lib.Axis import Axis
from sketchresponse.grader_lib.SplineFunction import SplineFunction


class TestSplineFunctionTolerance(unittest.TestCase):
    # Regression test for tolerance kwarg being silently passed as `functions`
    # to MultiFunction's init (positional-arg slot collision).
    def test_custom_tolerance_is_applied(self):
        xaxis = Axis([0, 10], 100)
        yaxis = Axis([10, 0], 100)
        path_info = [[10, 50], [30, 50], [50, 50], [70, 50]]
        grader = {"tolerance": 10, "debug": False}

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


if __name__ == "__main__":
    unittest.main()
