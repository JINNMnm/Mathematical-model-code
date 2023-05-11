import random
import math
import matplotlib.pyplot as plt
import numpy as np

# 定义常量
num_sensors = 1000
area_height = 1000
area_width = 100
k_coulomb = 1000.0
radius = 10
k_hooke = 0.1
min_force = 0.01
angle_max = 15
angle_min = 1
k_force_angle = 0.3

def centroid(x,y,direction):
    x = x + 10 * math.cos(math.radians(direction)) * (2/3)
    y = y + 10 * math.sin(math.radians(direction)) * (2/3)
    return [x,y,direction]


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


# 生成传感器位置和方向
sensors = []
for i in range(num_sensors):
    x = random.randint(0, area_width)
    y = random.randint(0, area_height)
    direction = random.randint(0, 359)
    sensors.append([x, y, direction])

#输入目标传感器以及传感器集合，返回目标传感器的邻居传感器集合
def neighbor(x,y):
    neighbor = []
    for sen in sensors:
        if ((sen[0]-x)**2+(sen[1]-y)**2)**0.5 < 2 * radius and (sen[0]-x)**2+(sen[1]-y)**2 != 0:
            neighbor.append(sen)
    return neighbor

#输入一个目标点和目标点邻居点，输出目标点所受的合力
def total_force(target,neightbor):
    fx = 0
    fy = 0
    for i in neightbor:
        centriod_i = centroid(i[0],i[1],i[2])
        centriod_target = centroid(target[0],target[1],target[2])
        f1, f2 = coulomb_force(centriod_i[0],centriod_i[1],centriod_target[0], centriod_target[1] )
        fx += f1
        fy += f2
    total_force = math.sqrt(fx*fx + fy*fy)
    if total_force < min_force:
        return (0,0)
    #计算合力的方向，范围为0-359
    if fx < 0 and fy < 0:
        force_direction = math.degrees(math.atan(fy/fx)) + 180
    elif fx < 0 and fy > 0:
        force_direction = math.degrees(math.atan(fy/fx)) + 180
    elif fx > 0 and fy < 0:
        force_direction = math.degrees(math.atan(fy/fx)) + 360
    else:
        force_direction = math.degrees(math.atan(fy/fx))
    #确定合力的方向施加在目标点后是顺时针还是逆时针，顺时针-1，逆时针1
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
    return total_force,direction

# 定义函数：更新传感器位置和方向
def update_sensors(target,forces,direction):
    if k_force_angle * forces > angle_max:
        new_direction = target[2] + angle_max * direction
    elif k_force_angle * forces < angle_min:
        new_direction = target[2] - angle_max * direction
    else:
        new_direction = target[2] + k_force_angle * forces * direction
    if new_direction >= 360 or new_direction < 0:
        new_direction = new_direction % 360
    return new_direction

#判断一个点有没有被传感器检测到
def is_included(x,y):
    for i in neighbor(x,y):
        dx = x - i[0]
        dy = y - i[1]
        d = math.sqrt(dx*dx + dy*dy)
        if d > 10 or d == 0:
            return False

        if dx < 0 and dy < 0:
            direction = math.degrees(math.atan(dy/dx)) + 180
        elif dx < 0 and dy > 0:
            direction = math.degrees(math.atan(dy/dx)) + 180
        elif dx > 0 and dy < 0:
            direction = math.degrees(math.atan(dy/dx)) + 360
        else:
            direction = math.degrees(math.atan(dy/dx))

        angle = math.fabs(i[2] - direction)
        if angle < 60:
            return True
    return False

# 添加新函数用于绘制扇形
def draw_sector(ax, x, y, radius, angle, direction):
    start_angle = direction - angle / 2
    end_angle = direction + angle / 2
    arc = np.linspace(np.radians(start_angle), np.radians(end_angle), 100)
    x_arc = x + radius * np.cos(arc)
    y_arc = y + radius * np.sin(arc)
    ax.plot(np.hstack([x, x_arc, x]), np.hstack([y, y_arc, y]), lw=1, color='b', alpha=0.3)
    ax.fill(np.hstack([x, x_arc, x]), np.hstack([y, y_arc, y]), 'b', alpha=0.2)


# 在此处添加绘图部分
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

# 迭代优化传感器位置和方向，直到收敛为止
for i in range(100):
    for target in sensors:
        neighbor_sensors = neighbor(target[0],target[1])
        forces,direction = total_force(target,neighbor_sensors)
        new_direction = update_sensors(target,forces,direction)
        # print(new_direction,target[2])
        target[2] = new_direction



# 在此处添加绘图部分
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

# 输出传感器位置和方向表格
print("Sensor\tX\tY\tDirection")
for i in range(num_sensors):
    print(f"{i+1}\t{sensors[i][0]}\t{sensors[i][1]}\t{sensors[i][2]}")