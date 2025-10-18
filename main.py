import cv2
from datetime import datetime

camera_ip = "192.168.88.10"
stream_url = f"rtsp://{camera_ip}/mainstream"

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("دوربین باز نشد!")
    exit()

# دریافت اندازه فریم و نرخ فریم از دوربین
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 20.0

print("width =", width)
print("height =", height)
print("fps =", fps)

# کاهش کیفیت تصویر
new_width = 1280  # عرض جدید (مقدار دلخواه)
new_height = 720  # ارتفاع جدید (مقدار دلخواه)
# new_fps = 15.0  # نرخ فریم جدید (مقدار دلخواه)

# تنظیم زمان فعلی برای نام فایل
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"output_{current_time}.mp4"

# تنظیم کدک و فایل خروجی
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # کدک MP4
out = cv2.VideoWriter(output_filename, fourcc, fps, (new_width, new_height))

while True:
    ret, frame = cap.read()

    if not ret:
        print("فریم خوانده نشد!")
        break

    # تغییر اندازه فریم (اختیاری)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # نمایش فریم در پنجره
    cv2.imshow('دوربین', resized_frame)

    # نوشتن فریم در فایل ویدیویی
    out.write(resized_frame)

    # اگر کلید 'q' فشار داده شود، حلقه متوقف می‌شود
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()