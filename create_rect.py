import numpy as np
import cv2

# 创建一个空白图片
image = np.ones((2400, 3200, 3), dtype=np.uint8) * 255

# 定义三角形的三个顶点
pts1 = np.array([[0, 0], [300, 0], [0, 300]], np.int32)
pts2 = np.array([[3200-300,0],[3200,0],[3200,300]],np.int32)
pts3 = np.array([[3200,2400-300],[3200,2400],[3200-300,2400]],np.int32)
pts4 = np.array([[0,2400-300],[0,2400],[300,2400]],np.int32)

# 使用fillPoly函数绘制实心三角形
cv2.fillPoly(image, [pts1], (0, 0, 255))
cv2.fillPoly(image, [pts2], (0, 0, 255))
cv2.fillPoly(image, [pts3], (0, 0, 255))
cv2.fillPoly(image, [pts4], (0, 0, 255))

# 显示生成的图片
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('./rect.jpg',image)