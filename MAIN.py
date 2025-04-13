import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import subprocess

class VideoPlayerApp:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("USB Physical Security")
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)-40
        window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))
        self.update()

    def play_video(self):
        self.cap = cv2.VideoCapture(self.video_source)

    def stop_video(self):
        self.cap.release()
        
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)
        self.window.after(3000, self.navigate_to_another_page)

    def navigate_to_another_page(self):
        root.destroy()
        subprocess.run(["python", "login.py"])

root = tk.Tk()
video_source = 'welcome6.mp4'  
app = VideoPlayerApp(root, video_source)
root.mainloop()
