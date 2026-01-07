#读取表格中的2列来计算这2列的mean_error
import pandas as pd
import numpy as np

data = pd.read_excel('D:/AkyPower/onnx与rknn模型精度损失比较/1745_1805.xlsx')

pac_real = data['pac_real'].astype(float)
pred_rknn = data['pred_rknn']
pred_onnx = data['pred_onnx']

mean_error_real_rknn = np.mean((pac_real - pred_rknn)**2)
mean_error_onnx_rknn = np.mean((pred_onnx - pred_rknn)**2)

print(f'rknn与真实pac的均方差为{round(mean_error_real_rknn,4)}')
print(f'onnx与rknn的均方差为{round(mean_error_onnx_rknn,4)}')