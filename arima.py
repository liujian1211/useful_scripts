from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
import pandas as pd
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.stats.diagnostic import acorr_ljungbox

data = pd.read_excel('D:/AkyPower/20240628_203707_5min.xlsx')

time_series_ghi = data.set_index('time')['GHI']  # 取GHI作为时间序列数据
time_series_at = data.set_index('time')['AT']    # 取AT作为时间序列数据

time = data['time']
GHI = data['GHI']
AT = data['AT']

# 绘制时间序列图
# plt.figure(figsize=(12, 6))
# plt.plot(time, AT)
# plt.xlabel('time')
# plt.ylabel('AT')
# plt.xticks(range(0, 100, 10))  # 设置x轴刻度从到100，间隔为10
# plt.title('Time Series of AT')
# plt.show()

# #绘制自相关图
# plot_acf(time_series_ghi)
# plt.show()
# #绘制偏自相关图
# plot_pacf(time_series_ghi)
# plt.show()

# 检验平稳性（ADF检验）
result = adfuller(AT)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])  #p的值显著大于0.05，因此判断为不平滑
for key, value in result[4].items():
    print('Critical Values:')
    print(f'   {key}, {value}')

# 如果数据非平稳，可以进行差分操作
GHI_diff = np.diff(GHI, n=2) # n阶差分
AT_diff = np.diff(AT,n=1)
# plt.figure(figsize=(12, 6))
# # plt.plot(time[2:], GHI_diff)
# plt.plot(time[1:],AT_diff)
# plt.xlabel('Time')
# plt.ylabel('Differenced AT')
# plt.xticks(range(0, 100, 10))  # 设置x轴刻度从到100，间隔为10
# plt.title('Differenced Time Series of AT')
# plt.show()

# plot_acf(AT_diff).show()
# plt.show()
#
# plot_pacf(AT_diff).show()
# plt.show()

#再次检查平稳性
print('-------------------------差分后---------------------------\n')
# result = adfuller(GHI_diff)
result = adfuller(AT_diff)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
for key, value in result[4].items():
    print('Critical Values:')
    print(f'   {key}, {value}')

# print(f"白噪声检验结果为：\n {acorr_ljungbox(GHI_diff,lags=1)}")
# print(f"白噪声检验结果为：\n {acorr_ljungbox(AT_diff,lags=1)}")

pmax_ghi = int(len(GHI_diff)/10)
qmax_ghi = int(len(GHI_diff)/10)
pmax_at = int(len(AT_diff)/10)
qmax_at = int(len(AT_diff)/10)

# 用 贝 叶 斯 信 息 准 则 BIC 判 断
bic_matrix_at = []
for p in range(pmax_at+1):
    tmp=[]
    for q in range(qmax_at+1):
        try:
            model= ARIMA(time_series_at,order=(p,1,q)).fit()
            bic = model.bic
            tmp.append(bic)
        except:
            tmp.append(float('inf'))
    bic_matrix_at.append(tmp)

bic_matrix_at = pd.DataFrame(bic_matrix_at)  # 将bic矩阵转换为DataFrame
# 找出最小值位置
min_idx_at = np.unravel_index(np.nanargmin(bic_matrix_at.values), bic_matrix_at.shape)
p_at, q_at = min_idx_at

bic_matrix_ghi=[]
for p in range(pmax_ghi+1):
    tmp = []
    for q in range(qmax_ghi + 1):
        try:
            model= ARIMA(time_series_ghi, order=(p, 2, q)).fit()
            bic = model.bic
            tmp.append(bic)
        except:
            tmp.append(float('inf'))
    bic_matrix_ghi.append(tmp)
bic_matrix_ghi = pd.DataFrame(bic_matrix_ghi)
min_idx_ghi = np.unravel_index(np.nanargmin(bic_matrix_ghi.values),bic_matrix_ghi.shape)
p_ghi ,q_ghi = min_idx_ghi

# 理论上每段都要算一下p d q，但时间较长，目前可以直接写死，亲测影响不大
print(f'p_at和q_at的值为{p_at},{q_at}')
print(f'p_ghi和q_ghi的值为{p_ghi},{q_ghi}')

# p_ghi=0 #根据上述min_idx确定
d_ghi=2 #因为使用了2阶差分
# q_ghi=2 #根据上述min_idx确定

# p_at=0 #根据PACF图确定
d_at=1 #因为使用了1阶差分
# q_at=0 #根据ACF图确定

# # 计算ACF和PACF
# lag_acf = acf(GHI_diff, nlags=20)
# lag_pacf = pacf(GHI_diff, nlags=20, method='ols')
#
# # 绘制ACF和PACF图
# plt.figure(figsize=(12, 6))
# plt.subplot(121)
# plt.plot(lag_acf)
# plt.axhline(y=0, linestyle='--', color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(GHI_diff)), linestyle='--', color='gray')
# plt.axhline(y=1.96/np.sqrt(len(GHI_diff)), linestyle='--', color='gray')
# plt.title('Autocorrelation Function')
#
# plt.subplot(122)
# plt.plot(lag_pacf)
# plt.axhline(y=0, linestyle='--', color='gray')
# plt.axhline(y=-1.96/np.sqrt(len(GHI_diff)), linestyle='--', color='gray')
# plt.axhline(y=1.96/np.sqrt(len(GHI_diff)), linestyle='--', color='gray')
# plt.title('Partial Autocorrelation Function')
# plt.tight_layout()
# plt.show()

# p_ghi=2 #根据PACF图确定
# d_ghi=2 #因为使用了2阶差分
# q_ghi=1 #根据ACF图确定

# p_temp=1 #根据PACF图确定
# d_temp=1 #因为使用了1阶差分
# q_temp=1 #根据ACF图确定

def fit_arima_model(series,order):
    model = ARIMA(series,order=order)
    result = model.fit()
    return result

at_order = (p_at,d_at,q_at)
ghi_order = (p_ghi,d_ghi,q_ghi)

# 拟合模型
temperature_model = fit_arima_model(time_series_at, at_order)
ghi_model = fit_arima_model(time_series_ghi, ghi_order)

predictions_at = temperature_model.predict(start=len(AT_diff),end=len(AT_diff)+10,dynamic=True)  #每隔时间步长是6s，这里+10是后10个步长，即1min
predictions_ghi = ghi_model.predict(start=len(GHI_diff),end = len(GHI_diff)+10,dynamic=True)

plt.plot(GHI, label='Actual GHI')
plt.plot(AT,label='Actual AT')
plt.plot(predictions_ghi,label='predicted GHI')
plt.plot(predictions_at,label='predicted AT')
plt.xticks(range(0, 100, 5))  # 设置x轴刻度从到100，间隔为10
plt.legend()
plt.show()


# 预测未来数据 (例如未来12个时间点)
# forecast_steps = 60 #预测1min
# temperature_forecast = temperature_model.get_forecast(steps=forecast_steps)
# ghi_forecast = ghi_model.get_forecast(steps=forecast_steps)

# temperature_forecast_values = temperature_forecast.predicted_mean
# ghi_forecast_values = ghi_forecast.predicted_mean

# #预测内容保存至excel
# df = pd.DataFrame(columns=['temp_predict','ghi_predict'])
# for temp_value,ghi_value in zip(temperature_forecast_values,ghi_forecast_values):
#     df = df.append({'temp_predict':temp_value,'ghi_predict':ghi_value},ignore_index=True)
#
# df.to_excel('D:/AkyPower/20240628_203707_5min_.xlsx',index=False)
#
# 可视化结果
# plt.figure(figsize=(14, 7))
# #
# # 温度预测
# plt.subplot(2, 1, 1)
# plt.plot(temperature, label='Observed Temperature')
# plt.plot(temperature_forecast_values, label='Forecasted Temperature', linestyle='--')
# plt.title('Temperature Forecast')
# plt.legend()
#
# 辐照度预测
# plt.subplot(2, 1, 2)
# plt.plot(GHI, label='Observed GHI')
# plt.plot(ghi_forecast_values, label='Forecasted GHI', linestyle='--')
# plt.title('GHI Forecast')
# plt.legend()
#
# plt.tight_layout()
# plt.show()