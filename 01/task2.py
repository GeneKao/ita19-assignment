#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is my solution for the task 2
"""

import re
from .task1 import is_ccw

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "16.10.2019"


def read_pt_from_txt(file):
    """
    Open a file with three points tuples
    Args:
        file: string, a file name
    Returns:
        list of three points tuple
    """
    with open(file, 'r') as f:
        three_points_list = []
        for pts_str in f.readlines():
            # find all the floating numbers
            values = re.findall(r'\d+\.\d+', pts_str)
            # pair them with two
            three_points = tuple([(float(x), float(y)) for x, y in zip(values[0::2], values[1::2])])
            three_points_list.append(three_points)
        return three_points_list


if __name__ == '__main__':

    points = read_pt_from_txt('points.txt')
    for p in points:
        print(p)
        print(is_ccw(p[0], p[1], p[2]))
