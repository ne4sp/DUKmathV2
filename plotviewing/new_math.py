import math
from parsing import get_lines
import matplotlib.pyplot as plt

def angle_with_vertical(x1: float, y1: float, x2: float, y2: float) -> float:
    v1 = (0, 1)
    v2 = (x2 - x1, y2 - y1)
    dot_product = v1[1] * v2[1]
    magnitude_v2 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if magnitude_v2 == 0:
        return 0
    cos_theta = dot_product / magnitude_v2
    cos_theta = max(min(cos_theta, 1), -1)
    theta = math.acos(cos_theta)
    return theta

def find_vertical(array):
    minAngle = 180
    point = 0
    for i in range(len(array)-1):
        if angle_with_vertical(i, array[i], i+1, array[i+1]) < minAngle:
            minAngle = angle_with_vertical(i, array[i], i+1, array[i+1])
            point = i
    return point

def tangent(array, dp, level):
    return (level - array[dp])/(array[dp+1]-array[dp]) + dp

a = get_lines('trlog.txt')

conc = [a[i].rv for i in range(len(a))]
print(conc)
runup = [find_vertical(a[i].lv) for i in range(len(a))]
print(runup)
intersections = [tangent(a[i].lv, runup[i], 3500) for i in range(len(a))]

intersections_avg = [(intersections[i] + runup[i]) for i in range(len(intersections))]
plt.plot(intersections, conc)
plt.plot([intersections[0], intersections[-1]], [conc[0], conc[-1]])
plt.show()