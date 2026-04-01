import math
import unittest

from sketchresponse.grader_lib import GradeableFunction, Point
from test_grader_lib import TestData


class TestGradeableFunctionMethods(TestData.TestData):
    #    Test the methods in the GradeableFunction class
    def test_closest_point_to_point(self):
        # test using data from the app2-17-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            test_point = Point.Point(cp, -1, 3, pixel=False)
            dist, p = cp.closest_point_to_point(test_point)
            #            print '' + str(p.x) + ' ' + str(p.y)
            #            print dist
            # the square pixel distance can be quite big e.g. 98.5 for (-.95, 3.16)
            self.assertLess(dist, 100)
            self.assertIsNotNone(p)

    def test_closest_point_to_x(self):
        # test using data from the app2-17-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            dist, p = cp.closest_point_to_x(-1)
            self.assertLess(dist, 1)
            self.assertIsNotNone(p)

    def test_not_none_with_point_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            test_point = Point.Point(cp, -1, 3, pixel=False)
            self.assertIsNotNone(cp.get_point_at(100, point=test_point))

    def test_is_none_with_point_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            test_point = Point.Point(cp, -2, 5, pixel=False)
            self.assertIsNone(cp.get_point_at(100, point=test_point))

    def test_not_none_with_xy_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertIsNotNone(cp.get_point_at(100, x=-1, y=3))

    def test_is_none_with_xy_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertIsNone(cp.get_point_at(100, x=-2, y=5))

    def test_not_none_with_x_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            p = cp.get_point_at(100, x=-1)
            self.assertIsNotNone(p)
            self.assertAlmostEqual(p.y, 3, places=0)

    def test_is_none_with_x_get_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            p = cp.get_point_at(100, x=-2)
            self.assertIsNone(p)

    def test_true_with_point_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            test_point = Point.Point(cp, -1, 3, pixel=False)
            self.assertTrue(cp.has_point_at(-1, 3, 100, point=test_point))

    def test_false_with_point_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            test_point = Point.Point(cp, -2, 5, pixel=False)
            self.assertFalse(cp.has_point_at(-2, 5, 100, point=test_point))

    def test_true_with_xy_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(cp.has_point_at(-1, 3, 100))

    def test_false_with_xy_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(cp.has_point_at(-2, 5, 100))

    def test_true_with_x_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertTrue(cp.has_point_at(-1, None, 100))

    def test_false_with_x_has_point_at(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertFalse(cp.has_point_at(-2, None, 100))

    def test_get_number_of_points(self):
        # test using data from the hw4A-4-1 csv
        data = self.load_as_gradeable_collections("hw4A-tab4-problem1.anon.csv")
        for d in data:
            args = d["cp"]
            cp = GradeableFunction.GradeableFunction(args.grader, args.submission, args.tool_id)
            self.assertEqual(cp.get_number_of_points(), 2)

    def test_function_to_spline(self):
        range_data = {
            "x_start": -2,
            "x_end": 5,
            "y_start": -5,
            "y_end": 25,
            "height": 400,
            "width": 500,
        }
        expected = (
            [
                [2.8011204481792773, 282.0709983339741],
                [5.6022408963585395, 284.1009867999487],
                [8.403361344537817, 286.08996539792383],
                [11.204481792717079, 288.0379341278995],
                [14.005602240896355, 289.9448929898757],
                [16.806722689075634, 291.81084198385236],
                [19.607843137254896, 293.63578110982957],
                [22.408963585434176, 295.4197103678073],
                [25.210084033613448, 297.16262975778545],
                [28.01120448179271, 298.8645392797642],
                [30.81232492997199, 300.52543893374343],
                [33.61344537815127, 302.1453287197232],
                [36.41456582633053, 303.72420863770344],
                [39.215686274509814, 305.2620786876842],
                [42.01680672268908, 306.75893886966554],
                [44.81792717086835, 308.2147891836473],
                [47.619047619047606, 309.6296296296296],
                [50.42016806722688, 311.0034602076125],
                [53.221288515406165, 312.3362809175958],
                [56.02240896358542, 313.62809175957966],
                [58.8235294117647, 314.87889273356404],
                [61.62464985994398, 316.0886838395489],
                [64.42577030812325, 317.2574650775343],
                [67.22689075630252, 318.3852364475202],
                [70.0280112044818, 319.4719979495066],
                [72.82913165266106, 320.5177495834935],
                [75.63025210084034, 321.52249134948096],
                [78.43137254901963, 322.4862232474689],
                [81.23249299719888, 323.4089452774574],
                [84.03361344537815, 324.29065743944636],
                [86.83473389355741, 325.13135973343583],
                [89.6358543417367, 325.93105215942586],
                [92.43697478991598, 326.6897347174164],
                [95.23809523809523, 327.4074074074074],
                [98.0392156862745, 328.08407022939895],
                [100.84033613445376, 328.719723183391],
                [103.64145658263305, 329.3143662693836],
                [106.44257703081233, 329.86799948737666],
                [109.24369747899159, 330.38062283737025],
                [112.04481792717085, 330.85223631936435],
                [114.84593837535014, 331.28283993335896],
                [117.6470588235294, 331.67243367935407],
                [120.44817927170868, 332.02101755734975],
                [123.24929971988796, 332.3285915673459],
                [126.05042016806723, 332.5951557093426],
                [128.8515406162465, 332.8207099833397],
                [131.65266106442576, 333.00525438933744],
                [134.45378151260505, 333.14878892733566],
                [137.25490196078434, 333.2513135973344],
                [140.05602240896357, 333.3128283993336],
                [142.85714285714286, 333.3333333333333],
                [145.65826330532212, 333.3128283993336],
                [148.4593837535014, 333.2513135973344],
                [151.26050420168067, 333.14878892733566],
                [154.0616246498599, 333.00525438933744],
                [156.86274509803926, 332.8207099833397],
                [159.6638655462185, 332.5951557093426],
                [162.46498599439775, 332.3285915673459],
                [165.266106442577, 332.02101755734975],
                [168.0672268907563, 331.67243367935407],
                [170.86834733893556, 331.28283993335896],
                [173.66946778711483, 330.85223631936435],
                [176.47058823529412, 330.38062283737025],
                [179.2717086834734, 329.86799948737666],
                [182.07282913165267, 329.3143662693836],
                [184.87394957983196, 328.719723183391],
                [187.67507002801122, 328.08407022939895],
                [190.47619047619045, 327.4074074074074],
                [193.27731092436974, 326.6897347174164],
                [196.078431372549, 325.93105215942586],
                [198.87955182072827, 325.13135973343583],
                [201.68067226890753, 324.29065743944636],
                [204.48179271708685, 323.4089452774574],
                [207.2829131652661, 322.4862232474689],
                [210.08403361344537, 321.52249134948096],
                [212.88515406162466, 320.5177495834935],
                [215.68627450980392, 319.4719979495066],
                [218.48739495798318, 318.3852364475202],
                [221.28851540616247, 317.2574650775343],
                [224.0896358543417, 316.0886838395489],
                [226.890756302521, 314.87889273356404],
                [229.6918767507003, 313.62809175957966],
                [232.49299719887955, 312.3362809175958],
                [235.2941176470588, 311.0034602076125],
                [238.0952380952381, 309.6296296296296],
                [240.89635854341736, 308.2147891836473],
                [243.69747899159663, 306.75893886966554],
                [246.49859943977592, 305.2620786876842],
                [249.29971988795518, 303.72420863770344],
                [252.10084033613447, 302.1453287197232],
                [254.90196078431373, 300.52543893374343],
                [257.703081232493, 298.8645392797642],
                [260.5042016806723, 297.16262975778545],
                [263.3053221288515, 295.4197103678073],
                [266.1064425770308, 293.63578110982957],
                [268.9075630252101, 291.81084198385236],
                [271.7086834733893, 289.9448929898757],
                [274.5098039215687, 288.0379341278995],
                [277.3109243697479, 286.08996539792383],
                [280.11204481792714, 284.1009867999487],
                [282.91316526610643, 282.0709983339741],
            ],
            False,
            2,
        )
        self.assertEqual(
            GradeableFunction.function_to_spline(lambda x: x**2, -2, 2, range_data), expected
        )

    def test_function_to_spline_broken(self):
        range_data = {
            "x_start": -2,
            "x_end": 5,
            "y_start": -5,
            "y_end": 25,
            "height": 400,
            "width": 500,
        }
        expected = ([], True, -1.9597843137254902)
        self.assertEqual(
            GradeableFunction.function_to_spline(lambda x: math.log(x), -2, 2, range_data), expected
        )


if __name__ == "__main__":
    unittest.main()
