# coding: utf-8

r"""Mechanical links modeling"""

import numpy as np

from transformations import translation_matrix, rotation_matrix, superimposition_matrix


def find_transformation_to_world(p, u, v):
    v0 = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0)])
    v1 = np.array([p, p + u, p + v])

    return superimposition_matrix(v0.T, v1.T, scale=False, usesvd=False)


class Link(object):
    def __init__(self, anchor, tx=0, ty=0, tz=0, rx=0, ry=0, rz=0):
        self._anchor = anchor

        self.tx = tx
        self.ty = ty
        self.tz = tz

        self.rx = rx
        self.ry = ry
        self.rz = rz

    @property
    def anchor(self):
        return self._anchor

    @property
    def p(self):
        return self.anchor.p

    @property
    def u(self):
        return self.anchor.u

    @property
    def v(self):
        return self.anchor.v

    @property
    def w(self):
        r"""Virtual 3rd anchor vector"""
        return self.anchor.w

    @property
    def transformation_matrix(self):
        m = find_transformation_to_world(self.p, self.u, self.v)
        t_world = np.dot(m, np.array([self.tx, self.ty, self.tz, 0]))
        tr = translation_matrix([t_world[0], t_world[1], t_world[2]])
        rot_x = rotation_matrix(self.rx, self.u, self.p)
        rot_y = rotation_matrix(self.ry, self.v, self.p)
        rot_z = rotation_matrix(self.rz, self.w, self.p)
        from functools import reduce
        return reduce(np.dot, [tr, rot_x, rot_y, rot_z])
