# coding: utf-8

r"""?"""

# TODO : potential anchor names duplicates problem
#        add_assembly should not be static and an assembly should manage a list of contained assemblies

import numpy as np

from transformations.anchors import Anchor, anchor_transformation
from transformations.transformations import identity_matrix


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
        # self._part_transformation_matrices = [m] + self._part_transformation_matrices

    @property
    def combined_matrix(self):
        r"""Combine all transformation matrices into a single matrix that
        can be used to place the part in its final location"""
        from functools import reduce
        if self._part_transformation_matrices:
            return reduce(np.dot, self._part_transformation_matrices)
        else:
            return identity_matrix()

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
        self._parts.append(root_part)
        self._name = name

    def add_part(self,
                 part_to_add,
                 part_to_add_anchors,
                 receiving_parts,
                 receiving_parts_anchors,
                 links):
        r"""
        
        Parameters
        ----------
        part_to_add : AnchorablePart
        part_to_add_anchors : list
            List of anchors names on part_to_add
        receiving_parts : list
            List of AnchorablePart
        receiving_parts_anchors
            List of anchors names on receiving parts
        links : list[Link]
            List of links applied in the same order as the anchors

        Returns
        -------

        """
        assert len(part_to_add_anchors) == len(receiving_parts) == len(receiving_parts_anchors) == len(links)
        if len(part_to_add_anchors) == 1:
            # This is the base case that is already dealt with in osvcad
            m = anchor_transformation(part_to_add.transformed.anchors[part_to_add_anchors[0]],
                                      receiving_parts[0].transformed.anchors[receiving_parts_anchors[0]])
            part_to_add.add_matrix(m)
            part_to_add.add_matrix(links[0].transformation_matrix)
            self._parts.append(part_to_add)
        else:
            # constraints solver
            # system of equations
            # other ideas ?
            raise NotImplementedError

    @staticmethod
    def add_assembly(assembly_to_add,
                     assembly_to_add_anchors,
                     receiving_assemblies,
                     receiving_assemblies_anchors,
                     links):
        assert len(assembly_to_add_anchors) == len(receiving_assemblies) == len(receiving_assemblies_anchors) == len(links)
        if len(assembly_to_add_anchors) == 1:
            m = anchor_transformation(assembly_to_add.anchors[assembly_to_add_anchors[0]],
                                      receiving_assemblies[0].anchors[receiving_assemblies_anchors[0]])
            for part in assembly_to_add._parts:
                # part.add_matrix(m)
                part._part_transformation_matrices = [m] + part._part_transformation_matrices
                # part.add_matrix(links[0].transformation_matrix)
                part._part_transformation_matrices = [links[0].transformation_matrix] + part._part_transformation_matrices
        else:
            raise NotImplementedError

    @property
    def anchors(self):
        anchors = {}
        for part in self._parts:
            for k, v in part.transformed.anchors.items():
                anchors[k] = v
        return anchors
