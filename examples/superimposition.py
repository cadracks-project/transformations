import numpy as np
from numpy.linalg import det

from transformations.transformations import superimposition_matrix, \
    decompose_matrix

# v0 = np.random.rand(3, 10)
# print(v0)
# M = superimposition_matrix(v0, v0)
# print(np.allclose(M, np.identity(4)))
#
# v0 = [[0, 0, 0, 1], [1, 0, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1]]
# v1 = [[1, 0, 0, 1], [2, 0, 0, 1], [1, 0, 1, 1], [2, 1, 1, 1]]

v0 = [[0, 1, 0, 1],  # xs
      [0, 0, 0, 1],  # ys
      [0, 0, 1, 1]]  # zs

v1 = [[1, 2, 1, 2],  # xs
      [0, 0, 0, 1],  # ys
      [0, 0, 1, 1]]  # zs

# M = superimposition_matrix(v0, v0)
# print(M)

m = superimposition_matrix(v0, v1, scale=False, usesvd=True)
print(m)

m = superimposition_matrix(v0, v1, scale=False, usesvd=False)
print(m)
# m = superimposition_matrix(v0, v1, scale=False, usesvd=True)
# print(m)
print("  Det : %.6f" % det(m))
print("scale, shear, angles, translate, perspective")
print(decompose_matrix(m))
print(np.dot(m, [0, 0, 0, 1]))
