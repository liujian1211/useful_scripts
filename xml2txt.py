import os
import glob
import xml.etree.ElementTree as ET

# 标签映射
label_map = {
    # "Transverse cracks":0,
    # "Linear cracks":1,
    # "Pit slot":2,
    # "Crack":3,
    # "Mark":4,
    # "Tyreskidmark":5,
    # "patched":6,
    # "manhole":7,
    # "joint":8,
    # "trash":9,
    # "puddle":10,
    # "repaired crack":11,
    # "animal":12,
    # "shoes":13,
    # "bumps":14,
    # "shadow":15,
    # "incomplete mark":16,
    # "crushing_plate":17,
    # "faulting":18

    #沥青路标签
    "Transverse cracks":0,
    "Linear cracks":1,
    "Pit slot":2,
    "Crack":3,
    "patched":4,
    "trash":5,
    "repaired crack":6,
    "incomplete mark":7
}


def get_label_id(label):
    return label_map[label]


def convert_annotations(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    image_path = root.find("filename").text
    image_width = int(root.find("size/width").text)
    image_height = int(root.find("size/height").text)

    with open(os.path.splitext(xml_path)[0] + ".txt", "w") as out_file:
        for obj in root.iter("object"):
            label = obj.find("name").text
            if label=='white cracks':
                print(xml_path)
            bbox = obj.find("bndbox")
            x_center = (int(bbox.find("xmin").text) + int(bbox.find("xmax").text)) / 2.0 / image_width
            y_center = (int(bbox.find("ymin").text) + int(bbox.find("ymax").text)) / 2.0 / image_height
            width = (int(bbox.find("xmax").text) - int(bbox.find("xmin").text)) / image_width
            height = (int(bbox.find("ymax").text) - int(bbox.find("ymin").text)) / image_height
            label_id = get_label_id(label)
            out_file.write(f"{label_id} {x_center} {y_center} {width} {height}\n")


# 处理每个xml文件
for xml_file in glob.glob("D:/damagedataset_v8/finished_dataset5/labels/*.xml"):
    convert_annotations(xml_file)