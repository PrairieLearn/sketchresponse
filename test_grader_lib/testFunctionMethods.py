# from ..sketchinput import GradeableCollection
import unittest

# from ..csv_to_data_new import load_csv_data
from sketchresponse.grader_lib import GradeableFunction
from test_grader_lib import TestData


class TestFunctionMethods(TestData.TestData):
    #    The Function class implements the following methods to be tested
    #      has_value_y_at_x
    #      is_zero_at_x_equals_zero
    #      is_greater_than_y_between
    #      is_less_than_y_between
    # Execute: From outside the test_backend directory:
    # python -m test_backend.TestFunctionMethods

    def test_true__has_value_y_at_x(self):
        # initialize data from u4-psA-u2b1-a.py csv data
        # data = self.load_gradeable_function('hw4A-tab4-problem1.anon.csv')
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.has_value_y_at_x(1, 0))

    def test_false__has_value_y_at_x(self):
        # initialize data from u4-psA-u2b1-a.py csv data
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.has_value_y_at_x(3, 0))

    def test_threshold__has_value_y_at_x(self):
        # At x=0, function values range from ~0.35 to ~1.85 across all test entries (yscale ~47px/unit)
        # y=5 is about 3.15 units (~147px) away from the closest function value
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            # y=5 should fail with tight tolerance (100px < 147px needed)
            self.assertFalse(f.has_value_y_at_x(5, 0, yTolerance=100))
            # But y=5 should pass with larger tolerance (200px > 147px needed)
            self.assertTrue(f.has_value_y_at_x(5, 0, yTolerance=200))

    def test_true__is_zero_at_x_equals_zero(self):
        # initialize data from u4-ps4B-criticaldamping.py csv data
        data = self.load_as_gradeable_collections("hw4B-tab4-problem4.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_zero_at_x_equals_zero())

    def test_false__is_zero_at_x_equals_zero(self):
        # initialize data from u4-app2-sketch1.py csv data
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.is_zero_at_x_equals_zero())

    def test_true__is_greater_than_y_between(self):
        # initialize data from u4-app2-sketch1.py csv data
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_greater_than_y_between(2, -4, -1))

    def test_false__is_greater_than_y_between(self):
        # initialize data from u4-app2-sketch1.py csv data
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.is_greater_than_y_between(0, -1, 1))

    def test_true__is_less_than_y_between(self):
        # initialize data from u4-app2-sketch1.py csv data
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(f.is_less_than_y_between(0, -1, 1))

    def test_false__is_less_than_y_between(self):
        # initialize data from u4-app2-sketch1.py csv data
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["f"]
            f = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(f.is_less_than_y_between(2, -4, -1))


if __name__ == "__main__":
    unittest.main()
