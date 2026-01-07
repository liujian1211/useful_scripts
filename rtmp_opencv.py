import cv2

RTMP_URL = "rtmp://223.244.16.243:1935/dock_stream/4TADL2L001001Y_1751593648487"

cap = cv2.VideoCapture(RTMP_URL)

if not cap.isOpened():
    print("❌ 无法打开流")
    exit()

print("🟢 开始播放 - 按ESC键退出")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("⚠️ 帧读取错误，重试中...")
        # 尝试重新连接
        cap.release()
        cap = cv2.VideoCapture(RTMP_URL)
        continue
        
    cv2.imshow('RTMP Stream', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()