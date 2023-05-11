import random

def random_walk(n):
    #walk to a random direction
    x , y = 0 , 0
    for i in range(n):
        (dx,dy) = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        x += dx
        y += dy
    return (x,y)
walk_num = 10000
for i in range(31):
    no_transport = 0
    for j in range(walk_num):
        (x,y) = random_walk(i)
        distance = abs(x) + abs(y)
        if distance <= 4:
            no_transport += 1
    no_transport_percentage = float(no_transport)/walk_num
    print("walk size = ",i," / % of no transport = ",100*no_transport_percentage)