import re


def calculate_scoring_function(s_loc, membership):

    # membership 实例位置序号 及其犹豫模糊隶属度表
    # s_loc 实例位置的序号
    # h_fuzz_e 提取的隶属度字符串
    # h_fuzz_e_pure 提取的犹豫模糊隶属度列表
    # h_fuzz_e_count 获取的犹豫个数
    # sc 记分系数
    h_fuzz_e = membership.loc[abs(s_loc) - 1, 'mem']
    h_fuzz_e_pure = re.findall(r"\d+\.?\d*", h_fuzz_e)
    h_fuzz_e_count = len(h_fuzz_e_pure)

    # 犹豫个数>1 引入记分函数 —————————————————————记分系数暂写死为0—————————————————————
    sc = 0.0
    if h_fuzz_e_count != 1:
        sum_of_h_fuzz_e1 = 0.0
        sum_of_h_fuzz_e2 = 0.0
        for fu_i in range(0, h_fuzz_e_count):
            sum_of_h_fuzz_e1 = sum_of_h_fuzz_e1 + float(h_fuzz_e_pure[fu_i]) ** (sc + 1)
            sum_of_h_fuzz_e2 = sum_of_h_fuzz_e2 + float(h_fuzz_e_pure[fu_i]) ** sc
        h_fuzz_mem = sum_of_h_fuzz_e1 / sum_of_h_fuzz_e2

    else:
        h_fuzz_mem = float(h_fuzz_e_pure[0])

    return h_fuzz_mem
