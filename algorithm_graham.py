#this file implements the second algorith discussed in the paper,  Graham Bell, to find a convex hull,
#and also all the dunctions required to use thsi algorithm

import geometry_utils as geom
import math


def graham_hull(points):
    
    pnct = list(set(points)) 
    n = len(pnct)
    if n < 3:
        return pnct  

    
    pivot = min(pnct, key=lambda p: (p[1], p[0]))

   
    pnct.remove(pivot)
    pnct.sort(key=lambda p: (polar_angle(pivot, p), geom.distance_sq(pivot, p)))

   
    hull = [pivot]
    for p in pnct:
        
        while len(hull) >= 2 and geom.orientation(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull


def polar_angle(pivot, point):

    dx = point[0] - pivot[0]
    
    
    dy = point[1] - pivot[1]
    return math.atan2(dy, dx)


def graham_layers(points):
  
    layers = []
    pnct = list(set(tuple(p) for p in points))  

    while len(pnct) >= 3:
        hull = graham_hull(pnct)
        if len(hull) < 3:
            break
            
            
            
            
        layers.append(hull)
        pnct = geom.remove_points(pnct, hull)  

    
    if pnct:
        layers.append(pnct)

    return layers
