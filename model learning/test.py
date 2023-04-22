# Here is an example of a Monte Carlo method code to estimate the value of pi

import random

# Number of points inside the circle
inside = 0

# Total number of points
total = 10000000

# Loop through all the points
for i in range(total):
    # Generate a random point inside the square
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    # Check if the point is inside the circle
    if x**2 + y**2 <= 1:
        inside += 1

# Estimate the value of pi
pi = 4 * inside / total

# Print the result
print(pi)