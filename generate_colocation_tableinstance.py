import numpy as np
import pandas as pd


def generate_co_location_table_instance(min_prev, c, t_co_location, k, proximity_matrix_pm, f_i_pr, membership):

    global N
    F = 30
    global K
    K = 7

    count = np.shape(c[k+1]['pattern'])
    count_co = count[0]  # 特征对对数
    count = np.shape(t_co_location[k]['label'])
    count_tk = count[0]  # 总特征数

    # 预先创建
    tt_co_location = pd.DataFrame(columns=['label', 'instance', 'pr', 'pi', 'pattern_instance_count1'])
    ckp = pd.DataFrame(columns=['pattern'])
    ckq = pd.DataFrame(columns=['pattern'])

    # 产生C(k+1) k+1阶候选co_location所有模式的实例

    for i in range(0, count_co):
        instance_all_in_one = []
        ckp_3_pattern = []
        ckq_3_pattern = []
        find_3_w = 0
        tt_co_location.loc[i, 'label'] = c[k+1]['pattern'].iloc[i]

        # x = 1

        if k+1 == 1:  # 2阶特征对分至ckp ckq
            ckp.loc[i, 'pattern'] = c[k+1]['pattern'].iloc[i][0]
            ckq.loc[i, 'pattern'] = c[k+1]['pattern'].iloc[i][1]

        # else:  *----------------------------------------未完成----------------------------------------

        else:  # 3阶以上特征对分至ckp ckq
            for w in range(0, k):
                ckp_3_pattern.append(c[k+1]['pattern'].iloc[i][w])
                ckq_3_pattern.append(c[k+1]['pattern'].iloc[i][w])
                find_3_w = w

            ckp_3_pattern.append(c[k+1]['pattern'].iloc[i][find_3_w+1])
            ckq_3_pattern.append(c[k+1]['pattern'].iloc[i][find_3_w+2])

            ckp.loc[i, 'pattern'] = ckp_3_pattern
            ckq.loc[i, 'pattern'] = ckq_3_pattern

        find_p = -1
        find_q = -1

        # 找到ckp ckq中特征与T表中特征对应序号  find_p与find_q
        for w in range(0, count_tk):

            # 如果找到 不再循环
            if find_p != -1 & find_q != -1:
                break

            # find_p find_q为0.1 说明没找到对应
            if find_p == -1:
                if ckp['pattern'][i] == t_co_location[k]['label'][w]:
                    find_p = w

            if find_q == -1:
                if ckq['pattern'][i] == t_co_location[k]['label'][w]:
                    find_q = w

        count_tkp = len(t_co_location[k].loc[find_p, 'instance'])
        count_tkq = len(t_co_location[k].loc[find_q, 'instance'])

        # 各实例循环判断邻近度
        for pp in range(0, count_tkp):

            for qq in range(0, count_tkq):
                instance_a = []

                e_quk = 1

                if k != 0:
                    for w in range(0, k):

                        if (t_co_location[k].loc[find_p, 'instance'][pp][w]
                                != t_co_location[k].loc[find_q, 'instance'][qq][w]):
                            e_quk = 0
                            break
                        instance_a.append(t_co_location[k].loc[find_p, 'instance'][pp][w])

                if e_quk == 1 or k == 0:  # 距离判断

                    dis_p = 0
                    dis_q = 0

                    for w in range(0, F):  # 找到对应distance序号

                        if t_co_location[k].loc[find_p, 'instance'][pp][k] == proximity_matrix_pm['instanceInfo'][0, w]:
                            dis_p = w

                        if t_co_location[k].loc[find_q, 'instance'][qq][k] == proximity_matrix_pm['instanceInfo'][0, w]:
                            dis_q = w

                    a = proximity_matrix_pm['proximity_mp'][dis_p, dis_q]

                    if a > 0:

                        instance_a.append(dis_p+1)
                        instance_a.append(dis_q+1)

                        if k+1 == 1:  # 2阶 实例序号后添加空间邻近度
                            instance_a.append(a)

                        else:  # 3阶 实例序号后添加空间邻近度
                            count_spd3 = len(instance_a)
                            spd3 = []
                            for spd_x in range(0, count_spd3-1):
                                for spd_y in range(spd_x + 1, count_spd3):
                                    spd3.append(proximity_matrix_pm['proximity_mp'][instance_a[spd_x]-1, instance_a[spd_y]-1])
                            instance_a.append(np.mean(spd3))   # 3阶邻近度为222均值

                        instance_all_in_one.append(instance_a)

                    # for w in range(0, k+1):
                    tt_co_location.loc[i, 'instance'] = instance_all_in_one

    # 计算Tk+1 即tt的pr pi
    count = np.shape(tt_co_location['label'])  # 阶数
    count_co_c = count[0]

    p_1 = np.zeros((count_co_c, 1))  # 预先置零
    c[k+1]['pattern_pi'] = p_1
    c[k+1]['pattern_pr'] = p_1
    c[k+1]['pattern_instance_count'] = p_1

    for i in range(0, count_co_c):

        pr_all_in_one = []  # pr表

        count_co_cf = len(tt_co_location.loc[i, 'label'])  # 阶数
        count_co_ct = len(tt_co_location.loc[i, 'instance'])  # 特征之间的实例对数

        if count_co_ct == 0:  # 无实例置零
            tt_co_location.loc[i, 'pr'] = 0
            tt_co_location.loc[i, 'pi'] = 0
            tt_co_location.loc[i, 'pattern_instance_count1'] = 0
            continue

        # 标记参与实例
        for wf in range(0, count_co_cf):
            for f in range(0, K):
                if tt_co_location.loc[i, 'label'][wf] == f_i_pr.loc[f, 'label']:
                    find_f = f
                    break

            # 标记清零
            for bmp in range(0, f_i_pr.loc[find_f, 'pattern_instance_count']):
                f_i_pr.loc[find_f, 'instance'][bmp][0] = abs(f_i_pr.loc[find_f, 'instance'][bmp][0])

            # 参与标记
            for xT in range(0, count_co_ct):
                for x in range(0, f_i_pr.loc[find_f, 'pattern_instance_count']):

                    # 判断是否参与
                    if tt_co_location.loc[i, 'instance'][xT][wf] == abs(f_i_pr.loc[find_f, 'instance'][x][0]):
                        ccc = 0 - f_i_pr.loc[find_f, 'instance'][x][0]

                        # 避免重复标记
                        if f_i_pr.loc[find_f, 'instance'][x][0] < 0:
                            f_i_pr.loc[find_f, 'instance'][x][0] = -ccc
                        # 标记
                        else:
                            f_i_pr.loc[find_f, 'instance'][x][0] = ccc

            # 计算参与总数
            count_co_all = 0.0

            all_spd = 0
            for x in range(0, f_i_pr.loc[find_f, 'pattern_instance_count']):
                ac = f_i_pr.loc[find_f, 'instance'][x][0]
                # 根据ac正负判断是否参与
                if ac < 0:
                    # # h_fuzz_e 提取隶属度字符串
                    # # h_fuzz_e_pure 提取犹豫模糊隶属度列表
                    # # h_fuzz_e_count 获取犹豫个数
                    # h_fuzz_e = membership.loc[abs(ac)-1, 'mem']
                    # h_fuzz_e_pure = re.findall(r"\d+\.?\d*", h_fuzz_e)
                    # h_fuzz_e_count = len(h_fuzz_e_pure)
                    #
                    # # 犹豫个数>1 引入函数 ———————————————————————————暂为均值计算—————————————————————————————
                    # # if h_fuzz_e_count != 1:
                    #     # fuzzAllCount = 0.0
                    #     # for fu_i in range(0, h_fuzz_e_count):
                    #     #     fuzzAllCount = fuzzAllCount + float(h_fuzz_e_pure[fu_i])
                    #     # fuzz2 = fuzzAllCount/fuzzCount
                    #
                    # # 犹豫个数>1 引入记分函数 —————————————————————记分系数暂写死为0—————————————————————
                    # if h_fuzz_e_count != 1:
                    #     sum_of_h_fuzz_e1 = 0.0
                    #     sum_of_h_fuzz_e2 = 0.0
                    #     for fu_i in range(0, h_fuzz_e_count):
                    #         sum_of_h_fuzz_e1 = sum_of_h_fuzz_e1 + (float(h_fuzz_e_pure[fu_i])) ** (0 + 1)
                    #         sum_of_h_fuzz_e2 = sum_of_h_fuzz_e2 + (float(h_fuzz_e_pure[fu_i])) ** 0
                    #     fuzz2 = sum_of_h_fuzz_e1/sum_of_h_fuzz_e2
                    #
                    # else:
                    #     fuzz2 = float(h_fuzz_e_pure[0])

                    # h_fuzz_mem = csf.calculate_scoring_function(ac, membership)
                    # count_co_all = count_co_all + h_fuzz_mem

                    # ins_spd 实例的所有空间邻近度的集合
                    # count_spd 实例的所有空间邻近度的个数
                    ins_spd = []
                    for spd_i in range (0, count_co_ct):
                        if -ac == tt_co_location.loc[i, 'instance'][spd_i][wf]:
                            ins_spd.append(tt_co_location.loc[i, 'instance'][spd_i][count_co_cf])

                    count_spd = len(ins_spd)

                    # 如果多个 取最大值
                    if count_spd != 1:
                        spd = max(ins_spd)
                    else:
                        spd = ins_spd[0]
                    all_spd = all_spd + spd

            # pr计算公式 详细信息
            pr_data = [all_spd/f_i_pr.loc[find_f, 'pattern_instance_count'],
                       all_spd, f_i_pr.loc[find_f, 'pattern_instance_count']]
            pr_all_in_one.append(pr_data)

        # pr、count记录
        tt_co_location.loc[i, 'pr'] = pr_all_in_one
        tt_co_location.loc[i, 'pattern_instance_count1'] = len(tt_co_location.loc[i, 'instance'])

        # pi=pr最小值
        min_pr = tt_co_location.loc[i, 'pr'][1][0]
        for wf in range(0, count_co_cf):
            if tt_co_location.loc[i, 'pr'][wf][0] <= min_pr:
                min_pr = tt_co_location.loc[i, 'pr'][wf][0]

        tt_co_location.loc[i, 'pi'] = min_pr

    tt_pi = tt_co_location.loc[:, 'pi']
    tt_pr = tt_co_location.loc[:, 'pr']
    tt_count = tt_co_location.loc[:, 'pattern_instance_count1']

    c[k+1]['pattern_pi'] = tt_pi
    c[k+1]['pattern_pr'] = tt_pr
    c[k+1]['pattern_instance_count'] = tt_count

    return [tt_co_location, c]
