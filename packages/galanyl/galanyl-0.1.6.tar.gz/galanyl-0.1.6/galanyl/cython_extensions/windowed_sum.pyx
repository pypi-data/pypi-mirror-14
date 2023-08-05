import numpy as np
cimport numpy as np
cimport cython
from cython cimport parallel
from numpy cimport intp_t, float64_t as f8_t

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
cdef inline void process_cell(f8_t* Dptr, f8_t* Aptr, intp_t index,
                              intp_t* m0ptr, intp_t* m1ptr, intp_t* m2ptr,
                              intp_t size, intp_t* s) nogil:

    cdef intp_t i, j, k, ii, jj, kk, mi, mj
    i = index/s[2]/s[1] % s[0]
    j = index/s[2] % s[1]
    k = index % s[2]
    Dptr[index] = 0
    for ii in range(size):
        mi = m0ptr[i+ii]*s[1]
        for jj in range(size):
            mj = (mi + m1ptr[j+jj])*s[2]
            for kk in range(size):
                Dptr[index] += Aptr[mj + m2ptr[k+kk]]

@cython.cdivision(True)
@cython.wraparound(False)
@cython.boundscheck(False)
def windowed_sum(f8_t[:,:,::1] arr, intp_t size):

    cdef intp_t* s = [arr.shape[0], arr.shape[1], arr.shape[2]]

    cdef f8_t[:,:,::1] D = np.empty((s[0], s[1], s[2]))
    cdef intp_t[:] m0 = np.mod(np.arange(s[0]+2*size/2)-1, s[0])
    cdef intp_t[:] m1 = np.mod(np.arange(s[1]+2*size/2)-1, s[1])
    cdef intp_t[:] m2 = np.mod(np.arange(s[2]+2*size/2)-1, s[2])

    cdef f8_t* Dptr = &D[0,0,0]
    cdef f8_t* Aptr = &arr[0,0,0]
    cdef intp_t* m0ptr = &m0[0]
    cdef intp_t* m1ptr = &m1[0]
    cdef intp_t* m2ptr = &m2[0]

    cdef intp_t i
    cdef intp_t ncells = s[0]*s[1]*s[2]
    with nogil:
        for i in parallel.prange(ncells):
            process_cell(Dptr, Aptr, i, m0ptr, m1ptr, m2ptr, size, s)

    return np.asarray(D)
