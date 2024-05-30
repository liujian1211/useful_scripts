import os

images_dir = 'D:/damagedataset_v8/cement/images/train'
labels_dir = 'D:/damagedataset_v8/cement/labels/train'

# 获取images和labels文件夹中的文件名列表
# Get the list of image files and their corresponding labels
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
label_files = [f for f in os.listdir(labels_dir) if os.path.isfile(os.path.join(labels_dir, f))]

# Create sets to store the matches
image_set = set(os.path.splitext(f)[0] for f in image_files)
label_set = set(os.path.splitext(f)[0] for f in label_files)

# Find the matches
matches = image_set & label_set

# Print the result
print(f"Number of matches: {len(matches)}")
