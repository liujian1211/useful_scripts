import os

folder_path = 'D:/yolov5-master/datasets/cap/labels/train_bak'

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path,filename)
        with open(file_path,'r') as f:
            lines = f.readlines()
        if len(lines)>0:
            first_line = lines[0] #获取第一行
            numbers = first_line.strip().split()
            if len(numbers) >0 and numbers[0]=='15':
                numbers[0] = '0'  # 将第一个数字替换为0
                first_line = ' '.join(numbers) + '\n'  # 拼接替换后的第一行
                lines[0] = first_line  # 替换原来的第一行
                with open(file_path, 'w') as f:
                    f.writelines(lines)  # 将修改后的内容写回文件

