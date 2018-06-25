# coding: utf-8

r"""Anchors stuff"""

import numpy as np

from conversions import p3_to_p4, p4_to_p3, v4_to_v3, v3_to_v4


class Anchor(object):
    r"""Anchor defined by a point and 2 perpendicular vectors

    u and v must be orthogonal and unitary

    Parameters
    ----------
    p : iterable
    u : iterable
    v : iterable
    name : str

    """
    def __init__(self, p, u, v, name):
        assert len(p) == len(u) == len(v) == 3
        assert np.dot(np.array(u), np.array(v)) == 0
        self._p = p
        self._u = u
        self._v = v
        self._name = name

    @property
    def p(self):
        return np.array(self._p)

    @property
    def u(self):
        r"""1st anchor vector, normally going out of the part"""
        return np.array(self._u)

    @property
    def v(self):
        r"""2nd anchor vector, normally tangential to the part surface"""
        return np.array(self._v)

    @property
    def w(self):
        r"""Virtual 3rd anchor vector"""
        return np.cross(self.u, self.v)

    @property
    def name(self):
        return self._name

    def transform(self, m):
        r"""Tranform the anchor with a 4x4 matrix

        Returns
        -------
        A new Anchor with the same name

        """
        assert np.shape(m) == (4, 4)
        return Anchor(p=p4_to_p3(np.dot(m, p3_to_p4(self.p))),
                      u=v4_to_v3(np.dot(m, v3_to_v4(self.u))),
                      v=v4_to_v3(np.dot(m, v3_to_v4(self.v))),
                      name=self.name)


def anchor_transformation(anchor_0, anchor_1):
    r"""

    Parameters
    ----------
    anchor_0 : Anchor
    anchor_1 : Anchor

    Returns
    -------
    4x4 matrix

    """
    from transformations import superimposition_matrix
    # compute points to transform
    v0 = np.array(
        [anchor_0.p, anchor_0.p + anchor_0.u, anchor_0.p + anchor_0.v])
    v1 = np.array(
        [anchor_1.p, anchor_1.p - anchor_1.u, anchor_1.p + anchor_1.v])

    return superimposition_matrix(v0.T, v1.T, scale=False, usesvd=False)
