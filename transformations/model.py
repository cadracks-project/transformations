# coding: utf-8

r"""?"""

# TODO : transform around the anchor
#          -> should generate another matrix stored on the part
#             or on the assembly
#             (since assemblies can be put together with anchors)
#        transform an assembly

import numpy as np

from anchors import Anchor, anchor_transformation


class Part(object):
    r"""A Part is the simplest possible element
    
    Parameters
    ----------
    shape : OCC shape
    name : str
    
    """
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
        r"""Add a 4x4 transformation matrix to the list of transformation
        matrices"""
        assert np.shape(m) == (4, 4)
        self._part_transformation_matrices.append(m)

    @property
    def combined_matrix(self):
        r"""Combine all transformation matrices into a single matrix that
        can be used to place the part in its final location"""
        from functools import reduce
        return reduce(np.dot, self._part_transformation_matrices)

    @property
    def transformed_shape(self):
        r"""The shape of the part, placed in its final location
        
        Returns
        -------
        an OCC shape, in its final location

        """
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
    r"""An AnchorablePart represents the combination of a Part and its Anchors
    
    Parameters
    ----------
    shape : OCC shape
    anchors : list of Anchors

    """
    def __init__(self, shape, name, anchors):
        super().__init__(shape, name)
        self._anchors = {anchor.name: anchor for anchor in anchors}

    @property
    def anchors(self):
        return self._anchors

    @property
    def transformed(self):
        r"""
        
        Returns
        -------
        A new AnchorablePart, placed in its final location

        """
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

    def add_part(self,
                 part_to_add,
                 part_to_add_anchors,
                 receiving_parts,
                 receiving_part_anchors,
                 links):
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
        links : list[Link]
            List of links applied in the same order as the anchors

        Returns
        -------

        """
        assert len(part_to_add_anchors) == len(receiving_parts) == len(receiving_part_anchors) == len(links)
        if len(part_to_add_anchors) == 1:
            # This is the base case that is already dealt with in osvcad
            m = anchor_transformation(part_to_add.anchors[part_to_add_anchors[0]],
                                      receiving_parts[0].anchors[receiving_part_anchors[0]])
            part_to_add.add_matrix(m)
            for link in links:
                part_to_add.add_matrix(link.transformation_matrix)
            self._parts.append(part_to_add)
        else:
            # constraints solver
            # system of equations
            # other ideas ?
            pass


if __name__ == "__main__":

    # a0 = Anchor(p=(0, 0, 0), u=(1, 0, 0), v=(0, 1, 0), name='a0')
    # a1 = Anchor(p=(2, 0, 0), u=(1, 0, 0), v=(0, 0, 1), name='a1')
    #
    # m = anchor_transformation(a0, a1)
    # print(m)
    # print("Det : %f" % np.linalg.det(m))

    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCC.Display.SimpleGui import init_display
    from display import display_anchorable_part

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

    display_anchorable_part(display, ap1, color="WHITE")

    a = Assembly(root_part=ap1, name='simple assembly')
    from links import Link

    a.add_part(ap2, ['a1'], [ap1], ['a1'], links=[Link(anchor=ap1.anchors['a1'],
                                                       tx=-3,
                                                       ty=0,
                                                       tz=0,
                                                       rx=0.2,
                                                       ry=0.2,
                                                       rz=0.2)])

    display_anchorable_part(display, ap2.transformed, color="BLUE")
    # print(ap2._part_transformation_matrices)

    display.FitAll()
    start_display()
