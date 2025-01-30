#this file implements the third algorith discussed in the paper, Andrew's Monotone Chain, to find a convex hull,
#and we use a mechansim to compute separatly uppr and lowe hulls

import geometry_utils as geom

def andrew_hull(points):
   
    pts = sorted(set(points))  

    if len(pts) < 3:
        return pts

 
    lower = []
    for p in pts:
        while len(lower) >= 2 and geom.orientation(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

 
 
 
 
 
    uppr = []
    for p in reversed(pts):
        while len(uppr) >= 2 and geom.orientation(uppr[-2], uppr[-1], p) <= 0:
            uppr.pop()
        uppr.append(p)


    lower.pop()
    
    
    
    
    uppr.pop()
    hull = lower + uppr
    return hull

def andrew_layers(points):
    
    
    
    layers = []
    pts = points[:]
    while len(pts) >= 3:
        hull = andrew_hull(pts)
        if len(hull) < 3:
            break
        layers.append(hull)
        pts = geom.remove_points(pts, hull)
    return layers
