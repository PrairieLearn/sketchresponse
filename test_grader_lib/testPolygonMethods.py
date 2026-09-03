import unittest

from sympy.geometry import Segment

from sketchresponse.grader_lib import Polygon
from test_grader_lib import TestData


class TestPolygonMethods(TestData.TestData):
    #    Test the methods in the Polygon class
    # nothing, pentagon, overlapping

    # point containment
    def test_contains_point_true(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.contains_point(0, 1))

    def test_null_polygon_submission_is_ignored(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        args.submission["gradeable"][args.tool_id].insert(0, None)

        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )

        self.assertEqual(poly.get_polygon_count(), 1)
        self.assertTrue(poly.contains_point(0, 1))

    def test_contains_point_false(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.contains_point(3, 3))

    def test_polygon_contains_point_true(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.polygon_contains_point(poly.polygons[0], [0, 1]))

    def test_polygon_contains_point_false(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.polygon_contains_point(poly.polygons[0], [3, 3]))

    # polygon containment
    def test_contains_polygon_true(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.contains_polygon([[0, 1]]))

    def test_contains_polygon_false(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.contains_polygon([[3, 3]]))

    def test_polygon_contains_polygon_true(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.polygon_contains_polygon(poly.polygons[0], [[0, 1]]))

    def test_polygon_contains_polygon_false(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.polygon_contains_polygon(poly.polygons[0], [[3, 3]]))

    # point on boundary
    def test_point_is_on_boundary_true(self):
        data = self.load_as_gradeable_collections("polygon_boundary")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.point_is_on_boundary([0, 1]))

    def test_point_is_on_boundary_false(self):
        data = self.load_as_gradeable_collections("polygon_boundary")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.point_is_on_boundary([3, 3]))

    def test_point_is_on_polygon_boundary_true(self):
        data = self.load_as_gradeable_collections("polygon_boundary")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertTrue(poly.point_is_on_polygon_boundary(poly.polygons[0], [0, 1]))

    def test_point_is_on_polygon_boundary_false(self):
        data = self.load_as_gradeable_collections("polygon_boundary")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        self.assertFalse(poly.point_is_on_polygon_boundary(poly.polygons[0], [3, 3]))

    # intersections with line segment
    def test_intersections_with_boundary_true(self):
        data = self.load_as_gradeable_collections("polygon_intersection")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        intersections = poly.get_intersections_with_boundary([[-2, 0], [0, 2]])
        self.assertTrue(len(intersections) > 0)
        self.assertEqual(len(intersections[0]), 2)

    def test_intersections_with_boundary_false(self):
        data = self.load_as_gradeable_collections("polygon_intersection")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        intersections = poly.get_intersections_with_boundary([[-2, 0], [-3, -3]])
        self.assertTrue(len(intersections) > 0)
        self.assertEqual(len(intersections[0]), 0)

    def test_intersections_with_polygon_boundary_true(self):
        data = self.load_as_gradeable_collections("polygon_intersection")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        intersections = poly.get_intersections_with_polygon_boundary(
            poly.polygons[0], [[-2, 0], [0, 2]]
        )
        self.assertEqual(len(intersections), 2)

    def test_intersections_with_polygon_boundary_false(self):
        data = self.load_as_gradeable_collections("polygon_intersection")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )
        intersections = poly.get_intersections_with_polygon_boundary(
            poly.polygons[0], [[-2, 0], [-3, -3]]
        )
        self.assertEqual(len(intersections), 0)

    def test_segment_range_intersection(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )

        for segment_in_range in (poly.segment_in_range, poly.segment_in_range_strict):
            with self.subTest(method=segment_in_range.__name__):
                self.assertFalse(segment_in_range(Segment((-2, 0), (-2, 1)), -1, 1))
                self.assertFalse(segment_in_range(Segment((2, 0), (2, 1)), -1, 1))
                self.assertTrue(segment_in_range(Segment((-1, 0), (-1, 1)), -1, 1))
                self.assertTrue(segment_in_range(Segment((1, 0), (1, 1)), -1, 1))
                self.assertTrue(segment_in_range(Segment((-2, 0), (2, 0)), -1, 1))
                self.assertTrue(segment_in_range(Segment((2, 0), (-2, 0)), -1, 1))

    def test_cut_vertical_segments(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]
        poly = Polygon.Polygons(
            args.grader, args.submission, args.submission["meta"]["config"], args.tool_id
        )

        self.assertIsNone(poly.cut_segment(Segment((-2, 0), (-2, 1)), -1, 1))
        self.assertIsNone(poly.cut_segment(Segment((2, 0), (2, 1)), -1, 1))
        self.assertEqual(
            set(poly.cut_segment(Segment((-1, 0), (-1, 1)), -1, 1).points),
            set(Segment((-1, 0), (-1, 1)).points),
        )
        self.assertEqual(
            set(poly.cut_segment(Segment((1, 0), (1, 1)), -1, 1).points),
            set(Segment((1, 0), (1, 1)).points),
        )
        self.assertEqual(
            set(poly.cut_segment(Segment((0, -3), (0, 3)), -1, 1).points),
            set(Segment((0, -2.5), (0, 2.5)).points),
        )

    def test_ltgt_function_ignores_vertical_edges_outside_range(self):
        data = self.load_as_gradeable_collections("polygon_point")
        d = data[0]
        args = d["pl"]

        for method, grader_type, points, func in (
            (
                "gt_function",
                "greater-than",
                [(0, 1.5), (2, 1.5), (2, 2), (0, 2)],
                lambda x: x**2,
            ),
            (
                "lt_function",
                "less-than",
                [(0, -2), (2, -2), (2, -1.5), (0, -1.5)],
                lambda x: -(x**2),
            ),
        ):
            with self.subTest(method=method):
                args.grader["type"] = grader_type
                args.grader["tolerance"] = 0
                poly = Polygon.Polygons(
                    args.grader,
                    args.submission,
                    args.submission["meta"]["config"],
                    args.tool_id,
                )
                polygon = Polygon.Polygon(points)
                poly.set_polygon_range_defined(polygon)
                poly.polygons = [polygon]

                self.assertTrue(getattr(poly, method)(func, -1, 1, 0))


if __name__ == "__main__":
    unittest.main()
