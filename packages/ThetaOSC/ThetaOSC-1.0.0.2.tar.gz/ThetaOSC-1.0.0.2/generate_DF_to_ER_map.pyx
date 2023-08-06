# import pyximport
# pyximport.install(pyimport = True)
"""
generate mapping from 2 fisheyes to equirectangular
"""

import numpy
#from numpy import cos,sin

cdef extern from "math.h":
    cdef double sin(double)
    cdef double cos(double)
    cdef double atan2(double,double)
    cdef double sqrt(double)
    
cdef double pi=numpy.pi

cdef f(int u, int v, int w, int h,double RR, double uoff, double voff,double e):
    cdef double x,y,z
    cdef double theta,phi,R
    cdef int X,Y,Z,wh,hh
    cdef double ov,ou
    
    wh=w/4
    hh=h/2

    R=float(w)/4.0*RR

    ov=hh*voff
    ou=wh*uoff
    
    theta= pi*v/h
    phi=2.0*pi*u/w

    x=R*sin(theta)*cos(phi)
    y=R*sin(theta)*sin(phi)
    z=R*cos(theta)
    if 0<= phi < pi:
        return((z-ou)+w, ov-e*x)
    else:
        return((ou-z),  ov-e*x)
    
cdef g(width, height, RR, uoff, voff,e):
    cdef int u,v,u1
    map0=numpy.zeros((width/2, width, 2), dtype=numpy.float32)
    for v in range(width/2):
            for u in range(width/2):
                map0[v, u, :]   = f(u, v, width, width/2, RR, uoff, voff,e )
                u1=width-1-u
                map0[v, u1, :] = f(u1, v, width, width/2, RR, uoff, voff,e )
    return map0

# half size matp

cdef fh(int u, int v, int w, int h,double RR, double uoff, double voff,double e):
    cdef double x,y,z
    cdef double theta,phi,R
    cdef int X,Y,Z,wh,hh
    cdef double ov,ou

    
    wh=w/2
    hh=h/2

    R=float(w)/2.0*RR

    ov=hh*voff
    ou=wh*uoff
    
    theta= pi*v/h
    phi=pi*u/w

    x=R*sin(theta)*cos(phi)
    y=R*sin(theta)*sin(phi)
    z=R*cos(theta)
    return((ou-z),  ov-e*x)

cdef gl(width, height, RR, uoff, voff,e):
    cdef int u,v
    map0=numpy.zeros((width, width, 2), dtype=numpy.float32)
    for v in range(width):
            for u in range(width):
                map0[v, u :] = f(u, v, width, width, RR, uoff, voff,e )
    return map0

cdef gr(width, height, RR, uoff, voff,e):
    cdef int u,v
    map0=numpy.zeros((width, width, 2), dtype=numpy.float32)
    for v in range(width):
            for u in range(width):
                map0[v, width-u :] = f(u, v, width, width, RR, uoff, voff,e )
    return map0


def generate_DFtoER_map(w, h, RR=0.895, uoff=1.0, voff=1.0, e=0.971):
    map0=g(w, h, RR, uoff, voff,e)
    return map0
