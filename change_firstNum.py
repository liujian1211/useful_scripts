import os

def modify_txt_lines(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为.txt文件
        if filename.endswith('.txt'):
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, filename)
            # 确保是文件而不是文件夹
            if os.path.isfile(file_path):
                try:
                    # 临时文件路径，用于存储修改后的内容
                    temp_file_path = file_path + '.tmp'
                    # 以读模式打开原始文件，以写模式打开临时文件
                    with open(file_path, 'r', encoding='utf-8') as file, open(temp_file_path, 'w',encoding='utf-8') as temp_file:
                        # 逐行读取原始文件内容
                        for line in file:
                            # 去除每行可能存在的空白字符（如换行符、空格等）
                            stripped_line = line.strip()
                            # 检查行内容是否为空或第一个字符是否满足条件
                            if stripped_line and stripped_line[0] in '345':
                                # 替换第一个字符
                                new_line = stripped_line.replace(stripped_line[0], '5' if stripped_line[0] == '3' else (
                                    '3' if stripped_line[0] == '4' else '4'), 1)
                                # 将修改后的行（加上换行符）写入临时文件
                                temp_file.write(new_line + '\n')

                            else:

                                # 如果第一个字符不满足条件或行内容为空，则直接写入临时文件（保留原始格式）

                                temp_file.write(line)

                                # 替换原始文件为临时文件

                    os.replace(temp_file_path, file_path)

                    print(f"Modified {filename}")

                except Exception as e:

                    print(f"Error while processing {filename}: {e}")

                # 示例使用


if __name__ == "__main__":
    folder_to_process = 'D:/damagedataset_v8/Dataset/Dataset/shuini/labels_new'  # 请替换为你的文件夹路径

    modify_txt_lines(folder_to_process)