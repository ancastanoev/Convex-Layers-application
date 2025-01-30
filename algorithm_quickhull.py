# this file implements the forth algorith discussed in the paper, QuickHull, to find a convex hull,
# we use its  divide and conquer approach to calculate the huls
import math

import geometry_utils


def line_distance_sq(a, b, p):
    cross = abs(geometry_utils.orientation(a, b, p))
    ab_len_sq = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
    return cross ** 2 / ab_len_sq if ab_len_sq != 0 else 0




def quickhull_layers(points):
    layers = []
    pts = points[:]
    while len(pts) >= 3:
        hull = quickhull(pts)
        if len(hull) < 3:
            break
        layers.append(hull)
        pts = geometry_utils.remove_points(pts, hull)
    return layers

def quickhull(points):
    pts = list(set(points))
    if len(pts) < 3:
        return pts

    minX = min(pts, key=lambda p: p[0])
    maxx = max(pts, key=lambda p: p[0])

    left_set = [p for p in pts if geometry_utils.orientation(minX, maxx, p) > 0]
    right_set = [p for p in pts if geometry_utils.orientation(maxx, minX, p) > 0]

    hull = []
    find_hull(minX, maxx, left_set, hull)
    find_hull(maxx, minX, right_set, hull)

    hull.append(minX)
    hull.append(maxx)
    hull = sort_ccw(hull)

    return hull

def find_hull(p1, p2, pts, hull):
    if not pts:
        return

    farthest = max(pts, key=lambda p: line_distance_sq(p1, p2, p))
    hull.append(farthest)

    left_of_p1_farthest = [p for p in pts if geometry_utils.orientation(p1, farthest, p) > 0]

    left_of_farthest_p2 = [p for p in pts if geometry_utils.orientation(farthest, p2, p) > 0]
    find_hull(p1, farthest, left_of_p1_farthest, hull)
    find_hull(farthest, p2, left_of_farthest_p2, hull)



def sort_ccw(points):
   
   
   
    if len(points) < 3:
        return points

    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)

    points.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return points
