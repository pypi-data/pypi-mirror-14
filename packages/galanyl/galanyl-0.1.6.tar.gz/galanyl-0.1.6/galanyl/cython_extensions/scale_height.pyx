import numpy as np
cimport numpy as np
cimport cython
from cython cimport parallel
from numpy cimport intp_t, float64_t as f8_t


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef scale_height(np.ndarray[f8_t, ndim=1] x, np.ndarray[f8_t, ndim=3] y):
    """calculates a 2D scale height map given a 3D array of density values


    Parameters
    ----------
    x : 1-D ndarray (double type)
        Array containg the x (abcissa) values. Must be monotonically
        increasing.
    y : 3-D ndarray (double type)
        Array containing the density values.

    Returns
    -------
    new_y : 3-D ndarray
        Interpolated values.

    """
    cdef intp_t nx = y.shape[0]
    cdef intp_t ny = y.shape[1]
    cdef intp_t nz = y.shape[2]
    cdef intp_t xyindex
    cdef np.ndarray[f8_t, ndim=2] new_y = np.zeros((nx, ny), dtype='f8')

    cdef f8_t* xptr = &x[0]
    cdef f8_t* yptr = &y[0, 0, 0]
    cdef f8_t* new_yptr = &new_y[0, 0]
    cdef f8_t e = np.e

    with nogil:
        for xyindex in parallel.prange(nx*ny):
            process_scale_height_pencil(
                xyindex, e, xptr, yptr, new_yptr, nx, ny, nz)

    return new_y

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef void process_scale_height_pencil(intp_t xyindex, f8_t e,
                                      f8_t* xptr, f8_t* yptr, f8_t* new_yptr,
                                      intp_t nx, intp_t ny, intp_t nz) nogil:

    cdef f8_t bot, top, mid, x0, x1, y0, y1, yi, totsum, bottomsum
    cdef intp_t i, j, k

    bottomsum = 0
    totsum = 0
    bot = 0
    top = 0
    mid = 0

    i = (xyindex / ny) % nx
    j = xyindex % ny
    for k in range(nz):
        xyzindex = (i*ny + j)*nz + k
        totsum += yptr[xyzindex]
    if totsum == 0:
        new_yptr[xyindex] = 0
        return
    for k in range(nz):
        xyzindex = (i*ny + j)*nz + k
        x0 = xptr[k]
        x1 = xptr[k+1]
        y0 = bottomsum
        y1 = bottomsum + yptr[xyzindex]
        bottomsum += yptr[xyzindex]
        if bottomsum/(totsum/2.) > (1./e) and bot == 0:
            yi = (1./e)*totsum/2.
            bot = x0 + (x1 - x0)*(yi - y0)/(y1 - y0)
        if bottomsum/totsum > 0.5 and mid == 0:
            yi = (0.5)*totsum
            mid = x0 + (x1 - x0)*(yi - y0)/(y1 - y0)
        if bottomsum/(totsum/2.) > (2.0 - 1./e):
            # It's 2.0 - 1/e since we've counted a full half-slab plus
            # 1.0 - 1/e of another half-slab
            yi = (2.0 - 1./e)*totsum/2.
            top = x0 + (x1 - x0)*(yi - y0)/(y1 - y0)
            break
    bot = mid - bot
    top = top - mid
    new_yptr[xyindex] = (top + bot)/2.0
    return
