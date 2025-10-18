import cv2
import threading
from datetime import datetime

camera_ip = "192.168.88.10"
stream_url = f"rtsp://{camera_ip}/mainstream"

# --- کلاس برای خواندن فریم‌ها در Thread ---
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            print("دوربین باز نشد!")
            exit()
        self.ret, self.frame = self.cap.read()
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()


# --- راه‌اندازی ---
vs = VideoStream(stream_url)

width = int(vs.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vs.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vs.cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 20.0

print("width =", width)
print("height =", height)
print("fps =", fps)

new_width, new_height = 1280, 720

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"output_{current_time}.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_filename, fourcc, fps, (new_width, new_height))

print("شروع ضبط... برای خروج 'q' را بزنید.")

while True:
    ret, frame = vs.read()
    if not ret or frame is None:
        print("فریم خوانده نشد!")
        break

    resized_frame = cv2.resize(frame, (new_width, new_height))
    out.write(resized_frame)
    cv2.imshow("نمای زنده", resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop()
out.release()
cv2.destroyAllWindows()
print("پایان ضبط.")
