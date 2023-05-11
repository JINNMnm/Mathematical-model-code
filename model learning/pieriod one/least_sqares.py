# a test on least squares method

#first, import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import math

def divf(x):
    if x==0:
        return 1e-7
    return x

#then select two random parameters
x = [1,2,3,4,5,6,7]
num_x = len(x)
y = [1.5,3.8,6.7,9.0,11.2,13.6,16]
#respectively,calculate the sum of x and y
sum_x = sum(x)
sum_y = sum(y)
#calculate the sum of x^2
sum_x2 = sum([i**2 for i in x])
#calculate the sum of x*y
sum_xy = sum([i*j for i,j in zip(x,y)])

slope = (num_x*sum_xy - sum_x*sum_y)/divf(num_x*sum_x2 - sum_x**2)
intersect = (sum_y - slope*sum_x)/divf(num_x)
print("slope is %f, intersect is %f" %(slope,intersect))
#draw the line and the point
plt.plot(x,y,'bo')
plt.plot(x,[slope*i+intersect for i in x],'red')
plt.legend(['data','least squares']);
plt.show()