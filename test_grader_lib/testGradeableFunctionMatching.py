from sketchresponse.grader_lib import GradeableFunction
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
