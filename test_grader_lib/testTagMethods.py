from __future__ import absolute_import

import unittest

from sketchresponse.grader_lib import Asymptote, GradeableFunction, LineSegment, Polygon
from test_grader_lib import TestData


class TestTagMethods(TestData.TestData):
    #    Test the methods in the Polygon class
    # nothing, pentagon, overlapping

    # horizontal asymptote
    def test_horizontal_asymptote_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ha"]
        ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertTrue(ha.asyms[0].tag_equals("tag"))

    def test_horizontal_asymptote_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ha"]
        ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertFalse(ha.asyms[0].tag_equals("somethingelse"))

    def test_horizontal_asymptote_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ha"]
        ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(ha.contains_tag("tag"))

    def test_horizontal_asymptote_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ha"]
        ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNone(ha.contains_tag("somethingelse"))

    def test_horizontal_asymptote_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["ha"]
        ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNone(ha.contains_tag("tag"))

    # vertical asymptote
    def test_vertical_asymptote_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["va"]
        va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertTrue(va.asyms[0].tag_equals("tag"))

    def test_vertical_asymptote_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["va"]
        va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertFalse(va.asyms[0].tag_equals("somethingelse"))

    def test_vertical_asymptote_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["va"]
        va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(va.contains_tag("tag"))

    def test_vertical_asymptote_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["va"]
        va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNone(va.contains_tag("somethingelse"))

    def test_vertical_asymptote_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["va"]
        va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.tool_id)
        self.assertIsNone(va.contains_tag("tag"))

    # spline
    def test_spline_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["f"]
        f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertTrue(f.functions[0].tag_equals("tag"))

    def test_spline_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["f"]
        f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertFalse(f.functions[0].tag_equals("somethingelse"))

    def test_spline_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["f"]
        f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(f.contains_tag("tag"))

    def test_spline_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["f"]
        f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNone(f.contains_tag("somethingelse"))

    def test_spline_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["f"]
        f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNone(f.contains_tag("tag"))

    # point
    def test_point_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pt"]
        pt = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertTrue(pt.points[0].tag_equals("tag"))

    def test_point_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pt"]
        pt = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertFalse(pt.points[0].tag_equals("somethingelse"))

    def test_point_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pt"]
        pt = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(pt.contains_tag("tag"))

    def test_point_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pt"]
        pt = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNone(pt.contains_tag("somethingelse"))

    def test_point_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["pt"]
        pt = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
        self.assertIsNone(pt.contains_tag("tag"))

    # line segment
    def test_line_segment_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ls"]
        ls = LineSegment.LineSegments(args.grader, args.submission, args.tool_id)
        self.assertTrue(ls.segments[0].tag_equals("tag"))

    def test_line_segment_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ls"]
        ls = LineSegment.LineSegments(args.grader, args.submission, args.tool_id)
        self.assertFalse(ls.segments[0].tag_equals("somethingelse"))

    def test_line_segment_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ls"]
        ls = LineSegment.LineSegments(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(ls.contains_tag("tag"))

    def test_line_segment_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["ls"]
        ls = LineSegment.LineSegments(args.grader, args.submission, args.tool_id)
        self.assertIsNone(ls.contains_tag("somethingelse"))

    def test_line_segment_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["ls"]
        ls = LineSegment.LineSegments(args.grader, args.submission, args.tool_id)
        self.assertIsNone(ls.contains_tag("tag"))

    # polygon
    def test_polygon_has_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pg"]
        pg = Polygon.Polygons(args.grader, args.submission, args.tool_id)
        self.assertTrue(pg.polygons[0].tag_equals("tag"))

    def test_polygon_has_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pg"]
        pg = Polygon.Polygons(args.grader, args.submission, args.tool_id)
        self.assertFalse(pg.polygons[0].tag_equals("somethingelse"))

    def test_polygon_contains_tag_true(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pg"]
        pg = Polygon.Polygons(args.grader, args.submission, args.tool_id)
        self.assertIsNotNone(pg.contains_tag("tag"))

    def test_polygon_contains_tag_false(self):
        data = self.load_as_gradeable_collections("tag_data")
        d = data[0]
        args = d["pg"]
        pg = Polygon.Polygons(args.grader, args.submission, args.tool_id)
        self.assertIsNone(pg.contains_tag("somethingelse"))

    def test_polygon_no_tags(self):
        data = self.load_as_gradeable_collections("tag_none")
        d = data[0]
        args = d["pg"]
        pg = Polygon.Polygons(args.grader, args.submission, args.tool_id)
        self.assertIsNone(pg.contains_tag("tag"))


if __name__ == "__main__":
    unittest.main()
