# coding: utf-8

r"""Display functions"""

from OCC.Core.gp import gp_Pnt, gp_Vec


def display_anchorable_part(d, ap, color="YELLOW"):
    r"""
    
    Parameters
    ----------
    d
    ap
    color

    """
    d.DisplayColoredShape(ap.shape, color=color)
    print(ap.anchors)
    for anchor_name, anchor in ap.anchors.items():
        print(anchor.p[0])
        d.DisplayVector(pnt=gp_Pnt(float(anchor.p[0]), float(anchor.p[1]),
                                   float(anchor.p[2])),
                        vec=gp_Vec(float(anchor.u[0]), float(anchor.u[1]),
                                   float(anchor.u[2])))
        d.DisplayVector(pnt=gp_Pnt(float(anchor.p[0]), float(anchor.p[1]),
                                   float(anchor.p[2])),
                        vec=gp_Vec(float(anchor.v[0]), float(anchor.v[1]),
                                   float(anchor.v[2])))