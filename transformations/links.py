# coding: utf-8

r"""Mechanical links modeling"""

import numpy as np

from transformations import translation_matrix, rotation_matrix


class Link(object):
    def __init__(self, p, u, v, tx, ty, tz, rx, ry, rz):
        self._p = p
        self._u = u
        self._v = v

        self.tx = tx
        self.ty = ty
        self.tz = tz

        self.rx = rx
        self.ry = ry
        self.rz = rz

    @property
    def p(self):
        return np.array(self._p)

    @property
    def u(self):
        return np.array(self._u)

    @property
    def v(self):
        return np.ndarray(self._v)

    @property
    def w(self):
        r"""Virtual 3rd anchor vector"""
        return np.cross(self.u, self.v)

    def transformation_matrix(self):
        tr = translation_matrix((tx * self.u, ty * self.v, tz * self.w))
        rot_x = rotation_matrix(rx, self.u, self.p)
        rot_y = rotation_matrix(ry, self.v, self.p)
        rot_z = rotation_matrix(rz, self.w, self.p)
        return np.dot(tr, rot_x, rot_y, rot_z)
