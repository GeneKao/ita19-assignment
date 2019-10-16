#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is my solution for the task 1
"""

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "16.10.2019"


def is_ccw(A, B, C):
    """
    Counter-clockwise checker for vector AB to AC
    Args:
        A: tuple, 2d point A
        B: tuple, 2d point B
        C: tuple, 2d point C
    Returns:
        True if counter-clockwise
    """

    # cross product for two 2d vectors
    a = (B[0] - A[0], B[1] - A[1])
    b = (C[0] - A[0], C[1] - A[1])
    cross_prod = a[0] * b[1] - b[0] * a[1]
    if cross_prod > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    A, B, C = (0, 0), (10, 0), (0, 10)
    print(is_ccw(A, B, C))
