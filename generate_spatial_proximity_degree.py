import numpy as np
import pandas as pd
import calculate_score_function as csf


# 返回空间邻近度矩阵 *------------临时------------
def generate_spatial_proximity_degree(EP, distance, membership):
    global N
    N = 107
    global F
    F = 30
    global K
    K = 7
    a = 0

    # 计算邻近度信息存储（调试用）

    # label 实例对象集（A+B）
    # eligible_instance_x A中符合distance关系映射的位置集 同eligible_ins_x
    # eligible_instance_y B中符合distance关系映射的位置集 同eligible_ins_y
    # eligible_mem_x A中符合distance关系映射各位置的隶属度集
    # eligible_mem_y B中符合distance关系映射各位置的隶属度集
    # all_mem_x A中所有位置的隶属度集
    # all_mem_y B中所有位置的隶属度集
    pm_calculate = pd.DataFrame(
        columns=['label', 'eligible_instance_x', 'eligible_instance_y', 'eligible_mem_x', 'eligible_mem_y',
                 'all_mem_y', 'all_mem_y'])
    proximity_matrix_pm = np.zeros((F, F))

    # ij循环：获取label每组实例集 及pm_calculate中信息
    for i in range(0, F):
        for j in range(i + 1, F):
            if EP.iloc[i, 3] != EP.iloc[j, 3]:

                f_label = list()
                f_label.append(EP.iloc[i, 2])
                f_label.append(EP.iloc[j, 2])

                eligible_ins_x = list()
                eligible_ins_y = list()

                # p_x p_y循环：获取eligible_ins_x eligible_ins_y位置集
                for p_x in range(EP.iloc[i, 1], EP.iloc[i + 1, 1]):
                    for p_y in range(EP.iloc[j, 1], EP.iloc[j + 1, 1]):

                        d = distance['distance_d'][p_x - 1, p_y - 1]  # 验证是否符合关系映射
                        if d > 0:
                            eligible_ins_x.append(p_x)
                            break  # 避免位置重复 存储一次即结束p_y内层循环

                if not eligible_ins_x:  # 若eligible_ins_x为空 则eligible_ins_y为空
                    continue  # 对象间无符合映射的位置 执行下一组j内层循环

                for p_y in range(EP.iloc[j, 1], EP.iloc[j + 1, 1]):
                    for p_x in range(EP.iloc[i, 1], EP.iloc[i + 1, 1]):
                        d = distance['distance_d'][p_x - 1, p_y - 1]
                        if d > 0:
                            eligible_ins_y.append(p_y)
                            break
                pm_calculate.loc[a, 'label'] = f_label  # label的一组实例集

                pm_calculate.loc[a, 'eligible_instance_x'] = eligible_ins_x
                pm_calculate.loc[a, 'eligible_instance_y'] = eligible_ins_y

                # 符合distance关系映射位置个数 用于循环遍历范围
                count_eligible_ins_x = len(eligible_ins_x)
                count_eligible_ins_y = len(eligible_ins_y)

                # 存储符合distance关系映射各位置的隶属度
                eligible_mem_x = []
                eligible_mem_y = []

                # 计算符合distance关系映射各位置的隶属度
                for s_eligible_loc_x in range(0, count_eligible_ins_x):
                    eligible_mem = csf.calculate_scoring_function(eligible_ins_x[s_eligible_loc_x], membership)
                    eligible_mem_x.append(eligible_mem)

                pm_calculate.loc[a, 'eligible_mem_x'] = eligible_mem_x

                for s_eligible_loc_y in range(0, count_eligible_ins_y):
                    eligible_mem = csf.calculate_scoring_function(eligible_ins_y[s_eligible_loc_y], membership)
                    eligible_mem_y.append(eligible_mem)

                pm_calculate.loc[a, 'eligible_mem_y'] = eligible_mem_y

                # 符合distance关系映射位置各隶属度的个数 用于遍历求和 数值同eligible_mem_x y
                count_eligible_x = len(eligible_mem_x)
                count_eligible_y = len(eligible_mem_y)

                sum_eligible_mem_x = 0
                sum_eligible_mem_y = 0

                # 符合distance关系映射位置的隶属度的和
                for e_mem_x in range(0, count_eligible_x):
                    sum_eligible_mem_x = sum_eligible_mem_x + eligible_mem_x[e_mem_x]

                for e_mem_y in range(0, count_eligible_y):
                    sum_eligible_mem_y = sum_eligible_mem_y + eligible_mem_y[e_mem_y]

                # 对象所有位置计算对应隶属度
                all_mem_x = []
                all_mem_y = []

                for s_loc_x in range(EP.iloc[i, 1], EP.iloc[i + 1, 1]):
                    all_mem = csf.calculate_scoring_function(s_loc_x, membership)
                    all_mem_x.append(all_mem)

                for s_loc_x in range(EP.iloc[j, 1], EP.iloc[j + 1, 1]):
                    all_mem = csf.calculate_scoring_function(s_loc_x, membership)
                    all_mem_y.append(all_mem)

                # 对象所有位置的隶属度的和
                count_all_mem_x = len(all_mem_x)
                count_all_mem_y = len(all_mem_y)

                sum_all_mem_x = 0
                sum_all_mem_y = 0

                for a_mem_x in range(0, count_all_mem_x):
                    sum_all_mem_x = sum_all_mem_x + all_mem_x[a_mem_x]

                for a_mem_y in range(0, count_all_mem_y):
                    sum_all_mem_y = sum_all_mem_y + all_mem_y[a_mem_y]

                # proximity 空间邻近度
                proximity = (sum_eligible_mem_x + sum_eligible_mem_y) / (sum_all_mem_x + sum_all_mem_y)  # 空间邻近度公式

                # 计入空间邻近度矩阵
                proximity_matrix_pm[i, j] = proximity
                proximity_matrix_pm[j, i] = proximity

                a = a + 1  # pm_calculate的下一组对象集

    return proximity_matrix_pm
