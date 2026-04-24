import math
import unittest
from typing import cast

from sketchresponse.types import SketchConfig, SketchSubmission
from sketchresponse.utils import (
    graph_to_screen,
    graph_to_screen_submission,
    in_range,
    parse_function_string,
    screen_to_graph,
    screen_to_graph_submission,
)


def _config(width=400, height=400, xrange=(-4, 4), yrange=(-4, 4)) -> SketchConfig:
    return cast(
        SketchConfig,
        {
            "width": width,
            "height": height,
            "xrange": list(xrange),
            "yrange": list(yrange),
            "xscale": "linear",
            "yscale": "linear",
        },
    )


_EMPTY_SUBMISSION = cast(SketchSubmission, {})


class TestParseFunctionString(unittest.TestCase):
    def test_literal_constant(self):
        f = parse_function_string("3.14")
        self.assertEqual(f(0), 3.14)
        self.assertEqual(f(99), 3.14)

    def test_arithmetic(self):
        self.assertEqual(parse_function_string("x + 1")(2), 3)
        self.assertEqual(parse_function_string("2 * x ** 2")(3), 18)
        self.assertEqual(parse_function_string("-x")(5), -5)

    def test_allowed_math_functions(self):
        self.assertEqual(parse_function_string("sin(x)")(0), 0.0)
        self.assertEqual(parse_function_string("sqrt(x)")(4), 2.0)
        self.assertAlmostEqual(parse_function_string("cos(pi)")(0), -1.0)

    def test_y_is_aliased_to_x(self):
        # parse_function_string replaces "y" with "x" before parsing, so that
        # y-as-variable (used when xyflip is set) evaluates identically.
        self.assertEqual(parse_function_string("y * 2")(5), 10)

    def test_rejects_disallowed_builtin(self):
        with self.assertRaises(ValueError):
            parse_function_string("__import__('os')")

    def test_rejects_unknown_name(self):
        with self.assertRaises(ValueError):
            parse_function_string("foo + 1")

    def test_rejects_attribute_access(self):
        # Attribute nodes are not in the ast node whitelist.
        with self.assertRaises(TypeError):
            parse_function_string("x.real")


class TestInRange(unittest.TestCase):
    def test_value_inside(self):
        self.assertTrue(in_range(5, 0, 10))

    def test_value_below_start(self):
        self.assertFalse(in_range(-1, 0, 10))

    def test_endpoints_are_inclusive(self):
        self.assertTrue(in_range(0, 0, 10))
        self.assertTrue(in_range(10, 0, 10))

    def test_tolerance_shrinks_range(self):
        # With tolerance=2 the effective range is [2, 8].
        self.assertFalse(in_range(1, 0, 10, tolerance=2))
        self.assertTrue(in_range(3, 0, 10, tolerance=2))
        self.assertFalse(in_range(9, 0, 10, tolerance=2))


class TestCoordinateTransforms(unittest.TestCase):
    def test_graph_to_screen_endpoints_and_center(self):
        self.assertEqual(graph_to_screen(-4, 4, 400, -4), 0)
        self.assertEqual(graph_to_screen(-4, 4, 400, 4), 400)
        self.assertEqual(graph_to_screen(-4, 4, 400, 0), 200)

    def test_round_trip(self):
        cases = [(-4, 4, 400, 1.5), (0, 10, 250, 7.25), (-2.35, 2.35, 750, -1.0)]
        for start, end, canvas, value in cases:
            screen = graph_to_screen(start, end, canvas, value)
            back = screen_to_graph(start, end, canvas, screen)
            self.assertAlmostEqual(back, value, places=9)


class TestSubmissionCoordinateTransforms(unittest.TestCase):
    def test_xaxis_maps_xrange_to_width(self):
        cfg = _config()
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, True, False, 0),
            200,
        )
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, True, False, 4),
            400,
        )

    def test_distance_uses_zero_start(self):
        cfg = _config()
        # With distance=True, start=0, end=xrange[1]=4, canvas=width=400.
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, True, True, 2),
            200,
        )
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, True, True, 4),
            400,
        )

    def test_yaxis_is_flipped(self):
        # Y is flipped: start=yrange[1] (top of graph), end=yrange[0] (bottom).
        cfg = _config()
        # Graph y=4 (top) -> screen y=0 (top).
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, False, False, 4),
            0,
        )
        # Graph y=-4 (bottom) -> screen y=height (bottom).
        self.assertEqual(
            graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, False, False, -4),
            400,
        )

    def test_screen_to_graph_submission_inverts_graph_to_screen(self):
        cfg = _config(width=500, height=300, xrange=(-5, 5), yrange=(-3, 3))
        for use_xaxis, distance, value in [
            (True, False, 1.25),
            (True, True, 3.75),
            (False, False, -2.1),
        ]:
            screen = graph_to_screen_submission(_EMPTY_SUBMISSION, cfg, use_xaxis, distance, value)
            back = screen_to_graph_submission(_EMPTY_SUBMISSION, cfg, use_xaxis, distance, screen)
            self.assertTrue(math.isclose(back, value, abs_tol=1e-9))


if __name__ == "__main__":
    unittest.main()
