import unittest

from sketchresponse.grader_lib import Asymptote
from test_grader_lib import TestData


class TestAsymptoteMethods(TestData.TestData):
    #    Test the methods in the Asymptote class

    def test_closest_asym_to_value(self):
        # test using data from the app2-7-1 csv
        data = self.load_as_gradeable_collections("app_2-tab7-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            dist, v = va.closest_asym_to_value(-1)
            self.assertLess(dist, 1)
            self.assertIsNotNone(v)

    def test_not_none_get_asym_at_value(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            v = va.get_asym_at_value(-7)
            self.assertIsNotNone(v)

    def test_none_get_asym_at_value(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            v = va.get_asym_at_value(-5)
            self.assertIsNone(v)

    def test_true_has_asym_at_value(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            self.assertTrue(va.has_asym_at_value(-7))

    def test_false_has_asym_at_value(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            self.assertFalse(va.has_asym_at_value(-5))

    def test_true_asym_greater_less_than(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["ha"]
            ha = Asymptote.HorizontalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            self.assertTrue(ha.has_asym_at_value(0))
            self.assertTrue(ha.is_greater_than_y_between(-1, -4.5, 4.5, 10))
            self.assertTrue(ha.is_less_than_y_between(1, -4.5, 4.5, 10))
            self.assertFalse(ha.is_greater_than_y_between(1, -4.5, 4.5, 10))
            self.assertFalse(ha.is_less_than_y_between(-1, -4.5, 4.5, 10))

    def test_get_number_of_asyms(self):
        # test using data from the hw4A-8-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab8-problem1.anon.csv")
        for d in data:
            args = d["va"]
            va = Asymptote.VerticalAsymptotes(args.grader, args.submission, args.submission["meta"]["config"], args.tool_id)
            self.assertEqual(va.get_number_of_asyms(), 3)


if __name__ == "__main__":
    unittest.main()
