import pandas as pd

df = pd.read_excel('D:/AkyPower/20240701.xlsx',sheet_name='Sheet1')

# 筛选满足条件的行
filtered_df = df[df['15min'].apply(lambda x: int(str(x).split('.')[0]) % 15 == 0)]

# 将筛选后的数据写入新的Excel文件
filtered_df.to_excel('D:/AkyPower/20240701_.xlsx', index=False)

df = pd.read_excel('D:/AkyPower/20240701_.xlsx',sheet_name='Sheet1')

# 初始化前一个数字为None
previous_number = None

indices_to_drop = []
for index, value in df['15min'].iteritems():
    current_number = int(str(value).split('.')[0])
    if current_number == previous_number:
        indices_to_drop.append(index)
    previous_number = current_number

# 删除行
df.drop(indices_to_drop, inplace=True)

# 将修改后的数据写入新的Excel文件
df.to_excel('D:/AkyPower/20240701__.xlsx', index=False)