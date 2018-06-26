from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display
from transformations.display import display_anchorable_part
from transformations.links import Link
from transformations.model import AnchorablePart, Assembly, Anchor

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
                                     name='t2'),
                              Anchor(p=(5, 5, 0),
                                     u=(0, 0, -1),
                                     v=(0, 1, 0),
                                     name='b2')
                              ],
                     name='ap2')

ap3 = AnchorablePart(shape=shape_1,
                     anchors=[Anchor(p=(5, 5, 10),
                                     u=(0, 0, 1),
                                     v=(0, 1, 0),
                                     name='a3')],
                     name='ap3')

display, start_display, add_menu, add_function_to_menu = init_display()

# print(ap1.anchors)

a = Assembly(root_part=ap1, name='simple assembly')

a.add_part(part_to_add=ap2,
           part_to_add_anchors=['t2'],
           receiving_parts=[ap1],
           receiving_parts_anchors=['a1'],
           links=[Link(anchor=ap1.anchors['a1'],
                       tx=-3,
                       ty=0,
                       tz=0,
                       rx=0.2,
                       ry=0.2,
                       rz=0.2)])
a.add_part(part_to_add=ap3,
           part_to_add_anchors=['a3'],
           receiving_parts=[ap2],
           receiving_parts_anchors=['b2'],
           links=[Link(anchor=ap2.anchors['b2'], tx=1)])

display_anchorable_part(display, ap1.transformed, color="YELLOW")
display_anchorable_part(display, ap2.transformed, color="BLUE")
display_anchorable_part(display, ap3.transformed, color="RED")
# print(ap2._part_transformation_matrices)

display.FitAll()
start_display()