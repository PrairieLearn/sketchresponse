from math import pi, sqrt

from sketchresponse.grader_lib import GradeableFunction
from test_grader_lib import TestDataPolar


class TestPolarTransform(TestDataPolar.TestDataPolar):
    def test_polar_transform_points_true(self):
        data = self.loadData("test_grader_lib/polar_points_true.csv")
        for d in data:
            args1 = d["pt1"]
            pt1 = GradeableFunction.GradeableFunction(args1.grader, args1.submission, args1.tool_id)
            args2 = d["pt2"]
            pt2 = GradeableFunction.GradeableFunction(args2.grader, args2.submission, args2.tool_id)
            args3 = d["pt3"]
            pt3 = GradeableFunction.GradeableFunction(args3.grader, args3.submission, args3.tool_id)

            self.assertTrue(pt1.has_point_at(x=(11 * pi / 6), y=2, distTolerance=20))
            self.assertTrue(pt2.has_point_at(x=(5 * pi / 4), y=sqrt(2), distTolerance=20))
            self.assertTrue(pt3.has_point_at(x=(2 * pi / 3), y=2, distTolerance=20))

    def test_polar_transform_points_false(self):
        data = self.loadData("test_grader_lib/polar_points_false.txt")
        for d in data:
            args1 = d["pt1"]
            pt1 = GradeableFunction.GradeableFunction(args1.grader, args1.submission, args1.tool_id)
            args2 = d["pt2"]
            pt2 = GradeableFunction.GradeableFunction(args2.grader, args2.submission, args2.tool_id)
            args3 = d["pt3"]
            pt3 = GradeableFunction.GradeableFunction(args3.grader, args3.submission, args3.tool_id)

            isCorrect = True
            isCorrect = isCorrect and pt1.has_point_at(x=(11 * pi / 6), y=2, distTolerance=20)
            isCorrect = isCorrect and pt2.has_point_at(x=(5 * pi / 4), y=sqrt(2), distTolerance=20)
            isCorrect = isCorrect and pt3.has_point_at(x=(2 * pi / 3), y=2, distTolerance=20)

            self.assertFalse(isCorrect)

    def test_polar_transform_quartercircle_true(self):
        data = self.loadData("test_grader_lib/polar_quartercircle_true.txt")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_straight_between(pi, (3 * pi / 2)))
            self.assertFalse(f.does_exist_between(0, pi))
            self.assertFalse(f.does_exist_between((3 * pi / 2), 2 * pi))

    def test_polar_transform_quartercircle_false(self):
        data = self.loadData("test_grader_lib/polar_quartercircle_false.txt")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)

            isCorrect = True
            isCorrect = isCorrect and f.is_straight_between(pi, (3 * pi / 2))
            isCorrect = isCorrect and not f.does_exist_between(0, pi)
            isCorrect = isCorrect and not f.does_exist_between((3 * pi / 2), 2 * pi)

            self.assertFalse(isCorrect)

    def test_polar_transform_threelobe_true(self):
        data = self.loadData("test_grader_lib/polar_threelobe_true.txt")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            allowedFails = 4

            self.assertTrue(f.is_increasing_between(0, (pi / 6), failureTolerance=allowedFails))
            self.assertTrue(
                f.is_decreasing_between((pi / 6), (pi / 3), failureTolerance=allowedFails)
            )
            self.assertTrue(
                f.is_increasing_between((4 * pi / 6), (5 * pi / 6), failureTolerance=allowedFails)
            )
            self.assertTrue(
                f.is_decreasing_between((5 * pi / 6), pi, failureTolerance=allowedFails)
            )
            self.assertTrue(
                f.is_increasing_between((8 * pi / 6), (3 * pi / 2), failureTolerance=allowedFails)
            )
            self.assertTrue(
                f.is_decreasing_between((3 * pi / 2), (10 * pi / 6), failureTolerance=allowedFails)
            )

    def test_polar_transform_threelobe_false(self):
        data = self.loadData("test_grader_lib/polar_threelobe_false.txt")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            allowedFails = 4

            # This curve has wrong monotonicity - it's not a proper three-lobe shape
            # At least one check should fail (return False or 'ndef')
            r1 = f.is_increasing_between(0, (pi / 6), failureTolerance=allowedFails)
            self.assertEqual(r1, "ndef")  # function doesn't exist in this range

            r2 = f.is_decreasing_between((pi / 6), (pi / 3), failureTolerance=allowedFails)
            self.assertEqual(r2, False)  # function is increasing, not decreasing

            r3 = f.is_increasing_between((4 * pi / 6), (5 * pi / 6), failureTolerance=allowedFails)
            self.assertEqual(r3, True)

            r4 = f.is_decreasing_between((5 * pi / 6), pi, failureTolerance=allowedFails)
            self.assertEqual(r4, True)

            r5 = f.is_increasing_between((8 * pi / 6), (3 * pi / 2), failureTolerance=allowedFails)
            self.assertEqual(r5, True)

            r6 = f.is_decreasing_between((3 * pi / 2), (10 * pi / 6), failureTolerance=allowedFails)
            self.assertEqual(r6, True)


if __name__ == "__main__":
    testPolar = TestPolarTransform()
    testPolar.test_polar_transform_points_true()
    testPolar.test_polar_transform_points_false()
