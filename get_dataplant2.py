import pandas as pd
import math
import numpy as np

import test as t

# excel数据导入
data_xy = pd.DataFrame(pd.read_excel
                       (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-测试\实验3.0'
                        r'\x_y_shiyan30 _pandas_3.0.xlsx'))
data_name = pd.DataFrame(pd.read_excel
                         (r'C:\Users\Joo\Desktop\毕设\实验数据\实验数据-测试\实验3.0'
                          r'\name_shiyan_pandas_3.0.xlsx'))
# 全局变量N poi总数
global N
N = 107

# 全局变量F 实例总数
global F
F = 30

# 全局变量K 特征总数
global K
K = 7
a = 0

# data_exa_2 实例poi坐标 用于邻居矩阵
data_exa_2 = pd.DataFrame(columns=['实例序号', '所属特征', 'point_x', 'point_y'])
# data_mem_2 实例poi犹豫模糊隶属度 用于记分函数
data_mem_2 = pd.DataFrame(columns=['poi序号', '实例名', '犹豫模糊隶属度'])
# data_poi_2 实例poi 用于空间邻近度
data_poi_2 = pd.DataFrame(columns=['实例序号', 'poi序号', '实例名', '所属特征'])
# data_fea_2 特征 用于行、表实例
data_fea_2 = pd.DataFrame(columns=['特征名'])

# 循环存储
for i in range(0, N):
    data_exa_2.loc[i, '实例序号'] = data_xy.iloc[i, 0]
    data_exa_2.loc[i, 'point_x'] = data_xy.iloc[i, 1]
    data_exa_2.loc[i, 'point_y'] = data_xy.iloc[i, 2]
    data_exa_2.loc[i, '所属特征'] = data_xy.iloc[i, 5]

for i in range(0, F):
    data_poi_2.loc[i, '实例序号'] = i + 1
    data_poi_2.loc[i, '实例名'] = data_name.iloc[i, 1]

for i in range(0, N):
    data_mem_2.loc[i, 'poi序号'] = data_xy.iloc[i, 7]
    data_mem_2.loc[i, '实例名'] = data_xy.iloc[i, 3]
    data_mem_2.loc[i, '犹豫模糊隶属度'] = data_xy.iloc[i, 6]
    if not math.isnan(data_xy.iloc[i, 0]):
        data_poi_2.loc[a, 'poi序号'] = data_xy.iloc[i, 7]
        data_poi_2.loc[a, '所属特征'] = data_xy.iloc[i, 5]
        a = a + 1

for i in range(0, K):
    data_fea_2.loc[i, '特征名'] = data_name.iloc[i, 2]

data_poi_2.loc[F, 'poi序号'] = N+1

# print(data_exa_2)
# print(data_mem_2)
# print(data_poi_2)
# print(data_fea_2)
