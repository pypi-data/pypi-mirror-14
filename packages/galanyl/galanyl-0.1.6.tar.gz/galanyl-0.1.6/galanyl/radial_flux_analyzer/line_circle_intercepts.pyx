cimport cython
from libc.math cimport sqrt, copysign, abs

@cython.cdivision(True)
def get_line_circle_intercepts(double x1, double x2, double y1, double y2, double r):
    """Finds the 2D coordinates of the collisions between a line and circle.
    
    Input parameters:
        x1 - float
            x coordinate of initial point
        x2 - float
            x coordinate of final point
        y1 - float
            y coordinate of initial point
        y2 - float
            y coordinate of final point
        r - float
            radius of the circle
            
    See: http://mathworld.wolfram.com/Circle-LineIntersection.html
    """
    cdef double d_x = x2 - x1
    cdef double d_y = y2 - y1
    cdef double d_r = sqrt(d_x*d_x + d_y*d_y)
    cdef double D = x1*y2 - x2*y1
    
    if r*r*d_r*d_r < D*D:
        return None
    
    if r*r*d_r*d_r == D*D:
        raise NotImplementedError
    
    if d_y == 0:
        s = 1
    else:
        s = copysign(1, d_y)
    
    if x1==x2:
        yint = (-D*d_x + abs(d_y)*sqrt(r**2*d_r**2 - D**2))/d_r**2
        xint = x1
        return [(xint, yint), (xint, -yint)]
    else:
        xint = (D*d_y + d_x*s*sqrt(r**2*d_r**2 - D**2))/d_r**2
        yint = y1
        return [(xint, yint), (-xint, yint)]
