# coding: utf-8

r"""Convert points and vectors from 3 numbers representation to 4 numbers
representation and back
"""

import numpy as np


def p3_to_p4(p3):
    assert isinstance(p3, np.ndarray)
    assert len(p3) == 3
    return np.append(p3, 1)


def p4_to_p3(p4):
    assert isinstance(p4, np.ndarray)
    assert len(p4) == 4
    return p4[0: 3]


def v3_to_v4(v3):
    assert isinstance(v3, np.ndarray)
    assert len(v3) == 3
    return np.append(v3, 0)


def v4_to_v3(v4):
    assert isinstance(v4, np.ndarray)
    assert len(v4) == 4
    return v4[0: 3]