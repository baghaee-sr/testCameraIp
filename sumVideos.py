from moviepy.editor import VideoFileClip, concatenate_videoclips

# لیست فایل‌های ویدئو
video_files = [
    "video1.mp4",
    "video2.mp4",
    "video3.mp4"
]

# بارگذاری ویدیوها
clips = [VideoFileClip(v) for v in video_files]

# اتصال به هم
final_clip = concatenate_videoclips(clips, method="compose")

# خروجی نهایی
final_clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
