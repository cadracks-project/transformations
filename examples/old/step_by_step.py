import numpy as np
from numpy.linalg import det

from transformations.transformations import identity_matrix, \
    translation_matrix, translation_from_matrix, reflection_matrix, \
    reflection_from_matrix, rotation_matrix, rotation_from_matrix, \
    scale_matrix, scale_from_matrix, projection_matrix, \
    projection_from_matrix, shear_matrix, shear_from_matrix, decompose_matrix

print("---- Identity matrix ----")
print(identity_matrix())

print("---- Translation matrix ----")
tm = translation_matrix((10, 20, 30))
print(tm)
print("  Det : %.6f" % det(tm))
print("Trace : %.6f" % np.trace(tm))
print(translation_matrix([10, 20, 30]))
print(translation_matrix(np.array([10, 20, 30])))
print("---- Translation from matrix ----")
print(translation_from_matrix(tm))

print("---- Reflection matrix ----")
reflect_m = reflection_matrix((0, 0, 0), (0, 0, 1))
print(reflect_m)
print("  Det : %.6f" % det(reflect_m))
print("Trace : %.6f" % np.trace(reflect_m))
print("---- Reflection from matrix ----")
print(reflection_from_matrix(reflect_m))

print("---- Rotation matrix ----")
rot_m = rotation_matrix(np.pi / 2, direction=(0, 0, 1), point=(10, 0, 0))
print(rot_m)
print("  Det : %.6f" % det(rot_m))
print("Trace : %.6f" % np.trace(rot_m))
print("---- Rotation from matrix ----")
print(rotation_from_matrix(rot_m))

print("---- Scale matrix ----")
scale_m = scale_matrix(factor=3, origin=(0, 0, 0), direction=(1, 1, 1))
print(scale_m)
print("  Det : %.6f" % det(scale_m))
print("Trace : %.6f" % np.trace(scale_m))
print("---- Scale from matrix ----")
print(scale_from_matrix(scale_m))

print("---- Projection matrix ----")
proj_m = projection_matrix(point=(1, 0, 0), normal=(0, 0, 1))
print(proj_m)
print("  Det : %.6f" % det(proj_m))
print("Trace : %.6f" % np.trace(proj_m))
print("---- Projection from matrix ----")
print(projection_from_matrix(proj_m))

print("---- Shear matrix ----")
shear_m = shear_matrix(angle=0.1, direction=(1, 0, 0), point=(0, 0, 0), normal=(0, 0, 1))
print(shear_m)
print("  Det : %.6f" % det(shear_m))
print("Trace : %.6f" % np.trace(shear_m))
print("---- Shear from matrix ----")
print(shear_from_matrix(shear_m))

print("---- Decompose matrix ----")
m = np.dot(rot_m, tm)
scale, shear, angles, translate, perspective = decompose_matrix(m)
print("scale:")
print(scale)
print("shear:")
print(shear)
print("angles:")
print(angles)
print("translate:")
print(translate)
print("perspective:")
print(perspective)
