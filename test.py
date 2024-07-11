import cv2

# 读取图片
image = cv2.imread('D:/0104_td_2829.png')

# 定义矩形框的坐标
# x1, y1, x2, y2 = 112, 770, 1207, 868

bbox_h=98
bbox_w=87
x_c=1163
y_c=819

# x1 = int(x_c - bbox_w/2)
# y1 = int(y_c - bbox_h/2)
# x2 = int(x_c + bbox_w/2)
# y2 = int(y_c + bbox_h/2)

x1 = 631
y1 = 1370
x2=680
y2=1548

# 画矩形框
cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # (, 255, ) 代表绿色，2 代表线段的宽度

# 显示结果
cv2.imshow('Image with Rectangle', image)
cv2.waitKey()
cv2.destroyAllWindows()