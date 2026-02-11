from __future__ import absolute_import

import unittest

from sketchresponse.grader_lib import GradeableFunction
from test_grader_lib import TestData


class TestMultiFunctionMethods(TestData.TestData):
    #    Test the methods in the MultiFunction class
    #      is_straight
    #      is_straight_between

    def test_true_is_straight(self):
        data = self.load_as_gradeable_collections("straight_line")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_straight())

    def test_false_is_straight(self):
        data = self.load_as_gradeable_collections("min_at_zero")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.is_straight())

    def test_true_is_straight_between(self):
        data = self.load_as_gradeable_collections("straight_line")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_straight_between(-1, 1))

    def test_false_is_straight_between(self):
        data = self.load_as_gradeable_collections("min_at_zero")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.is_straight_between(-1, 1))

    def test_true_get_vertical_line_crossings(self):
        data = self.load_as_gradeable_collections("vert_cross")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertEqual(len(f.get_vertical_line_crossings(0)), 2)

    def test_false_get_vertical_line_crossings(self):
        data = self.load_as_gradeable_collections("horiz_cross")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertNotEqual(len(f.get_vertical_line_crossings(0)), 2)

    def test_true_get_horizontal_line_crossings(self):
        data = self.load_as_gradeable_collections("horiz_cross")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertEqual(len(f.get_horizontal_line_crossings(0)), 2)

    def test_false_get_horizontal_line_crossings(self):
        data = self.load_as_gradeable_collections("vert_cross")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertNotEqual(len(f.get_horizontal_line_crossings(0)), 2)


if __name__ == "__main__":
    unittest.main()
