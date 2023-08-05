import numpy as np
cimport numpy as np
cimport cython
from cython cimport parallel
from numpy cimport intp_t, float64_t as f8_t


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline intp_t sign(f8_t x) nogil:
    return (x > 0) - (x < 0)

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void process_particle_cic(
    f8_t[:,:,::1] ret, f8_t px, f8_t py, f8_t pz, f8_t pm, f8_t w,
    f8_t cx, f8_t cy, f8_t cz, f8_t delx,
    intp_t i, intp_t j, intp_t k,
    intp_t[:] mod0, intp_t[:] mod1, intp_t[:] mod2
    ) nogil:

    cdef f8_t dx, dy, dz, tx, ty, tz, xw, yw, zw
    cdef intp_t i0, i1, i2, ii, jj, kk

    cdef f8_t mx, my, mz
    cdef f8_t cell_volume = delx**3
    mx, my, mz = (cx - px)/delx, (cy - py)/delx, (cz - pz)/delx
    cdef intp_t sx, sy, sz
    sx, sy, sz = sign(mx), sign(my), sign(mz)

    dx = sx*mx
    tx = 1-dx
    dy = sy*my
    ty = 1-dy
    dz = sz*mz
    tz = 1-dz

    for ii in range(2):
        i0 = mod0[1+i+ii*sx]
        xw = ii*dx + (1-ii)*tx
        for jj in range(2):
            i1 = mod1[1+j+jj*sy]
            yw = jj*dy + (1-jj)*ty
            for kk in range(2):
                i2 = mod2[1+k+kk*sz]
                zw = kk*dz + (1-kk)*tz
                ret[i0,i1,i2] += pm*w/cell_volume*(xw*yw*zw)

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef cic_particle_density(f8_t[:] px, f8_t[:] py, f8_t[:] pz,
                           intp_t[:] xind, intp_t[:] yind, intp_t[:] zind,
                           weight, f8_t[:] pm, intp_t[:] dds, f8_t[:,:] bbox):

    cdef intp_t nparticles = px.shape[0]
    cdef intp_t i, wind, wshape

    if weight is None:
        wshape = 1
    else:
        wshape = weight.shape[0]

    cdef f8_t[:] _weight
    if wshape == 1:
        _weight = np.ones(wshape)
    else:
        _weight = weight

    cdef intp_t[:] mod0 = np.mod(np.arange(dds[0]+2)-1, dds[0])
    cdef intp_t[:] mod1 = np.mod(np.arange(dds[1]+2)-1, dds[1])
    cdef intp_t[:] mod2 = np.mod(np.arange(dds[2]+2)-1, dds[2])

    cdef f8_t dx = (bbox[0,1] - bbox[0,0])/<f8_t>dds[0]

    cdef f8_t[:,:,::1] ret = np.zeros(dds)
    cdef f8_t cx, cy, cz, w

    with nogil:
        for i in parallel.prange(nparticles):
            cx = bbox[0,0]+(<f8_t>xind[i]+0.5)*dx
            cy = bbox[1,0]+(<f8_t>yind[i]+0.5)*dx
            cz = bbox[2,0]+(<f8_t>zind[i]+0.5)*dx
            if wshape == 1:
                wind = 0
            else:
                wind = i
            process_particle_cic(ret, px[i], py[i], pz[i], pm[i], _weight[wind],
                                 cx, cy, cz, dx, xind[i], yind[i], zind[i],
                                 mod0, mod1, mod2)
    return np.asarray(ret)
