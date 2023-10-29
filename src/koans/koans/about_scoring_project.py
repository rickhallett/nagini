#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *
from collections import Counter

# Greed is a dice game where you roll up to five dice to accumulate
# points.  The following "score" function will be used to calculate the
# score of a single roll of the dice.
#
# A greed roll is scored as follows:
#
# * A set of three ones is 1000 points
#
# * A set of three numbers (other than ones) is worth 100 times the
#   number. (e.g. three fives is 500 points).
#
# * A one (that is not part of a set of three) is worth 100 points.
#
# * A five (that is not part of a set of three) is worth 50 points.
#
# * Everything else is worth 0 points.
#
#
# Examples:
#
# score([1,1,1,5,1]) => 1150 points
# score([2,3,4,6,2]) => 0 points
# score([3,4,5,3,3]) => 350 points
# score([1,5,1,2,4]) => 250 points
#
# More scoring examples are given in the tests below:
#
# Your goal is to write the score method.

"""
Strategy 1: make dict of scores

make dict
    for each die
        inc dict key

for each dict key
    if key value >= 3
        score key value 
        dec key by 3
    if key == 1
        score 100 x key value
        key value = 0
    if key == 5
        score 50 x key valye
        key value = 0    
"""


def score(turns):
    pts = 0

    rolls = {face: turns.count(face) for face in set(turns)}

    for face, count in rolls.items():

        if count >= 3:
            if face == 1:
                pts += 1000
            else:
                pts += face * 100
            rolls[face] -= 3

        if rolls[face]:
            if face == 1:
                pts += rolls[face] * 100
                rolls[face] -= count
            elif face == 5:
                pts += rolls[face] * 50
                rolls[face] -= count

    return pts


def score_with_counter(turns):
    pts = 0
    rolls = Counter(turns)

    for face, count in rolls.items():
        triplets, remainder = divmod(count, 3)

        if triplets:
            pts += 1000 if face == 1 else face * 100

        if remainder:
            if face == 1:
                pts += remainder * 100
            elif face == 5:
                pts += remainder * 50

    return pts


class AboutScoringProject(Koan):
    def test_score_of_an_empty_list_is_zero(self):
        self.assertEqual(0, score([]))

    def test_score_of_a_single_roll_of_5_is_50(self):
        self.assertEqual(50, score([5]))

    def test_score_of_a_single_roll_of_1_is_100(self):
        self.assertEqual(100, score([1]))

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores(self):
        self.assertEqual(300, score([1, 5, 5, 1]))

    def test_score_of_single_2s_3s_4s_and_6s_are_zero(self):
        self.assertEqual(0, score([2, 3, 4, 6]))

    def test_score_of_a_triple_1_is_1000(self):
        self.assertEqual(1000, score([1, 1, 1]))

    def test_score_of_other_triples_is_100x(self):
        self.assertEqual(200, score([2, 2, 2]))
        self.assertEqual(300, score([3, 3, 3]))
        self.assertEqual(400, score([4, 4, 4]))
        self.assertEqual(500, score([5, 5, 5]))
        self.assertEqual(600, score([6, 6, 6]))

    def test_score_of_mixed_is_sum(self):
        self.assertEqual(250, score([2, 5, 2, 2, 3]))
        self.assertEqual(550, score([5, 5, 5, 5]))
        self.assertEqual(1150, score([1, 1, 1, 5, 1]))

    def test_ones_not_left_out(self):
        self.assertEqual(300, score([1, 2, 2, 2]))
        self.assertEqual(350, score([1, 5, 2, 2, 2]))

    # GPT-4 additional test cases

    def test_minimum_number_of_rolls(self):
        # Single roll that should yield 0 points
        self.assertEqual(0, score([2]))
        # Single roll that should yield 100 points
        self.assertEqual(100, score([1]))
        # Single roll that should yield 50 points
        self.assertEqual(50, score([5]))

    def test_maximum_number_of_rolls(self):
        self.assertEqual(0, score([2, 3, 4, 6, 6]))  # Max rolls with 0 points
        self.assertEqual(1200, score([1, 1, 1, 1, 1]))  # Max rolls with all 1s
        self.assertEqual(600, score([5, 5, 5, 5, 5]))  # Max rolls with all 5s

    def test_mixed_scenarios(self):
        # Triple 2s and double 1s
        self.assertEqual(400, score([1, 1, 2, 2, 2]))
        self.assertEqual(0, score([2, 3, 4, 6, 6, 2]))  # No scoring rolls

    def test_empty_input(self):
        self.assertEqual(0, score([]))  # Empty list

    def test_invalid_input(self):
        self.assertEqual(0, score([0]))  # Invalid face value
        self.assertEqual(0, score([7]))  # Invalid face value
        self.assertEqual(0, score([-1]))  # Negative face value

    # -----

    def test_score_of_an_empty_list_is_zero_alt(self):
        self.assertEqual(0, score_with_counter([]))

    def test_score_of_a_single_roll_of_5_is_50_alt(self):
        self.assertEqual(50, score_with_counter([5]))

    def test_score_of_a_single_roll_of_1_is_100_alt(self):
        self.assertEqual(100, score_with_counter([1]))

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores_alt(self):
        self.assertEqual(300, score_with_counter([1, 5, 5, 1]))

    def test_score_of_single_2s_3s_4s_and_6s_are_zero_alt(self):
        self.assertEqual(0, score_with_counter([2, 3, 4, 6]))

    def test_score_of_a_triple_1_is_1000_alt(self):
        self.assertEqual(1000, score_with_counter([1, 1, 1]))

    def test_score_of_other_triples_is_100x_alt(self):
        self.assertEqual(200, score_with_counter([2, 2, 2]))
        self.assertEqual(300, score_with_counter([3, 3, 3]))
        self.assertEqual(400, score_with_counter([4, 4, 4]))
        self.assertEqual(500, score_with_counter([5, 5, 5]))
        self.assertEqual(600, score_with_counter([6, 6, 6]))

    def test_score_of_mixed_is_sum_alt(self):
        self.assertEqual(250, score_with_counter([2, 5, 2, 2, 3]))
        self.assertEqual(550, score_with_counter([5, 5, 5, 5]))
        self.assertEqual(1150, score_with_counter([1, 1, 1, 5, 1]))

    def test_ones_not_left_out_alt(self):
        self.assertEqual(300, score_with_counter([1, 2, 2, 2]))
        self.assertEqual(350, score_with_counter([1, 5, 2, 2, 2]))

    # GPT-4 additional test cases

    def test_minimum_number_of_rolls_alt(self):
        # Single roll that should yield 0 points
        self.assertEqual(0, score_with_counter([2]))
        # Single roll that should yield 100 points
        self.assertEqual(100, score_with_counter([1]))
        # Single roll that should yield 50 points
        self.assertEqual(50, score_with_counter([5]))

    def test_maximum_number_of_rolls_alt(self):
        self.assertEqual(0, score_with_counter(
            [2, 3, 4, 6, 6]))  # Max rolls with 0 points
        self.assertEqual(1200, score_with_counter(
            [1, 1, 1, 1, 1]))  # Max rolls with all 1s
        self.assertEqual(600, score_with_counter(
            [5, 5, 5, 5, 5]))  # Max rolls with all 5s

    def test_mixed_scenarios_alt(self):
        # Triple 2s and double 1s
        self.assertEqual(400, score_with_counter([1, 1, 2, 2, 2]))
        self.assertEqual(0, score_with_counter(
            [2, 3, 4, 6, 6, 2]))  # No scoring rolls

    def test_empty_input_alt(self):
        self.assertEqual(0, score_with_counter([]))  # Empty list

    def test_invalid_input_alt(self):
        self.assertEqual(0, score_with_counter([0]))  # Invalid face value
        self.assertEqual(0, score_with_counter([7]))  # Invalid face value
        self.assertEqual(0, score_with_counter([-1]))  # Negative face value
