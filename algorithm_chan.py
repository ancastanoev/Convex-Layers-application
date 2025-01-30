# this file implements the fifth and last algorith discussed in the paper, Chans's, to find a convex hull,
# this we have found- both in teh paper and in the actual experimeent here to be teh most efficient in some use cases
# we have here its layer computation function and some helprs

import geometry_utils as geom
from algorithm_andrew import andrew_hull

def chan_layers(points):
    layers = []



    pts = points[:]
    while len(pts) >= 3:
        hull = chan_hull(pts)
        if len(hull) < 3:
            break
        layers.append(hull)
        pts = geom.remove_points(pts, hull)
    return layers

def chan_hull(points, m=None):


    if m is None:
        m = max(10, int(len(points)**0.5))  

    pts = list(set(points))
    
    if len(pts) < 3:
        return pts

    chunk_size = m
    subhulls = []
    for i in range(0, len(pts), chunk_size):
        chunk = pts[i:i+chunk_size]



        subh = andrew_hull(chunk)
        subhulls.append(subh)




    combinat = []
    for sh in subhulls:
        combinat.extend(sh)
    combinat = list(set(combinat))


    final_hull = andrew_hull(combinat)
    return final_hull
