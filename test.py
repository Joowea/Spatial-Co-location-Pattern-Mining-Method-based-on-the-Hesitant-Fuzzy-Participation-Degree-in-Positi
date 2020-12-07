



# h_fuzz_e 提取隶属度字符串
# h_fuzz_e_pure 提取犹豫模糊隶属度列表
# h_fuzz_e_count 获取犹豫个数
# sc 记分系数
def aac(h_fuzz_e_count, h_fuzz_e_pure):
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