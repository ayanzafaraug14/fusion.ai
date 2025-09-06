# geometry_solver.py
import math

# --- Triangles ---
def triangle_area_heron(a, b, c):
    s = (a + b + c) / 2
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    steps = [
        f"Semi-perimeter s = (a + b + c) / 2 = {s}",
        f"Area = √(s * (s - a) * (s - b) * (s - c)) = {area}"
    ]
    return area, steps

def triangle_area_base_height(base, height):
    area = 0.5 * base * height
    steps = [
        f"Area = 1/2 * base * height",
        f"Area = 1/2 * {base} * {height} = {area}"
    ]
    return area, steps

# --- Circles ---
def circle_area(radius):
    area = math.pi * radius**2
    steps = [
        f"Area = π * r^2",
        f"Area = π * {radius}^2 = {area}"
    ]
    return area, steps

def circle_circumference(radius):
    circ = 2 * math.pi * radius
    steps = [
        f"Circumference = 2 × π × r",
        f"Circumference = 2 × π × {radius}",
        f"Circumference = {circ}"
    ]
    return circ, steps

# --- Coordinate Geometry ---
def distance_between_points(x1, y1, x2, y2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    steps = [
        f"Distance = √((x2 - x1)^2 + (y2 - y1)^2)",
        f"Distance = √(({x2}-{x1})^2 + ({y2}-{y1})^2) = {dist}"
    ]
    return dist, steps

def midpoint(x1, y1, x2, y2):
    mx = (x1 + x2)/2
    my = (y1 + y2)/2
    steps = [
        f"Midpoint = ((x1 + x2)/2, (y1 + y2)/2)",
        f"Midpoint = (({x1} + {x2})/2, ({y1} + {y2})/2) = ({mx}, {my})"
    ]
    return (mx, my), steps
