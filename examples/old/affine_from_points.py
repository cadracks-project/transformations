import numpy as np
from numpy.linalg import det

from transformations.transformations import affine_matrix_from_points, decompose_matrix

v0 = [[0, 1, 0, 1],  # xs
      [0, 0, 0, 1],  # ys
      [0, 0, 1, 1]]  # zs

v1 = [[1, 2, 1, 2],  # xs
      [0, 0, 0, 1],  # ys
      [0, 0, 1, 1]]  # zs

m = affine_matrix_from_points(v0, v1, shear=False, scale=False, usesvd=True)
print(m)

m = affine_matrix_from_points(v0, v1, shear=False, scale=False, usesvd=False)
print(m)

print("  Det : %.6f" % det(m))
print("scale, shear, angles, translate, perspective")
print(decompose_matrix(m))
print(np.dot(m, [0, 0, 0, 1]))