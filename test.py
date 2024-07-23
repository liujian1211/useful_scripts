import os
import shutil

# 定义文件路径
labels_path = r'D:\images7.22\labels_liqing'
images_path = r'D:\images7.22\liqing'
crack_labels_path = r'D:\images7.22\crack_labels'
crack_images_path = r'D:\images7.22\crack_images'

# 创建目标文件夹（如果不存在）
os.makedirs(crack_labels_path, exist_ok=True)
os.makedirs(crack_images_path, exist_ok=True)

# 遍历labels文件夹中的所有txt文件
for label_file in os.listdir(labels_path):
    if label_file.endswith('.txt'):
        label_file_path = os.path.join(labels_path, label_file)

        # 读取txt文件内容
        with open(label_file_path, 'r') as file:
            lines = file.readlines()

        # 检查是否有类别为3的标签
        contains_class_3 = any('3' in line.split() for line in lines)

        if contains_class_3:
            # 移动标签文件到crack_labels
            shutil.move(label_file_path, os.path.join(crack_labels_path, label_file))

            # 移动对应的图片文件到crack_images
            image_file = os.path.splitext(label_file)[0] + '.jpg'  # 假设图片扩展名为.jpg，可以根据实际情况调整
            image_file_path = os.path.join(images_path, image_file)
            if os.path.exists(image_file_path):
                shutil.move(image_file_path, os.path.join(crack_images_path, image_file))
            else:
                print(f'对应的图片文件 {image_file} 不存在')

print('文件处理完成。')
