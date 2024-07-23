import os
import json
from PIL import Image

# 定义路径
json_dir = r'D:\images7.22\labels_liqing'
image_dir = r'D:\images7.22\liqing'
output_dir = r'D:\images7.22\labels_yolo'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 类别对应表 (如有多个类别，请添加到此字典中)
class_mapping = {
    "Transverse cracks":0,
    "Linear cracks":1,
    "Pit slot": 2,
    "Crack":3,
    "Patched":4,
    "trash":5,
    "repaired crack":6,
    "incomplete mark":7,
    "Loose":8
}

for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_dir,json_file)

        with open(json_path,'r') as f:
            data = json.load(f)

        image_name = data[0]['image']
        image_path = os.path.join(image_dir,image_name)
        img = Image.open(image_path)
        image_width,image_height = img.size

        txt_filename = os.path.splitext(image_name)[0] + '.txt'
        txt_path = os.path.join(output_dir,txt_filename)

        with open(txt_path,'w') as txt_file:
            for annotation in data[0]['annotations']:
                label = annotation['label']
                class_id = class_mapping.get(label,-1)
                if class_id == -1:
                    continue

                coords = annotation['coordinates']
                x_center = coords['x'] / image_width
                y_center = coords['y'] / image_height
                width = coords['width'] / image_width
                height = coords['height'] / image_height

                # 写入YOLO格式的标签
                txt_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

                print(f'写入{txt_path}完成')