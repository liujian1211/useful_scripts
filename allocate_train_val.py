import os
import shutil
import random

# 设置文件夹路径
images_folder = 'D:/damagedataset_v8/cement/images'
labels_folder = 'D:/damagedataset_v8/cement/labels'
train_folder = 'train'
val_folder = 'val'

# 创建train和val文件夹
os.makedirs(os.path.join(images_folder, train_folder), exist_ok=True)
os.makedirs(os.path.join(images_folder, val_folder), exist_ok=True)
os.makedirs(os.path.join(labels_folder, train_folder), exist_ok=True)
os.makedirs(os.path.join(labels_folder, val_folder), exist_ok=True)

# 获取所有图片和标签文件列表
image_files = sorted([file for file in os.listdir(images_folder) if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']])
label_files = sorted([file for file in os.listdir(labels_folder) if file.endswith('.txt')])

# 随机打乱文件列表顺序
random.seed(42) # 设置随机种子保证每次运行结果一致
random.shuffle(image_files)
random.seed(42)
random.shuffle(label_files)

# 计算划分的边界索引
train_end_idx = int(len(image_files) * .9)
val_start_idx = train_end_idx

# 复制图片文件到train和val文件夹
for image_file in image_files[:train_end_idx]:
    shutil.move(os.path.join(images_folder, image_file), os.path.join(images_folder, train_folder, image_file))
for image_file in image_files[val_start_idx:]:
    shutil.move(os.path.join(images_folder, image_file), os.path.join(images_folder, val_folder, image_file))

# 复制标签文件到train和val文件夹
for label_file in label_files[:train_end_idx]:
    shutil.move(os.path.join(labels_folder, label_file), os.path.join(labels_folder, train_folder, label_file))
for label_file in label_files[val_start_idx:]:
    shutil.move(os.path.join(labels_folder, label_file), os.path.join(labels_folder, val_folder, label_file))

print("文件夹分割完成！")