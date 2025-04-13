import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import array
import time


class VideoPlayerApp:
    def __init__(self, window, video_source):
        self.count = 0
        self.chances = 0
        self.window = window
        self.window.title("Video Player")

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        def btn1():
             root.destroy()
             subprocess.run(["python", "createuser.py"]) 

        def btn2():
             root.destroy()
             subprocess.run(["python", "deleteuser.py"])

        def btn3():
             root.destroy()
             subprocess.run(["python", "userlimit.py"]) 

        def on_button_click():
            root.destroy()
            subprocess.run(["python", "login.py"]) 

        def setTime():
            root.destroy()
            subprocess.run(["python", "setTimeLimit.py"])

        width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)-40
        window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))

        self.createButton = tk.Button(window, text='CREATE  USER', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=btn1)
        self.createButton.place(x=600, y=130)

        self.deleteButton = tk.Button(window, text='DELETE  USER', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=btn2)
        self.deleteButton.place(x=600, y=205)

        self.userlimitButton = tk.Button(window, text='USER  LIMIT', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black', cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=btn3)
        self.userlimitButton.place(x=600, y=280)

        self.setTimeLimit = tk.Button(window, text='Set Time', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black', cursor='hand2', activebackground='black', activeforeground='cyan',width=15,  command=setTime)
        self.setTimeLimit.place(x=600, y=350)   

        self.backButton = tk.Button(window, text='Back', font=('Open Sans', 16, 'bold'), bd=0, bg='cyan', fg='black', cursor='hand2', activebackground='black', activeforeground='cyan',  command=on_button_click)
        self.backButton.place(x=20, y=20)

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


root = tk.Tk()
video_source = 'admin1.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
