#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *

# You need to write the triangle method in the file 'triangle.py'
from .triangle import *


def triangle(a: int, b: int, c: int) -> str:
    l = len(set([a, b, c]))
    if l == 1:
        return 'equilateral'
    elif l == 2:
        return 'isosceles'
    else:
        return 'scalene'


def triangle(a, b, c): return 'equilateral' if len(
    set([a, b, c])) == 1 else 'isosceles' if len(set([a, b, c])) == 2 else 'scalene'


def triangle(a, b, c): return {1: 'equilateral',
                               2: 'isosceles', 3: 'scalene'}[len(set([a, b, c]))]


class AboutTriangleProject(Koan):

    def test_equilateral_triangles_have_equal_sides(self):
        self.assertEqual('equilateral', triangle(2, 2, 2))
        self.assertEqual('equilateral', triangle(10, 10, 10))

    def test_isosceles_triangles_have_exactly_two_sides_equal(self):
        self.assertEqual('isosceles', triangle(3, 4, 4))
        self.assertEqual('isosceles', triangle(4, 3, 4))
        self.assertEqual('isosceles', triangle(4, 4, 3))
        self.assertEqual('isosceles', triangle(10, 10, 2))

    def test_scalene_triangles_have_no_equal_sides(self):
        self.assertEqual('scalene', triangle(3, 4, 5))
        self.assertEqual('scalene', triangle(10, 11, 12))
        self.assertEqual('scalene', triangle(5, 4, 2))
