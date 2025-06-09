import unittest
from unittest import TestCase

from ocaqda.utils.helper_utils import convert_and_merge_ranges


# noinspection PyMethodMayBeStatic
class ConvertAndMergeRangesTest(unittest.TestCase):

    def test_convert_and_merge_ranges_no_overlap(self):
        l = [[0, 1, ("Lorem")], [2, 3, ("Dolor")]]
        result = convert_and_merge_ranges(l)
        TestCase.assertListEqual(self, result, [[0, 1, "Lorem"], [2, 3, "Dolor"]])

    def test_convert_and_merge_ranges1(self):
        l = [[0, 1, ("Lorem")], [1, 2, ("Dolor")]]
        result = convert_and_merge_ranges(l)
        TestCase.assertListEqual(self, result, [[0, 0, "Lorem"], [1, 1, {"Lorem", "Dolor"}], [2, 2, "Dolor"]])

    def test_convert_and_merge_ranges2(self):
        l = [[23, 135, ("Lorem")], [24, 134, ("Dolor")]]
        result = convert_and_merge_ranges(l)
        TestCase.assertListEqual(self, result,
                                 [[23, 23, "Lorem"], [24, 134, {"Lorem", "Dolor"}], [135, 135, ("Lorem")]])

    def test_convert_and_merge_ranges3(self):
        l = [[20, 135, ("Lorem")], [130, 200, ("Dolor")]]
        result = convert_and_merge_ranges(l)
        TestCase.assertListEqual(self, result,
                                 [[20, 129, 'Lorem'], [130, 135, {'Dolor', 'Lorem'}], [136, 200, 'Dolor']])

    def test_convert_and_merge_ranges4(self):
        l = [[20, 135, ("Lorem")], [130, 200, ("Dolor")], [135, 201, ("Ipsum")]]
        result = convert_and_merge_ranges(l)
        expected = [[20, 129, 'Lorem'], [130, 134, {"Dolor", "Lorem"}],
                    [135, 135, {"Lorem", "Dolor", "Ipsum"}], [136, 200, {"Dolor", "Ipsum"}],
                    [201, 201, "Ipsum"]]
        print(expected)
        TestCase.assertListEqual(self, result, expected)

    def test_convert_and_merge_ranges5(self):
        l = [[20, 135, ("Lorem")], [135, 200, ("Dolor")]]
        result = convert_and_merge_ranges(l)
        TestCase.assertListEqual(self, result,
                                 [[20, 134, 'Lorem'], [135, 135, {'Dolor', 'Lorem'}], [136, 200, 'Dolor']])
