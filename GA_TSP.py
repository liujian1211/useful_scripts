# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import math
# import random
#
# #读取城市数据
# def read_data():
#     data = pd.read_excel("D:/城市信息.xlsx")
#     city_name = data['city'].values
#     city_position_x = data['x'].values
#     city_position_y = data['y'].values
#
#     plt.scatter(city_position_x, city_position_y)
#     for i in range(len(city_position_x)):
#         plt.annotate(city_name[i], xy=(city_position_x[i], city_position_y[i]),
#                      xytext=(city_position_x[i] + 0.1, city_position_y[i] + 0.1))  # xy是需要标记的坐标，xytext是对应的标签坐标
#     plt.show()
#     return city_name, city_position_x, city_position_y
#
# # 读取不同城市距离矩阵
# def distances(city_name,city_position_x,city_position_y):
#     global city_count,city_distance
#     # 城市总数量
#     city_count = len(city_name)
#
#     # 城市距离矩阵初始化
#     city_distance = np.zeros([city_count,city_count])
#     for i in range(city_count):
#         for j in range(city_count):
#             city_distance[i][j] = math.sqrt(
#                 (city_position_x[i] - city_position_x[j]) ** 2 + (city_position_y[i] - city_position_y[j]) ** 2)
#             return city_count, city_distance
#
# # 计算一条路径的总长度
# def path_length(path,origin):
#     distance = 0
#     distance += city_distance[origin][path[0]]
#     for i in range(len(path)):
#         if i == len(path) - 1:
#             distance += city_distance[origin][path[i]]
#         else:
#             distance += city_distance[path[i]][path[i + 1]]
#         return distance
#
# def improve(path,improve_count,origin):
#     distance = path_length(path,origin)
#     for i in range(improve_count):
#         # 随机选择两个城市
#         u = random.randint(0, len(path) - 1)
#         v = random.randint(0, len(path) - 1)
#         if u != v:
#             new_path = path.copy()
#             t = new_path[u]
#             new_path[u] = new_path[v]
#             new_path[v] = t
#             new_distance = path_length(new_path, origin)
#             if new_distance < distance:  # 保留更优解
#                 distance = new_distance
#                 path = new_path.copy()
#     return path
#
# # 环境选择父代种群
# def selection(population,retain_rate,live_rate,origin):
#     graded = [[path_length(path, origin), path] for path in population]
#     graded = [path[1] for path in sorted(graded)]
#     # 选出适应性强的染色体
#     retain_length = int(len(graded) * retain_rate)
#     parents = graded[: retain_length]  # 保留适应性强的染色体
#     # 保留一定存活程度强的个体
#     for weak in graded[retain_length:]:
#         if random.random() < live_rate:
#             parents.append(weak)
#     return parents
#
#
# # 使用常规匹配交叉获得子代
# # 随机选取一个交配位，子代1交配位之前的基因选自父代1交配位之前，交配位之后按父代2顺序选择没有在子代1中出现的基因
# # 子代2交配位之前的基因选自父代2交配位之前，交配位之后按父代1顺序选择没有在子代2中出现的基因
# def crossover(parents, population_num):  # 存活的父代种群，种群总数
#     # 生成子代的个数
#     children_count = population_num - len(parents)
#     # 孩子列表
#     children = []
#     while len(children) < children_count:
#         # 在父母种群中随机选择父母
#         male_index = random.randint(0, len(parents) - 1)
#         female_index = random.randint(0, len(parents) - 1)
#         if male_index != female_index:
#             male = parents[male_index]
#             female = parents[female_index]
#             position = random.randint(0, len(male) - 1)  # 随机产生一个交配位
#             child1 = male[:position]
#             child2 = female[:position]
#             for i in female:
#                 if i not in child1:
#                     child1.append(i)
#             for i in male:
#                 if i not in child2:
#                     child2.append(i)
#             children.append(child1)
#             children.append(child2)
#
#
#     return children
#
#
# # 变异：随机交换路径中两个城市位置
# def mutation(children, mutation_rate):  # 孩子种群，变异率
#     for i in range(len(children)):
#         if random.random() < mutation_rate:  # 变异
#             child = children[i]
#             u = random.randint(0, len(child) - 2)
#             v = random.randint(u + 1, len(child) - 1)
#             tmp = child[u]
#             child[u] = child[v]
#             child[v] = tmp
#             children[i] = child
#     return children
#
#
# # 得到当前代种群最优个体
# def get_result(population, origin):
#     graded = [[path_length(path, origin), path] for path in population]
#     graded = sorted(graded)
#     return graded[0][0], graded[0][1]  # 返回种群的最优解
#
#
# # 结果可视化
# def plt_magin(iters, distance, result_path, origin, city_name, city_position_x, city_position_y):
#     print("进化次数为", iters, "时的最佳路径长度为：", distance)
#     result_path = [origin] + result_path + [origin]
#     #     print("最佳路线为：")
#     #     for i, index in enumerate(result_path):
#     #         print(city_name[index] + "(" + str(index) + ")", end=' ')
#     #         if i % 9 == 0:
#     #             print()
#     X = []
#     Y = []
#     for i in result_path:
#         X.append(city_position_x[i])
#         Y.append(city_position_y[i])
#
#     plt.figure()
#     plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
#     plt.plot(X, Y, '-o')
#     plt.xlabel('经度')
#     plt.ylabel('纬度')
#     plt.title("GA_TSP")
#     for i in range(len(X)):
#         plt.annotate(city_name[result_path[i]], xy=(X[i], Y[i]),
#                      xytext=(X[i] + 0.1, Y[i] + 0.1))  # xy是需要标记的坐标，xytext是对应的标签坐标
#     plt.show()
#
#
# # 遗传算法总流程
# def GA_TSP(origin, population_num, improve_count, iter_count, retain_rate, live_rate, mutation_rate):
#     # 源点，种群个体数，改良迭代数,进化次数，适者概率，生命强度，变异率
#     city_name, city_position_x, city_position_y = read_data()
#     city_count, city_distance = distances(city_name, city_position_x, city_position_y)
#     list = [i for i in range(city_count)]
#     list.remove(origin)
#     population = []
#     for i in range(population_num):
#         # 随机生成个体
#         path = list.copy()
#         random.shuffle(path)  # 随机打乱
#         path = improve(path, improve_count, origin)  # 使用改良方案尽量提高初始化种群多样性
#         population.append(path)
#     every_gen_best = []  # 存储每一代最好的
#     distance, result_path = get_result(population, origin)
#     for i in range(iter_count):
#         # 选择繁殖个体群
#         parents = selection(population, retain_rate, live_rate, origin)
#         # 交叉繁殖
#         children = crossover(parents, population_num)
#         # 变异
#         children = mutation(children, mutation_rate)
#         # 更新种群，采用杰出选择
#         population = parents + children
#         distance, result_path = get_result(population, origin)
#         every_gen_best.append(distance)
#         if (i % 500 == 0):
#             plt_magin(i, distance, result_path, origin, city_name, city_position_x, city_position_y)
#     plt_magin(i, distance, result_path, origin, city_name, city_position_x, city_position_y)
#     plt.plot(range(len(every_gen_best)), every_gen_best)
#     plt.show()
#
#
# if __name__ == '__main__':
#     GA_TSP(10, 300, 200, 10000, 0.3, 0.5, 0.01)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random


# 读取城市数据
def read_data():
    data = pd.read_excel('D:/城市信息.xlsx')
    city_name = data['city'].values
    city_position_x = data['x'].values
    city_position_y = data['y'].values
    # 原始问题图
    plt.scatter(city_position_x, city_position_y)
    for i in range(len(city_position_x)):
        plt.annotate(city_name[i], xy=(city_position_x[i], city_position_y[i]),
                     xytext=(city_position_x[i] + 0.1, city_position_y[i] + 0.1))  # xy是需要标记的坐标，xytext是对应的标签坐标
    plt.show()
    return city_name, city_position_x, city_position_y


# 计算不同城市间距离矩阵
def distances(city_name, city_position_x, city_position_y):
    global city_count, city_distance
    # 城市总数量
    city_count = len(city_name)
    # 城市距离矩阵初始化
    city_distance = np.zeros([city_count, city_count])
    for i in range(city_count):
        for j in range(city_count):
            city_distance[i][j] = math.sqrt(
                (city_position_x[i] - city_position_x[j]) ** 2 + (city_position_y[i] - city_position_y[j]) ** 2)
    return city_count, city_distance


# 计算一条路径的总长度
def path_length(path, origin):  # 具体路径，出发源点
    distance = 0
    distance += city_distance[origin][path[0]]
    for i in range(len(path)):
        if i == len(path) - 1:
            distance += city_distance[origin][path[i]]
        else:
            distance += city_distance[path[i]][path[i + 1]]
    return distance


# 改良
def improve(path, improve_count, origin):  # 具体路径，改良迭代次数
    distance = path_length(path, origin)
    for i in range(improve_count):
        # 随机选择两个城市
        u = random.randint(0, len(path) - 1)
        v = random.randint(0, len(path) - 1)
        if u != v:
            new_path = path.copy()
            t = new_path[u]
            new_path[u] = new_path[v]
            new_path[v] = t
            new_distance = path_length(new_path, origin)
            if new_distance < distance:  # 保留更优解
                distance = new_distance
                path = new_path.copy()
    return path


# 环境选择父代种群
def selection(population, retain_rate, live_rate, origin):  # 种群，适者比例, 生命强度
    # 对总距离进行从小到大排序
    graded = [[path_length(path, origin), path] for path in population]
    graded = [path[1] for path in sorted(graded)]
    # 选出适应性强的染色体
    retain_length = int(len(graded) * retain_rate)
    parents = graded[: retain_length]  # 保留适应性强的染色体
    # 保留一定存活程度强的个体
    for weak in graded[retain_length:]:
        if random.random() < live_rate:
            parents.append(weak)
    return parents


# 使用常规匹配交叉获得子代
# 随机选取一个交配位，子代1交配位之前的基因选自父代1交配位之前，交配位之后按父代2顺序选择没有在子代1中出现的基因
# 子代2交配位之前的基因选自父代2交配位之前，交配位之后按父代1顺序选择没有在子代2中出现的基因
def crossover(parents, population_num):  # 存活的父代种群，种群总数
    # 生成子代的个数
    children_count = population_num - len(parents)
    # 孩子列表
    children = []
    while len(children) < children_count:
        # 在父母种群中随机选择父母
        male_index = random.randint(0, len(parents) - 1)
        female_index = random.randint(0, len(parents) - 1)
        if male_index != female_index:
            male = parents[male_index]
            female = parents[female_index]
            position = random.randint(0, len(male) - 1)  # 随机产生一个交配位
            child1 = male[:position]
            child2 = female[:position]
            for i in female:
                if i not in child1:
                    child1.append(i)
            for i in male:
                if i not in child2:
                    child2.append(i)
            children.append(child1)
            children.append(child2)


    return children


# 变异：随机交换路径中两个城市位置
def mutation(children, mutation_rate):  # 孩子种群，变异率
    for i in range(len(children)):
        if random.random() < mutation_rate:  # 变异
            child = children[i]
            u = random.randint(0, len(child) - 2)
            v = random.randint(u + 1, len(child) - 1)
            tmp = child[u]
            child[u] = child[v]
            child[v] = tmp
            children[i] = child
    return children


# 得到当前代种群最优个体
def get_result(population, origin):
    graded = [[path_length(path, origin), path] for path in population]
    graded = sorted(graded)
    return graded[0][0], graded[0][1]  # 返回种群的最优解


# 结果可视化
def plt_magin(iters, distance, result_path, origin, city_name, city_position_x, city_position_y):
    print("进化次数为", iters, "时的最佳路径长度为：", distance)
    result_path = [origin] + result_path + [origin]
    #     print("最佳路线为：")
    #     for i, index in enumerate(result_path):
    #         print(city_name[index] + "(" + str(index) + ")", end=' ')
    #         if i % 9 == 0:
    #             print()
    X = []
    Y = []
    for i in result_path:
        X.append(city_position_x[i])
        Y.append(city_position_y[i])

    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(X, Y, '-o')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.title("GA_TSP")
    for i in range(len(X)):
        plt.annotate(city_name[result_path[i]], xy=(X[i], Y[i]),
                     xytext=(X[i] + 0.1, Y[i] + 0.1))  # xy是需要标记的坐标，xytext是对应的标签坐标
    plt.show()


# 遗传算法总流程
def GA_TSP(origin, population_num, improve_count, iter_count, retain_rate, live_rate, mutation_rate):
    # 源点，种群个体数，改良迭代数,进化次数，适者概率，生命强度，变异率
    city_name, city_position_x, city_position_y = read_data()
    city_count, city_distance = distances(city_name, city_position_x, city_position_y)
    list = [i for i in range(city_count)]
    list.remove(origin)
    population = []
    for i in range(population_num):
        # 随机生成个体
        path = list.copy()
        random.shuffle(path)  # 随机打乱
        path = improve(path, improve_count, origin)  # 使用改良方案尽量提高初始化种群多样性
        population.append(path)
    every_gen_best = []  # 存储每一代最好的
    distance, result_path = get_result(population, origin)
    for i in range(iter_count):
        # 选择繁殖个体群
        parents = selection(population, retain_rate, live_rate, origin)
        # 交叉繁殖
        children = crossover(parents, population_num)
        # 变异
        children = mutation(children, mutation_rate)
        # 更新种群，采用杰出选择
        population = parents + children
        distance, result_path = get_result(population, origin)
        every_gen_best.append(distance)
        if (i % 500 == 0):
            plt_magin(i, distance, result_path, origin, city_name, city_position_x, city_position_y)
    plt_magin(i, distance, result_path, origin, city_name, city_position_x, city_position_y)
    plt.plot(range(len(every_gen_best)), every_gen_best)
    plt.show()


if __name__ == '__main__':
    GA_TSP(10, 300, 200, 10000, 0.3, 0.5, 0.01)  # 源点，种群个数，改良次数，进化次数，适者概率，生命强度，变异率
