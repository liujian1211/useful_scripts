import requests
import pandas as pd

# url = "https://api.seniverse.com/v4?fields=weather_15m&key=SsJMdjPgS1s9FEDVf&locations=31:120"
#
# # 获取数据
# r = requests.get(url)
#
# # 解析数据
# data = r.json()["weather_15m"]
#
# #data[0]是一个字典{'data':xxx,'location':xxx,'time_updated':xxx}
#
# data_list = data[0]['data']
# location = data[0]['location']
# time_updated = data[0]['time_updated']
#
# df = pd.DataFrame(data_list)
# df.to_excel('D:/AkyPower/xinzhiAPI.xlsx',index=False)

df = pd.read_excel('D:/AkyPower/xinzhiAPI.xlsx')

# 将time列转换成datetime格式
df['time'] = pd.to_datetime(df['time'])

# 新增日期列和时间列
df['date'] = df['time'].dt.date
df['time'] = df['time'].dt.time

# 删除时区信息
df['date'] = df['date'].astype(str)  # 转换日期列为字符串类型
df['time'] = df['time'].astype(str)  # 转换时间列为字符串类型
# 保存处理后的文件
df.to_excel('D:/AkyPower/xinzhiAPI_out.xlsx', index=False)

print("处理完成，结果已保存到output.xlsx文件中。")
