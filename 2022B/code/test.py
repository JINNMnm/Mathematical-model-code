from sympy import *
from collections import namedtuple
import math
import matplotlib.pyplot as plt
import random
import time
Point = namedtuple('Point', ['x', 'y'])
r = 100
flys = [Point(0, 0)]
for i in range(9):
    ang = i * 40 / 180 * math.pi
    flys.append(Point(r * math.cos(ang), r * math.sin(ang)))
    print(flys)
sel_p = random.choice(flys[1:])
target = sel_p + Point((random.randint(0, 2) * 2 - 1) * random.randint(80, 120) / 10,
                       (random.randint(0, 2) * 2 - 1) * random.randint(80, 120) / 10)
p1 = 1
p2 = random.randint(2, 9)
print(target, p1, p2)
a0 = get_ang(flys[0] - target)
ap1 = get_ang(flys[p1] - target)
ap2 = get_ang(flys[p2] - target)
show(a0, ap1, ap2)
plt.pause(1)
plt.clf()