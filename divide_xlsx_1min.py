import pandas as pd

df =pd.read_excel('D:/AkyPower/xlp/2019.08.xlsx')

# 确保“日期”和“时间”列为字符串
df['日期'] = df['日期'].astype(str)
df['时间'] = df['时间'].astype(str)

# 合并“日期”和“时间”列为一个新的 datetime 列
df['datetime'] = pd.to_datetime(df['日期'] + ' ' + df['时间'])

# 设置 datetime 列为索引
df.set_index('datetime', inplace=True)

# 按每分钟的间隔进行重采样，并获取每分钟的第一条数据
df_minute = df.resample('T').first().dropna().reset_index()

df_minute.to_excel('D:/AkyPower/xlp/725_2_.xlsx',index=False)