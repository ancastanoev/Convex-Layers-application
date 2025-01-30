#this file implements the first algorith discussed in the paper,  Jarvis March (Gift Wrapping) to find a convex hull,
#and aslo a function `jarvis_layers` for peeling away layers


import geometry_utils as geom


def remove_points(points, to_remove):
    return [p for p in points if p not in to_remove]



def jarvis_hull(points):
    
    pts = list(set(points))  
    n = len(pts)
    if n < 3:
        return pts  




    lftmost = min(pts, key=lambda p: (p[0], p[1])) 
    hull = []
    current = lftmost
    while True:
        hull.append(current)
        next_pt = pts[0] if pts[0] != current else pts[1]

        for p in pts:
            if p == current:
                continue
            
            orient = geom.orientation(current, next_pt, p)
            if orient > 0:  
                next_pt = p
            elif orient == 0:  
                if distance_sq(current, p) > distance_sq(current, next_pt):
                    next_pt = p

        current = next_pt  
        if current == lftmost:  
            break

    return hull

def distance_sq(a, b):




    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2



def jarvis_layers(points):
    
    
    layers = []
    pts = list(set(tuple(p) for p in points))
    print(f"Starting Jarvis Layers with {len(pts)} points.")

    while len(pts) >= 3:
        hull = jarvis_hull(pts)
       
        if len(hull) < 3:
            print("Hull size less than 3, stoping.")
            break
        layers.append(hull)
        pts = remove_points(pts, hull)  
     

   
    if pts:
        layers.append(pts)
        print(f"Remaining Points Added as Fial Layer: {pts}")

   
    return layers
