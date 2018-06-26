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
                                     name='top1'),
                              Anchor(p=(5, 5, 0),
                                     u=(0, 0, -1),
                                     v=(0, 1, 0),
                                     name='bottom1')],
                     name='ap1')

ap2 = AnchorablePart(shape=shape_1,
                     anchors=[Anchor(p=(5, 5, 10),
                                     u=(0, 0, 1),
                                     v=(0, 1, 0),
                                     name='top2'),
                              Anchor(p=(5, 5, 0),
                                     u=(0, 0, -1),
                                     v=(0, 1, 0),
                                     name='bottom2')],
                     name='ap2')

ap3 = AnchorablePart(shape=shape_1,
                     anchors=[Anchor(p=(5, 5, 10),
                                     u=(0, 0, 1),
                                     v=(0, 1, 0),
                                     name='top3'),
                              Anchor(p=(5, 5, 0),
                                     u=(0, 0, -1),
                                     v=(0, 1, 0),
                                     name='bottom3')],
                     name='ap3')

ap4 = AnchorablePart(shape=shape_1,
                     anchors=[Anchor(p=(5, 5, 10),
                                     u=(0, 0, 1),
                                     v=(0, 1, 0),
                                     name='top4'),
                              Anchor(p=(5, 5, 0),
                                     u=(0, 0, -1),
                                     v=(0, 1, 0),
                                     name='bottom4')],
                     name='ap4')

display, start_display, add_menu, add_function_to_menu = init_display()

# print(ap1.anchors)

# display_anchorable_part(display, ap1, color="RED")

a = Assembly(root_part=ap1, name='a')
a.add_part(part_to_add=ap2,
           part_to_add_anchors=['top2'],
           receiving_parts=[ap1],
           receiving_parts_anchors=['top1'],
           links=[Link(anchor=ap1.anchors['top1'],
                       tx=-1.,
                       rx=0.2,
                       ry=0.2,
                       rz=0.)])
print("assembly a has %i parts and %i anchors" % (len(a._parts), len(a.anchors)))

b = Assembly(root_part=ap3, name='b')
b.add_part(part_to_add=ap4,
           part_to_add_anchors=['top4'],
           receiving_parts=[ap3],
           receiving_parts_anchors=['top3'],
           links=[Link(anchor=ap3.anchors['top3'],
                       tx=-1,
                       rx=0,
                       ry=0,
                       rz=0)])
print("assembly b has %i parts and %i anchors" % (len(b._parts), len(b.anchors)))


before = False

if before:
    for part in a._parts:
        display_anchorable_part(display, part.transformed, color="RED")

    for part in b._parts:
        display_anchorable_part(display, part.transformed, color="BLUE")
else:
    Assembly.add_assembly(assembly_to_add=b,
                          assembly_to_add_anchors=['bottom3'],
                          receiving_assemblies=[a],
                          receiving_assemblies_anchors=['bottom2'],
                          links=[Link(anchor=a.anchors['bottom2'],
                                 tx=1,
                                 rx=0.7,
                                 ry=1,
                                 rz=0)])
    print("-- A --")
    for part in a._parts:
        print(part.name)
        print(part._part_transformation_matrices)
        display_anchorable_part(display, part.transformed, color="RED")

    print("-- B --")
    for part in b._parts:
        print(part.name)
        print(part._part_transformation_matrices)
        display_anchorable_part(display, part.transformed, color="BLUE")


display.FitAll()
start_display()