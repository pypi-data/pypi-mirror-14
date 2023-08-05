import numpy as np
cimport numpy as np
cimport cython
from cython cimport parallel
from libc.math cimport sqrt, isnan
from numpy cimport intp_t, float64_t as f8_t


@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline void process_particle(f8_t* s0, f8_t* s1, f8_t* s2, intp_t ind,
                                  f8_t v, f8_t m, intp_t* m0ptr, intp_t* m1ptr,
                                  intp_t* m2ptr, intp_t size, intp_t* s) nogil:

    cdef intp_t i, j, k, ii, jj, kk, mi, mj, index
    i = ind/s[2]/s[1] % s[0]
    j = ind/s[2] % s[1]
    k = ind % s[2]
    for ii in range(size):
        mi = m0ptr[i+ii]*s[1]
        for jj in range(size):
            mj = (mi + m1ptr[j+jj])*s[2]
            for kk in range(size):
                index = mj + m2ptr[k+kk]
                s0[index] += m
                s1[index] += m*v
                s2[index] += m*v*v

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef void reduce_dispersion(f8_t* ret, f8_t* s0, f8_t* s1, f8_t* s2,
                            intp_t* indices, f8_t* v, f8_t* m, intp_t nparticles,
                            intp_t size, intp_t* s, intp_t* m0ptr,
                            intp_t* m1ptr, intp_t* m2ptr) nogil:

    cdef intp_t i

    for i in parallel.prange(nparticles):
        process_particle(s0, s1, s2, indices[i], v[i], m[i],
                         m0ptr, m1ptr, m2ptr, size, s)

    for i in parallel.prange(s[0]*s[1]*s[2]):
        if s0[i] == 0:
            ret[i] = 0
        else:
            ret[i] = sqrt(s0[i]*s2[i] - s1[i]*s1[i])/s0[i]
        if isnan(ret[i]):
            ret[i] = 0

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cpdef tuple particle_dispersion(f8_t[:] velx, f8_t[:] vely, f8_t[:] velz,
                                f8_t[:] pmass, intp_t[:] indices,
                                intp_t[:] shape, intp_t size):
    cdef intp_t i, ncells, ind

    cdef intp_t* s = [shape[0], shape[1], shape[2]]
    ncells = s[0]*s[1]*s[2]

    cdef intp_t nparticles = velx.shape[0]

    cdef f8_t[:, :, ::1] sum0 = np.zeros((s[0], s[1], s[2]))
    cdef f8_t[:, :, ::1] sum1 = np.zeros((s[0], s[1], s[2]))
    cdef f8_t[:, :, ::1] sum2 = np.zeros((s[0], s[1], s[2]))
    cdef f8_t[:, :, ::1] sigma_x = np.empty((s[0], s[1], s[2]))
    cdef f8_t[:, :, ::1] sigma_y = np.empty((s[0], s[1], s[2]))
    cdef f8_t[:, :, ::1] sigma_z = np.empty((s[0], s[1], s[2]))
    cdef intp_t[:] m0 = np.mod(np.arange(s[0]+2*size/2)-1, s[0])
    cdef intp_t[:] m1 = np.mod(np.arange(s[1]+2*size/2)-1, s[1])
    cdef intp_t[:] m2 = np.mod(np.arange(s[2]+2*size/2)-1, s[2])

    cdef f8_t* s0 = &sum0[0, 0, 0]
    cdef f8_t* s1 = &sum1[0, 0, 0]
    cdef f8_t* s2 = &sum2[0, 0, 0]
    cdef f8_t* vx = &velx[0]
    cdef f8_t* vy = &vely[0]
    cdef f8_t* vz = &velz[0]
    cdef f8_t* m = &pmass[0]
    cdef intp_t* m0ptr = &m0[0]
    cdef intp_t* m1ptr = &m1[0]
    cdef intp_t* m2ptr = &m2[0]
    cdef intp_t* inds = &indices[0]

    with nogil:
        reduce_dispersion(&sigma_x[0, 0, 0], s0, s1, s2, inds, vx, m, nparticles, size, s,
                          m0ptr, m1ptr, m2ptr)
        reduce_dispersion(&sigma_y[0, 0, 0], s0, s1, s2, inds, vy, m, nparticles, size, s,
                          m0ptr, m1ptr, m2ptr)
        reduce_dispersion(&sigma_z[0, 0, 0], s0, s1, s2, inds, vz, m, nparticles, size, s,
                          m0ptr, m1ptr, m2ptr)

    return (np.asarray(sigma_x), np.asarray(sigma_y), np.asarray(sigma_z))
