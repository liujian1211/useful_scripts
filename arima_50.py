from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_excel('D:/AkyPower/20240703_1645_1745.xlsx')
data_predict = pd.read_excel('D:/AkyPower/20240703_1745_1750.xlsx')

# 设置GHI和AT的拟合相关的参数
p_ghi=0
d_ghi=2
q_ghi=2

p_at=0
d_at=1
q_at=0

at_order = (p_at,d_at,q_at)
ghi_order = (p_ghi,d_ghi,q_ghi)

#拟合算法
def fit_arima_model(series,order):
    model = ARIMA(series,order=order)
    result = model.fit()
    return result

time_series_ghi = data.set_index('time')['GHI']  # 取GHI作为时间序列数据
time_series_at = data.set_index('time')['AT']    # 取AT作为时间序列数据

time = data['time']
GHI = data['GHI']
AT = data['AT']

GHI_future = data_predict['GHI']
AT_future  = data_predict['AT']

# 拟合模型
temperature_model = fit_arima_model(time_series_at, at_order)
ghi_model = fit_arima_model(time_series_ghi, ghi_order)

predictions_at = temperature_model.predict(start=len(AT),end=len(AT)+6,dynamic=True)
predictions_ghi = ghi_model.predict(start=len(GHI),end = len(GHI)+6,dynamic=True)

print(f'实际GHI和AT的均值为{np.mean(GHI_future.values)}和{np.mean(AT_future.values)}')
print(f'预测GHI和AT的均值为{np.mean(predictions_ghi.values)}和{np.mean(predictions_at.values)}')

plt.plot(range(63, len(GHI_future) + 63),GHI_future,label='real GHI')
plt.plot(range(63, len(GHI_future) + 63),AT_future,label='real AT')

# plt.plot(GHI, label='Actual GHI')
# plt.plot(AT,label='Actual AT')
plt.plot(predictions_ghi,label='predicted GHI')
plt.plot(predictions_at,label='predicted AT')
plt.xticks(range(0, 100, 5))  # 设置x轴刻度从到100，间隔为10
plt.legend()
plt.show()

# all_results = pd.DataFrame()
#
# window_size=50 #每50个数据拟合一下GHI和AT
# for i in range(len(data)-window_size+1):
#     subset = data.iloc[i:i+window_size]
#     time_series_ghi = subset.set_index('time')['GHI']
#     time_series_at = subset.set_index('time')['AT']    # 取AT作为时间序列数据
#
#     time = subset['time']
#     GHI = subset['GHI']
#     AT = subset['AT']
#
#     GHI_diff = np.diff(GHI, n=2)  # n阶差分
#     AT_diff = np.diff(AT, n=1)
#
#     # 拟合模型
#     temperature_model = fit_arima_model(time_series_at, at_order)
#     ghi_model = fit_arima_model(time_series_ghi, ghi_order)
#
#     predictions_at = temperature_model.predict(start=len(AT) , end=len(AT) + 10,dynamic=True) # 每隔时间步长是6s，这里+10是后10个步长，即1min
#     predictions_ghi = ghi_model.predict(start=len(GHI), end=len(GHI) + 10, dynamic=True)
#
#     temp_df = pd.DataFrame({'Prediction_ghi':predictions_ghi})
#     all_results = pd.concat([all_results,temp_df])
#
# # 将结果保存到Excel文件中
# all_results.to_excel('./arima_predictions.xlsx', index=False)
