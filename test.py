import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import acf, pacf, plot_acf, plot_pacf
from statsmodels.graphics.api import qqplot

# 1.创建数据
data = [5922, 5308, 5546, 5975, 2704, 1767, 4111, 5542, 4726, 5866, 6183, 3199, 1471, 1325, 6618, 6644, 5337, 7064,
        2912, 1456, 4705, 4579, 4990, 4331, 4481, 1813, 1258, 4383, 5451, 5169, 5362, 6259, 3743, 2268, 5397, 5821,
        6115, 6631, 6474, 4134, 2728, 5753, 7130, 7860, 6991, 7499, 5301, 2808, 6755, 6658, 7644, 6472, 8680, 6366,
        5252, 8223, 8181, 10548, 11823, 14640, 9873, 6613, 14415, 13204, 14982, 9690, 10693, 8276, 4519, 7865, 8137,
        10022, 7646, 8749, 5246, 4736, 9705, 7501, 9587, 10078, 9732, 6986, 4385, 8451, 9815, 10894, 10287, 9666, 6072,
        5418]

data = pd.Series(data)
data.index = pd.Index(sm.tsa.datetools.dates_from_range('1901', '1990'))
# data.plot(figsize=(12, 8))
# # 绘制时序的数据图
# plt.show()

data1 = data.diff(1)
data1.dropna(inplace=True)

# 第一步：先检查平稳序列的自相关图和偏自相关图
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(data1, lags=40, ax=ax1)
# lags 表示滞后的阶数
# 第二步：下面分别得到acf 图和pacf 图
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(data1, lags=40, ax=ax2)

plt.show()

# # 读取图片
# image = cv2.imread('D:/0104_td_2829.png')
#
# bbox_h=98
# bbox_w=87
# x_c=1163
# y_c=819
#
#
# x1 = 631
# y1 = 1370
# x2=680
# y2=1548
#
# # 画矩形框
# cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # (, 255, ) 代表绿色，2 代表线段的宽度
#
# # 显示结果
# cv2.imshow('Image with Rectangle', image)
# cv2.waitKey()
# cv2.destroyAllWindows()