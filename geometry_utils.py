# this file is used for a basic utility colelction, reagarding teh geometric functions used throughout our project
#in here we have algorithms to compute all of teh 6 point distributions presented in the paper + an additional heart

import random
import math

def orientation(p, q, r):
    (px, py) = p



    (qx, qy) = q
    (rx, ry) = r
    return (qx - px) * (ry - py) - (qy - py) * (rx - px)

def generate_points(distribution, num_pts, w, h):
    pts = []

    if distribution == "Uniform Random":
        for _ in range(num_pts):
            x = random.uniform(0, w)
            y = random.uniform(0, h)

            pts.append((x, y))
    elif distribution == "Mostly Collinear":
        half = num_pts // 2
        for _ in range(half):
            x = random.uniform(0, w)
            y = 0.5 * x + random.uniform(-20, 20)
            pts.append((x, y))
        for _ in range(num_pts - half):
            x = random.uniform(0, w)
            y = random.uniform(0, h)
            pts.append((x, y))
    elif distribution == "Circle":
        c_x, c_y = w / 2, h / 2
        rad = min(w, h) / 3
        for _ in range(num_pts):
            angle = random.uniform(0, 2 * math.pi)
            x = c_x + rad * math.cos(angle)
            y = c_y + rad * math.sin(angle)
            pts.append((x, y))
    elif distribution == "Duplicates":
        uniq_pts = {(random.uniform(0, w), random.uniform(0, h)) for _ in range(num_pts // 2)}
        pts = list(uniq_pts) * 2
    elif distribution == "Fibonacci Spiral":
        c_x, c_y = w / 2, h / 2
        golden_ang = math.radians(137.5)  # that is golden angle in radians
        scale = min(w, h) / 10
        pts = []

        for i in range(num_pts):
            angle = i * golden_ang
            rad = scale * math.sqrt(i)
            x = c_x + rad * math.cos(angle)
            y = c_y + rad * math.sin(angle)
            pts.append((x, y))

        print("Fibonacci Spiral Points:")
        for p in pts:
            print(p)







    elif distribution == "Heart":
        c_x, c_y = w / 2, h / 2
        scl = min(w, h) / 3
        for t in range(num_pts):
            ang = 2 * math.pi * t / num_pts
            x_val = 16 * math.sin(ang)**3
            y_val = 13 * math.cos(ang) - 5 * math.cos(2 * ang) - 2 * math.cos(3 * ang) - math.cos(4 * ang)
            x_pos = c_x + scl * x_val / 34
            y_pos = c_y - scl * y_val / 34
            if 0 <= x_pos <= w and 0 <= y_pos <= h:
                pts.append((x_pos, y_pos))
    elif distribution == "Sierpinski Triangle":
        verts = [(w / 2, 20), (20, h - 20), (w - 20, h - 20)]
        current_pt = verts[0]
        for _ in range(num_pts):
            chosen_vert = random.choice(verts)
            current_pt = ((current_pt[0] + chosen_vert[0])/2, (current_pt[1] + chosen_vert[1])/2)
            pts.append(current_pt)
    elif distribution == "Koch Snowflake":
        def koch_iterate(pnts, depth):
            if depth == 0 or len(pnts) > num_pts:
                return pnts
            new_pnts = []
            for i in range(len(pnts)):
                p1 = pnts[i]
                p2 = pnts[(i + 1) % len(pnts)]
                dx, dy = (p2[0] - p1[0]) / 3, (p2[1] - p1[1]) / 3
                new_pnts.extend([
                    p1,
                    (p1[0] + dx, p1[1] + dy),
                    (p1[0] + dx - dy * math.sqrt(3)/2, p1[1] + dy + dx * math.sqrt(3)/2),
                    (p1[0] + 2*dx, p1[1] + 2*dy)
                ])
            return koch_iterate(new_pnts, depth - 1)

        base_tri = [
            (w / 4, h * 3 / 4),



            (w * 3 / 4, h * 3 / 4),
            (w / 2, h / 4)
        ]
        pts = koch_iterate(base_tri, 3)[:num_pts]

    return pts

def distance_sq(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2




def remove_points(orig, hull):
    hull_set = set(hull)
    new_lst = [p for p in orig if p not in hull_set]
    return new_lst
