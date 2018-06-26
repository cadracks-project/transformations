import math

import numpy

from transformations.transformations import identity_matrix, rotation_matrix, \
    concatenate_matrices, euler_from_matrix, euler_matrix, is_same_transform, \
    quaternion_about_axis, quaternion_multiply, quaternion_matrix, \
    scale_matrix, translation_matrix, shear_matrix, random_rotation_matrix, \
    decompose_matrix, random_vector, unit_vector, vector_product, \
    compose_matrix, angle_between_vectors

alpha, beta, gamma = 0.123, -1.234, 2.345
origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
I = identity_matrix()
Rx = rotation_matrix(alpha, xaxis)
Ry = rotation_matrix(beta, yaxis)
Rz = rotation_matrix(gamma, zaxis)
R = concatenate_matrices(Rx, Ry, Rz)
euler = euler_from_matrix(R, 'rxyz')
print(numpy.allclose([alpha, beta, gamma], euler))

Re = euler_matrix(alpha, beta, gamma, 'rxyz')
print(is_same_transform(R, Re))

al, be, ga = euler_from_matrix(Re, 'rxyz')
print(is_same_transform(Re, euler_matrix(al, be, ga, 'rxyz')))

qx = quaternion_about_axis(alpha, xaxis)
qy = quaternion_about_axis(beta, yaxis)
qz = quaternion_about_axis(gamma, zaxis)
q = quaternion_multiply(qx, qy)
q = quaternion_multiply(q, qz)
Rq = quaternion_matrix(q)
print(is_same_transform(R, Rq))

S = scale_matrix(1.23, origin)
T = translation_matrix([1, 2, 3])
Z = shear_matrix(beta, xaxis, origin, zaxis)
R = random_rotation_matrix(numpy.random.rand(3))
M = concatenate_matrices(T, R, Z, S)
scale, shear, angles, trans, persp = decompose_matrix(M)
print(numpy.allclose(scale, 1.23))

print(numpy.allclose(trans, [1, 2, 3]))

print(numpy.allclose(shear, [0, math.tan(beta), 0]))

print(is_same_transform(R, euler_matrix(axes='sxyz', *angles)))

M1 = compose_matrix(scale, shear, angles, trans, persp)
print(is_same_transform(M, M1))

v0, v1 = random_vector(3), random_vector(3)
M = rotation_matrix(angle_between_vectors(v0, v1), vector_product(v0, v1))
v2 = numpy.dot(v0, M[:3,:3].T)
print(numpy.allclose(unit_vector(v1), unit_vector(v2)))
