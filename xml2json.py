import pandas as pd
import json
from sklearn.model_selection import train_test_split

# 读取Excel文件
file_path = 'D:/ChatGLM3/大模型微调_养护类.xlsx'  # 将其替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 检查是否包含所需的列
if 'content' not in df.columns or 'summary' not in df.columns:
    raise ValueError("Excel表格必须包含 'content' 和 'summary' 列")

#去除数据集中的\n，并且将所有的float和int型内容转为字符串
def clean_data(row):
    # 将所有字符中的 \n 去掉，并将 float 和 int 转换为字符串
    clean_row = {}
    for key, value in row.items():
        if isinstance(value, str):
            clean_value = value.replace('\n', '')
        elif isinstance(value, (int, float)):
            clean_value = str(value)
        else:
            clean_value = value
        clean_row[key] = clean_value
    return clean_row

# 按照9:1划分训练集和验证集
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

# 打开训练集文件，以逐行写入JSON对象
train_file = 'D:/ChatGLM3/大模型微调数据集划分/train.json'
with open(train_file, 'w', encoding='utf-8') as f:
    for _, row in train_df.iterrows():
        data = {
            "content": row['content'],
            "summary": row['summary']
        }
        # json.dump(data, f, ensure_ascii=False)
        clean_row = clean_data(data)
        json.dump(clean_row, f, ensure_ascii=False)
        f.write('\n')

# 打开验证集文件，以逐行写入JSON对象
val_file = 'D:/ChatGLM3/大模型微调数据集划分/val.json'
with open(val_file, 'w', encoding='utf-8') as f:
    for _, row in val_df.iterrows():
        data = {
            "content": row['content'],
            "summary": row['summary']
        }
        # json.dump(data, f, ensure_ascii=False)
        clean_row = clean_data(data)
        json.dump(clean_row, f, ensure_ascii=False)
        f.write('\n')

print(f"数据已保存到 大模型微调数据集划分 文件夹")
