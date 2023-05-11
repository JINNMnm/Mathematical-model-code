#本代码实现第二题中的正十边形对目标区域的密排问题。
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv

def decagon_centers(r, width, height, overlap_ratio):
    # 计算正十边形的宽和高
    decagon_width = r * (1 + math.cos(math.pi / 5))
    decagon_height = r * (1 + math.sin(math.pi / 5))

    # 考虑重叠，计算间距
    adjusted_decagon_width = decagon_width * (1 - overlap_ratio)
    adjusted_decagon_height = decagon_height * (1 - overlap_ratio)

    # 定义存储正十边形中心点的列表
    centers = []

    # 遍历矩阵的行和列，根据调整后的间距生成中心点
    for i in range(math.ceil(height / adjusted_decagon_height)):
        for j in range(math.ceil(width / adjusted_decagon_width)):
            # 将当前正十边形的中心添加进列表
            center_x = j * adjusted_decagon_width + decagon_width / 2
            center_y = i * adjusted_decagon_height + decagon_height / 2
            centers.append((center_x, center_y))

    return centers

def get_decagon_vertices(center, r):
    vertices = []
    for i in range(10):
        angle = 2 * math.pi * i / 10
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        vertices.append((x, y))
    return vertices

def plot_decagon_centers(decagon_centers, r):
    fig, ax = plt.subplots()
    
    for center in decagon_centers:
        vertices = get_decagon_vertices(center, r)
        decagon = patches.Polygon(vertices, fill=False, edgecolor="blue", linewidth=1)
        ax.add_patch(decagon)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    plt.show()

def get_sector_coordinates(center, r, angle, direction):
    x = center[0] + (r + 10) * math.cos(direction)
    y = center[1] + (r + 10) * math.sin(direction)
    return (x, y, angle)

def write_sectors_to_csv(centers, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['sector_center_x', 'sector_center_y', 'angle', 'direction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for center in centers:
            vertices = get_decagon_vertices(center, r)
            for i in range(10):
                direction = 2 * math.pi * i / 10 + math.pi / 10
                sector_coordinates = get_sector_coordinates(center, r, 120, direction)
                writer.writerow({
                    'sector_center_x': sector_coordinates[0],
                    'sector_center_y': sector_coordinates[1],
                    'angle': sector_coordinates[2],
                    'direction': direction})


# 设定边长、矩阵尺寸以及重叠比例（0-1）
r = 2.90
width = 1000
height = 100
overlap_ratio = 0.0

# 计算正十边形中心点
centers = decagon_centers(r, width, height, overlap_ratio)

# 绘制正十边形
plot_decagon_centers(centers, r)

print(len(centers))

# 将扇形信息写入csv文件
write_sectors_to_csv(centers, 'sectors.csv')