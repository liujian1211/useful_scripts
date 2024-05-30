import os
import cv2

def extract_frames_from_folder(folder_path,frame_interval,output_folder):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mp4", ".avi", ".mov")):
                video_path = os.path.join(root, file)
                # print("视频路径为",video_path)
                cap = cv2.VideoCapture(video_path)
                while cap.isOpened():
                    ret,frame = cap.read()
                    if not ret:
                        break
                    if count % frame_interval == 0:
                        frame_name = os.path.join(output_folder + "/frame_" + str(count) + ".jpg")
                        cv2.imwrite(frame_name, frame)
                        print("save frame",frame_name)
                    count += 1

                cap.release()
                cv2.destroyAllWindows()
    print("Extract frame successfully")

folder_path = "D:/test_tensorrt"
frame_interval = 7
output_folder = "D:/test_tensorrt/frames"
extract_frames_from_folder(folder_path, frame_interval,output_folder)