def point_in_neighbor_incircle(x, y, neighbor_x, neighbor_y, radius, angle, direction):
    incircle_radius = radius / (1 + math.sin(math.radians(angle)))
    incircle_center_x = neighbor_x + incircle_radius * math.cos(math.radians(direction))
    incircle_center_y = neighbor_y + incircle_radius * math.sin(math.radians(direction))

    dx = x - incircle_center_x
    dy = y - incircle_center_y
    d = math.sqrt(dx * dx + dy * dy)

    return d <= incircle_radius


def find_redundant_nodes(sensors):
    redundant_nodes = []

    for sensor in sensors:
        neighbor_sensors = neighbor(sensor[0], sensor[1])
        incircle_radius = radius / (1 + math.sin(math.radians(sensor[2])))

        is_covered = True

        # 检查内切圆上的360个点（每1度一个点）是否被其邻居节点的内切圆覆盖
        for angle in range(360):
            incircle_point_x = sensor[0] + incircle_radius * \
                math.cos(math.radians(sensor[2] + angle))
            incircle_point_y = sensor[1] + incircle_radius * \
                math.sin(math.radians(sensor[2] + angle))

            point_covered = False

            for neighbor_sensor in neighbor_sensors:
                if point_in_neighbor_incircle(incircle_point_x, incircle_point_y, neighbor_sensor[0], neighbor_sensor[1], radius, 120, neighbor_sensor[2]):
                    point_covered = True
                    break

            if not point_covered:
                is_covered = False
                break

        if is_covered:
            redundant_nodes.append(sensor)

    return redundant_nodes

# 在主程序中调用该函数
if __name__ == '__main__':
    # ... 其他代码 ...
    redundant_nodes = find_redundant_nodes(sensors)
    print("冗余节点数量:", len(redundant_nodes))
