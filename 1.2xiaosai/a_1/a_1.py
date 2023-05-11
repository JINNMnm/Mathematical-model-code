import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# create an empty list to store the points
points = []

# generate 1000 random points within the range of 0 to 1000 for both x and y coordinates
for i in range(1000):
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    points.append((x, y))
print(points)

