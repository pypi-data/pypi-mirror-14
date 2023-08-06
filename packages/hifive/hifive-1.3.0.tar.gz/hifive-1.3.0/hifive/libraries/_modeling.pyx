# distutils: language = c++

"""These functions provide increased speed in handling functions dealing with
3D modeling of HiC data using HiFive.
"""

import cython
cimport numpy as np
import numpy

ctypedef np.float32_t DTYPE_t
ctypedef np.float64_t DTYPE_64_t
ctypedef np.int32_t DTYPE_int_t
ctypedef np.int64_t DTYPE_int64_t
ctypedef np.uint32_t DTYPE_uint_t
ctypedef np.int8_t DTYPE_int8_t
cdef double Inf = numpy.inf

cdef extern from "math.h":
    double exp(double x) nogil
    double log(double x) nogil
    double log10(double x) nogil
    double sqrt(double x) nogil
    double pow(double x, double x) nogil
    double abs(double x) nogil
    double round(double x) nogil
    double floor(double x) nogil
    double ceil(double x) nogil


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def find_distances(
        np.ndarray[DTYPE_t, ndim=2] coords not None,
        np.ndarray[DTYPE_t, ndim=1] distances not None):
    cdef long long int i, j, k, pos
    cdef double value
    cdef long long int num_coords = coords.shape[0]
    cdef long long int num_parameters = coords.shape[1]
    with nogil:
        pos = 0
        for i in range(num_coords - 1):
            for j in range(i + 1, num_coords):
                value = 0.0
                for k in range(num_parameters):
                    value += pow(coords[i, k] - coords[j, k], 2.0)
                distances[pos] = pow(value, 0.5)
                pos += 1
    return None

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def find_poisson_cost(
        np.ndarray[DTYPE_int_t, ndim=1] zero_indices not None,
        np.ndarray[DTYPE_t, ndim=1] zero_weights not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_indices not None,
        np.ndarray[DTYPE_t, ndim=1] nonzero_weights not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_counts not None,
        np.ndarray[DTYPE_t, ndim=1] nonzero_log_distances not None,
        np.ndarray[DTYPE_t, ndim=1] distances not None,
        double alpha,
        double beta):
    cdef long long int i
    cdef double cost
    cdef long long int num_zero = zero_indices.shape[0]
    cdef long long int num_nonzero = nonzero_indices.shape[0]
    cdef double log_beta = log(beta)
    with nogil:
        cost = 0.0
        for i in range(num_zero):
            cost -= beta * zero_weights[i] * pow(distances[zero_indices[i]], alpha)
        for i in range(num_nonzero):
            cost += nonzero_counts[i] * (alpha * nonzero_log_distances[i] + log_beta) - beta * nonzero_weights[i] * pow(distances[nonzero_indices[i]], alpha)
    return cost

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def calculate_poisson_param_gradients(
        np.ndarray[DTYPE_int_t, ndim=1] zero_indices not None,
        np.ndarray[DTYPE_t, ndim=1] zero_weights not None,
        np.ndarray[DTYPE_t, ndim=1] zero_log_distances not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_indices not None,
        np.ndarray[DTYPE_t, ndim=1] nonzero_weights not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_counts not None,
        np.ndarray[DTYPE_t, ndim=1] nonzero_log_distances not None,
        np.ndarray[DTYPE_t, ndim=1] distances not None,
        np.ndarray[DTYPE_64_t, ndim=1] grads not None,
        double alpha,
        double beta):
    cdef long long int i
    cdef double bd_alpha, value
    cdef long long int num_zero = zero_indices.shape[0]
    cdef long long int num_nonzero = nonzero_indices.shape[0]
    with nogil:
        for i in range(num_zero):
            bd_alpha = zero_weights[i] * pow(distances[zero_indices[i]], alpha)
            value = -beta * bd_alpha * zero_log_distances[i]
            grads[0] -= value
            grads[1] += bd_alpha
        for i in range(num_nonzero):
            bd_alpha = nonzero_weights[i] * pow(distances[nonzero_indices[i]], alpha)
            value = (nonzero_counts[i] - beta * bd_alpha) * nonzero_log_distances[i]
            grads[0] += value
            value = nonzero_counts[i] / beta - bd_alpha
            grads[1] += value
    return None

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def calculate_poisson_coord_gradients(
        np.ndarray[DTYPE_int_t, ndim=1] zero_indices not None,
        np.ndarray[DTYPE_int_t, ndim=1] zero_indices0 not None,
        np.ndarray[DTYPE_int_t, ndim=1] zero_indices1 not None,
        np.ndarray[DTYPE_t, ndim=1] zero_weights not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_indices not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_indices0 not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_indices1 not None,
        np.ndarray[DTYPE_t, ndim=1] nonzero_weights not None,
        np.ndarray[DTYPE_int_t, ndim=1] nonzero_counts not None,
        np.ndarray[DTYPE_t, ndim=1] distances not None,
        np.ndarray[DTYPE_t, ndim=2] coords not None,
        np.ndarray[DTYPE_64_t, ndim=2] grads not None,
        double alpha,
        double beta):
    cdef long long int i, j, index0, index1
    cdef double distance, value, value2
    cdef long long int num_zero = zero_indices.shape[0]
    cdef long long int num_nonzero = nonzero_indices.shape[0]
    with nogil:
        for i in range(num_zero):
            distance = distances[zero_indices[i]]
            value = -alpha * beta * zero_weights[i] * pow(distance, alpha) / (distance * distance)
            index0 = zero_indices0[i]
            index1 = zero_indices1[i]
            for j in range(3):
                value2 = value * (coords[index0, j] - coords[index1, j])
                grads[index0, j] -= value2
                grads[index1, j] += value2
        for i in range(num_nonzero):
            distance = distances[nonzero_indices[i]]
            value = alpha * (nonzero_counts[i] - beta * nonzero_weights[i] * pow(distance, alpha)) / (distance * distance)
            index0 = nonzero_indices0[i]
            index1 = nonzero_indices1[i]
            for j in range(3):
                value2 = value * (coords[index0, j] - coords[index1, j])
                grads[index0, j] -= value2
                grads[index1, j] += value2
    return None










