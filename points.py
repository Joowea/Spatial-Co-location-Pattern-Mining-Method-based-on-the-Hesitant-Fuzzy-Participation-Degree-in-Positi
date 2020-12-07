import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


plt.title("I'm a scatter diagram.")
plt.xlim(xmax=80, xmin=0)
plt.ylim(ymax=80, ymin=0)

N = 107

data_exa = pd.DataFrame(pd.read_excel(r'C:\Users\Joo\Desktop'
                                      r'\毕设\实验数据\实验数据-测试\实验3.0'
                                      r'\x_y_shiyan30 _pandas_3.0.xlsx'))

E = data_exa
plt.title('The Test Data 3.0')


# for i in range(0, 14):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='x', c=(0.8, 0, 0), s=80, alpha=0.4)
#
# for i in range(14, 37):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='+', c=(0, 0.2, 0), s=80, alpha=0.4)
#
# for i in range(37, 46):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='o', c=(0,0.4,0.4), s=80, alpha=0.4)
#
# for i in range(46, 68):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='.', c=(0.2,0.2,0.4), s=50, alpha=0.4)
#
# for i in range(68, 82):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='1', c=(0.6,0,0.4), s=80, alpha=0.4)
#
# for i in range(82, 93):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker='2', c=(0.2,0.4,0.8), s=80, alpha=0.4)
#
# for i in range(93, N):
#     plt.scatter(E.iloc[i, 4], E.iloc[i, 5], marker=',', c=(0.2,0,0.6), s=80, alpha=0.4)

for i in range(0, N):

    if i < 14:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='x', c=(0.8, 0, 0), s=80, alpha=0.4)

    elif 14 <= i < 37:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='+', c=(0, 0.2, 0), s=80, alpha=0.4)

    elif 37 <= i < 46:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='o', c=(0, 0.4, 0.4), s=80, alpha=0.4)

    elif 46 <= i < 68:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='.', c=(0.2, 0.2, 0.4), s=50, alpha=0.4)

    elif 68 <= i < 82:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='1', c=(0.6, 0, 0.4), s=80, alpha=0.4)

    elif 82 <= i < 93:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker='2', c=(0.2, 0.4, 0.8), s=80, alpha=0.4)

    else:
        plt.scatter(E.iloc[i, 1], E.iloc[i, 2], marker=',', c=(0.2, 0, 0.6), s=80, alpha=0.4)

plt.show()