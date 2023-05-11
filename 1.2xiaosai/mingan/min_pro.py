import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# 定义常量
num_sensors = 1000
area_height = 1000
area_width = 100
k_coulomb = 1000.0
radius = 10
k_hooke = 0.1
min_force = 0.01
angle_max = 5
angle_min = 1
k_force_angle = 0.1

sensors = []
new_sensors = []

def centroid(x, y, direction):
    x = x + 10 * math.cos(math.radians(direction)) * (2/3)
    y = y + 10 * math.sin(math.radians(direction)) * (2/3)
    return [x, y, direction]


# 定义函数：计算 Coulomb 力，方向从 x1,y1 指向 x2,y2
def coulomb_force(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = math.sqrt(dx*dx + dy*dy)
    if d > 10 or d == 0:
        return (0, 0)
    f = k_coulomb / (d*d)
    fx = f * dx / d
    fy = f * dy / d
    return (fx, fy)

# 输入目标传感器以及传感器集合，返回目标传感器的邻居传感器集合


def neighbor(x, y):
    neighbor = []
    for sen in sensors:
        if ((sen[0]-x)**2+(sen[1]-y)**2)**0.5 < 2 * radius and (sen[0]-x)**2+(sen[1]-y)**2 != 0:
            neighbor.append(sen)
    return neighbor

# 输入一个目标点和目标点邻居点，输出目标点所受的合力


def total_force(target, neightbor):
    fx = 0
    fy = 0
    for i in neightbor:
        centriod_i = centroid(i[0], i[1], i[2])
        centriod_target = centroid(target[0], target[1], target[2])
        f1, f2 = coulomb_force(
            centriod_i[0], centriod_i[1], centriod_target[0], centriod_target[1])
        fx += f1
        fy += f2
    total_force = math.sqrt(fx*fx + fy*fy)
    if total_force < min_force:
        return (0, 0)
    # 计算合力的方向，范围为0-359
    if fx == 0:
        if fy > 0:
            force_direction = 90
        else:
            force_direction = 270
    if fx < 0 and fy < 0 :
        force_direction = math.degrees(math.atan(fy / fx)) + 180
    elif fx < 0 and fy > 0:
        force_direction = math.degrees(math.atan(fy / fx)) + 180
    elif fx > 0 and fy < 0:
        force_direction = math.degrees(math.atan(fy / fx)) + 360
    elif fx != 0:
        force_direction = math.degrees(math.atan(fy / fx))
    # 确定合力的方向施加在目标点后是顺时针还是逆时针，顺时针-1，逆时针1
    direction = 0
    if target[2] < 180:
        if force_direction > target[2] and force_direction < target[2] + 180:
            direction = 1
        else:
            direction = -1
    else:
        if force_direction > target[2] - 180 and force_direction < target[2]:
            direction = -1
        else:
            direction = 1
    return total_force, direction

# 定义函数：更新传感器位置和方向


def update_sensors(target, forces, direction):
    if k_force_angle * forces > angle_max:
        new_direction = target[2] + angle_max * direction
    elif k_force_angle * forces < angle_min:
        new_direction = target[2] - angle_max * direction
    else:
        new_direction = target[2] + k_force_angle * forces * direction
    if new_direction >= 360 or new_direction < 0:
        new_direction = new_direction % 360
    return new_direction

# 判断一个点有没有被传感器检测到


#判断一个点有没有被传感器检测到
def is_included(x,y):
    for i in neighbor(x,y):
        dx = x - i[0]
        dy = y - i[1]
        d = math.sqrt(dx*dx + dy*dy)
        if d > 10 or d == 0:
            continue

        if dx == 0:
            if dy > 0:
                direction = 90
            else:
                direction = 270
        if dx < 0 and dy < 0:
            direction = math.degrees(math.atan(dy/dx)) + 180
        elif dx < 0 and dy > 0:
            direction = math.degrees(math.atan(dy/dx)) + 180
        elif dx > 0 and dy < 0:
            direction = math.degrees(math.atan(dy/dx)) + 360
        elif dx == 0 or dy == 0:
            direction = 0
        else:
            direction = math.degrees(math.atan(dy / dx))

        angle = math.fabs(i[2] - direction)
        if angle < 60:
            return True
    return False

#计算概率
def calculate_probability(x,y):
    probability = 0
    for i in neighbor(x,y):
        dx = x - i[0]
        dy = y - i[1]
        d = math.sqrt(dx*dx + dy*dy)
        if d < 5.5 :
            probability = 1
            break
        elif d > 10:
            continue
        elif probability > 0.9:
            break
        probability += math.exp(5.5 - d)
    return probability

#检查附近7m有没有新增的点
def can_add(x,y,add_num):
    for i in range(add_num):
        dx = x - sensors[num_sensors + i][0]
        dy = y - sensors[num_sensors + i][1]
        d = math.sqrt(dx*dx + dy*dy)
        if d < 10:
            return False
    return True

#蒙特卡洛随机模拟，若不满足则加点
def monte_carlo():
    count = 0
    added = 0
    while True:
        x = random.randint(0, 93) + 4
        y = random.randint(0, 988) + 3.66
        if calculate_probability(x,y) > 0.97:
            count += 1
        else:
            if not can_add(x, y, added):
                continue
            count = 0
            added += 1
            #随机生成一个以该点为centriod的传感器
            sensors.append([x,y - 6.66,0])
            for i in range(2):
                neighbor_sensors_v = neighbor(x,y)
                forces_v , direction_v = total_force(sensors[num_sensors + added - 1], neighbor_sensors_v)
                new_direction_v = update_sensors(sensors[num_sensors + added - 1], forces_v, direction_v)
                sensors[num_sensors + added - 1][2] = new_direction_v
            print("add a sensor at (%d,%d)"%(x,y))
        if count > 5000:
            break

# 添加新函数用于绘制扇形
def draw_sector(ax, x, y, radius, angle, direction):
    start_angle = direction - angle / 2
    end_angle = direction + angle / 2
    arc = np.linspace(np.radians(start_angle), np.radians(end_angle), 100)
    x_arc = x + radius * np.cos(arc)
    y_arc = y + radius * np.sin(arc)
    ax.plot(np.hstack([x, x_arc, x]), np.hstack(
        [y, y_arc, y]), lw=1, color='b', alpha=0.3)
    ax.fill(np.hstack([x, x_arc, x]), np.hstack(
        [y, y_arc, y]), 'b', alpha=0.2)

#判断这个节点集的覆盖效果如何
def evaluate():
    result = 0
    covered = 0

    #随机生成点
    for i in range(10):
        for j in range(100):
            x = i*10 + random.randint(1,10)
            y = j*10 + random.randint(1,10)
            if x < 0:
                x = 0
            if x > 100:
                x = 100
            if y < 0:
                y = 0
            if y > 1000:
                y = 1000
            if is_included(x,y):
                covered += 1
    result = covered / 1000
    return result

# 在此处添加绘图部分
def draw():
    fig, ax = plt.subplots(figsize=(20, 10))
    for sensor in sensors:
        x, y, direction = sensor
        draw_sector(ax, y, x, 10, 120, direction)  # 交换x和y坐标来转置图
        ax.annotate(f"", (y, x), textcoords="offset points", xytext=(-6, 4), ha='center',
                    fontsize=8, color='k')  # 交换x和y坐标来转置图
    ax.set_xlim(0, area_height)
    ax.set_ylim(0, area_width)
    ax.set_aspect('equal', 'box')
    plt.title('Sensor Positions and Sectors')
    plt.xlabel('Y')  # 交换X和Y标签
    plt.ylabel('X')  # 交换X和Y标签
    plt.grid()
    plt.show()

if __name__ == '__main__':
    #生成所有点
    for i in range(10):
        for j in range(100):
            sensors.append([i*10+5,j*10,0])

    #draw()#画出初始图

    # 利用虚拟力场迭代优化传感器位置和方向，直到收敛为止
    for i in range(100):
        for target in sensors:
            neighbor_sensors = neighbor(target[0], target[1])
            forces, direction = total_force(target, neighbor_sensors)
            new_direction = update_sensors(target, forces, direction)
            target[2] = new_direction

    count = 0
    for i in range(10):
        for j in range(100):
            count += 1
            direction = sensors[count % 60][2]
            new_sensors.append([i*10+8,j*10+1,direction])
    sensors = new_sensors

    # 输出传感器位置和方向表格
    print("Sensor\tX\tY\tDirection")
    for i in range(num_sensors):
        print(f"{i+1}\t{sensors[i][0]}\t{sensors[i][1]}\t{sensors[i][2]}")
    #draw()#生成经过虚拟力场优化后的图
    monte_carlo()
    draw()#生成经过蒙特卡洛优化后的图
    #输出x,y,direction到上面的excel表格
    df = pd.DataFrame(sensors,columns=['x','y','direction'])
    df.to_excel('sensor2.xlsx', sheet_name='sensor', index=False, header=True)