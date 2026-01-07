import os
import cv2

# def extract_frames_from_folder(folder_path,frame_interval,output_folder):
#     count = 0
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.endswith((".mp4", ".avi", ".mov")):
#                 video_path = os.path.join(root, file)
#                 print("视频路径为",video_path)
#                 cap = cv2.VideoCapture(video_path)
#                 while cap.isOpened():
#                     ret,frame = cap.read()
#                     if not ret:
#                         break
#                     if count % frame_interval == 0:
#                         frame_name = os.path.join(output_folder + "/__frame__" + str(count) + ".jpg")
#                         cv2.imwrite(frame_name, frame)
#                         print("save frame",frame_name)
#                     count += 1
#
#                 cap.release()
#                 cv2.destroyAllWindows()
#     print("Extract frame successfully")
#
# folder_path = "D:/样本_待标注/20240815"
# frame_interval = 5
# output_folder = "D:/样本_待标注/frame"
# extract_frames_from_folder(folder_path, frame_interval,output_folder)

# def extract_frames(video_path, save_path, frame_interval):
#     # 检查保存路径是否存在，不存在则创建
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#
#     # 打开视频文件
#     cap = cv2.VideoCapture(video_path)
#
#     if not cap.isOpened():
#         print(f"无法打开视频文件: {video_path}")
#         return
#
#     frame_count = 0
#     saved_count = 0
#
#     while True:
#         ret, frame = cap.read()
#
#         if not ret:
#             break
#
#         # 如果当前帧是我们想要保存的
#         if frame_count % frame_interval == 0:
#             # 构建保存帧的文件名
#             frame_filename = os.path.join(save_path, f"frame_{saved_count:06d}.jpg")
#             # 保存帧为图片文件
#             cv2.imwrite(frame_filename, frame)
#             saved_count += 1
#
#         frame_count += 1
#
#     # 释放视频捕获对象
#     cap.release()
#     print(f"共保存了{saved_count}张图片在路径: {save_path}")
#
# # 使用示例
# video_path = 'D:/样本_待标注/20240815/72_16851050204_240301_112132_112833_1.mp4'
# save_path = 'D:/样本_待标注/frame'
# frame_interval = 5  # 每 帧保存一帧
#
# extract_frames(video_path, save_path, frame_interval)
