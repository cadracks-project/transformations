# TODO : transform around the anchor
#          -> should generate another matrix stored on the part
#             or on the assembly
#             (since assemblies can be put together with anchors)
#        transform an assembly

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


class Anchor(object):
    def __init__(self, p, u, v, name):
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
        return Anchor(p=p4_to_p3(np.dot(m, p3_to_p4(self.p))),
                      u=v4_to_v3(np.dot(m, v3_to_v4(self.u))),
                      v=v4_to_v3(np.dot(m, v3_to_v4(self.v))),
                      name=self.name)


class Part(object):
    def __init__(self, shape, name):
        self._shape = shape  # shape in own frame of reference
        self._part_transformation_matrices = []  # 4x4 matrices
        self._name = name

    @property
    def shape(self):
        return self._shape

    @property
    def name(self):
        return self._name

    def add_matrix(self, m):
        self._part_transformation_matrices.append(m)

    @property
    def combined_matrix(self):
        from functools import reduce
        return reduce(np.dot, self._part_transformation_matrices)

    @property
    def transformed_shape(self):

        from OCC.Core.gp import gp_Trsf
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        trsf = gp_Trsf()
        m = self.combined_matrix
        trsf.SetValues(m[0, 0], m[0, 1], m[0, 2], m[0, 3],
                       m[1, 0], m[1, 1], m[1, 2], m[1, 3],
                       m[2, 0], m[2, 1], m[2, 2], m[2, 3])
        transformed = BRepBuilderAPI_Transform(self.shape, trsf)
        return transformed.Shape()


class AnchorablePart(Part):
    def __init__(self, shape, name, anchors):
        super().__init__(shape, name)
        self._anchors = {anchor.name: anchor for anchor in anchors}

    @property
    def anchors(self):
        return self._anchors

    @property
    def transformed(self):
        transformed_shape = self.transformed_shape
        transformed_anchors = [a.transform(self.combined_matrix) for a in self.anchors.values()]
        return AnchorablePart(transformed_shape, self.name, transformed_anchors)


class Assembly(object):
    r"""
    
    Parameters
    ----------
    root_part : AnchorablePart

    """
    def __init__(self, root_part, name):
        self._root_part = root_part
        self._assembly_transformations_matrices = []
        self._parts = []
        self._name = name

    def add_part(self, part_to_add, part_to_add_anchors, receiving_parts, receiving_part_anchors, types_of_links):
        r"""
        
        Parameters
        ----------
        part_to_add : AnchorablePart
        part_to_add_anchors : list
            List of anchors names on part_to_add
        receiving_parts : list
            List of AnchorablePart
        receiving_part_anchors
            List of anchors names on receiving parts
        types_of_links : list
            List of types of links

        Returns
        -------

        """
        assert len(part_to_add_anchors) == len(receiving_parts) == len(receiving_part_anchors) == len(types_of_links)
        if len(part_to_add_anchors) == 1:
            # This is the base case that is already dealt with in osvcad
            m = anchor_transformation(part_to_add.anchors[part_to_add_anchors[0]],
                                      receiving_parts[0].anchors[receiving_part_anchors[0]])
            part_to_add.add_matrix(m)
            self._parts.append(part_to_add)
        else:
            # constraints solver
            # system of equations
            # other ideas ?
            pass


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
    v0 = np.array([anchor_0.p, anchor_0.p + anchor_0.u, anchor_0.p + anchor_0.v])
    v1 = np.array([anchor_1.p, anchor_1.p - anchor_1.u, anchor_1.p + anchor_1.v])

    return superimposition_matrix(v0.T, v1.T, scale=False, usesvd=False)


if __name__ == "__main__":
    print(np.dot(np.array([1, 0, 0]), np.array([0, 1, 0])))
    print(np.cross(np.array([1, 0, 0]), np.array([0, 1, 0])))

    a0 = Anchor(p=(0, 0, 0), u=(1, 0, 0), v=(0, 1, 0), name='a0')
    a1 = Anchor(p=(2, 0, 0), u=(1, 0, 0), v=(0, 0, 1), name='a1')

    m = anchor_transformation(a0, a1)
    print(m)
    print("Det : %f" % np.linalg.det(m))

    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCC.Display.SimpleGui import init_display
    from OCC.Core.gp import gp_Pnt, gp_Vec

    shape_1 = BRepPrimAPI_MakeBox(10, 10, 10).Shape()

    ap1 = AnchorablePart(shape=shape_1,
                         anchors=[Anchor(p=(5, 5, 10),
                                         u=(0, 0, 1),
                                         v=(0, 1, 0),
                                         name='a1')],
                         name='ap1')

    ap2 = AnchorablePart(shape=shape_1,
                         anchors=[Anchor(p=(5, 5, 10),
                                         u=(0, 0, 1),
                                         v=(0, 1, 0),
                                         name='a1')],
                         name='ap2')

    display, start_display, add_menu, add_function_to_menu = init_display()

    # print(ap1.anchors)

    def display_anchorable_part(d, ap, color="YELLOW"):
        d.DisplayColoredShape(ap.shape, color=color)
        print(ap.anchors)
        for anchor_name, anchor in ap.anchors.items():
            print(anchor.p[0])
            d.DisplayVector(pnt=gp_Pnt(float(anchor.p[0]), float(anchor.p[1]), float(anchor.p[2])),
                            vec=gp_Vec(float(anchor.u[0]), float(anchor.u[1]), float(anchor.u[2])))
            d.DisplayVector(pnt=gp_Pnt(float(anchor.p[0]), float(anchor.p[1]), float(anchor.p[2])),
                            vec=gp_Vec(float(anchor.v[0]), float(anchor.v[1]), float(anchor.v[2])))

    display_anchorable_part(display, ap1, color="WHITE")

    a = Assembly(root_part=ap1, name='simple assembly')
    a.add_part(ap2, ['a1'], [ap1], ['a1'], types_of_links=['basic'])

    display_anchorable_part(display, ap2.transformed, color="BLUE")
    # print(ap2._part_transformation_matrices)

    display.FitAll()
    start_display()
