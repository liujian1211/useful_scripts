import os

labels_dir = 'D:/images7.22/labels_liqing'
images_dir = 'D:/images7.22/liqing'

# 获取labels文件夹中所有txt文件的文件名
labels_files = [f.split('.')[0] for f in os.listdir(labels_dir) if f.endswith('.txt')]

# 获取images文件夹中所有图片文件的文件名
images_files = [f.split('.')[0] for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

# 遍历labels文件夹，删除不存在对应图片的txt文件
# for label_file in labels_files:
#     if label_file not in images_files:
#         os.remove(os.path.join(labels_dir, label_file + '.txt'))

# 遍历images文件夹，删除不存在对应标签的image文件
for image_file in images_files:
    if image_file not in labels_files:
        if os.path.exists(os.path.join(images_dir, image_file + '.jpg')):
            os.remove(os.path.join(images_dir, image_file + '.jpg'))
        elif os.path.exists(os.path.join(images_dir, image_file + '.png')):
            os.remove(os.path.join(images_dir, image_file + '.png'))

# # 获取删除后labels文件夹中所有txt文件的文件名
# updated_labels_files = [f.split('.')[0] for f in os.listdir(labels_dir) if f.endswith('.txt')]
#
# # 删除多余的图片文件
# for image_file in images_files:
#     if image_file not in updated_labels_files:
#         os.remove(os.path.join(images_dir, image_file + '.jpg'))  # 这里假设图片文件的格式为jpg

print("处理完成")