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
        width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)-40
        window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))
        def connect_database():
            if self.emailEntry.get()=='' or self.usernameEntry.get()=='' :
                messagebox.showerror('Error','All Fields Are Required')
            else:
                try:
                    conn = mysql.connector.connect(host='localhost',user='root',password='root',database='login')
                    cursor = conn.cursor()
                except:
                    messagebox.showerror('Error','Database Connectivity issue,  Please Try Again')
                    return
                query = 'select * from login where email=%s'
                cursor.execute(query, (self.emailEntry.get(),))
                row = cursor.fetchone()
                if row is not None: 
                    query = 'DELETE FROM login WHERE email=%s'
                    cursor.execute(query, (self.emailEntry.get(),))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','User Deleted Successfully')
                    window.destroy()
                    subprocess.run(["python", "admin.py"])
                else:
                   messagebox.showinfo('Error','User Doesnot Exists') 
        def clear():
            self.emailEntry.delete(0,tk.END)
            self.usernameEntry.delete(0,tk.END)
        self.usernameLabel = tk.Label(window, text='Username:', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.usernameLabel.place(x=560, y=160)
        def on_button_click():
            window.destroy()
            subprocess.run(["python", "admin.py"])

        self.usernameEntry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.usernameEntry.place(x=570, y=195)
        tk.Frame(window, width=240, height=2, bg='black').place(x=570, y=225)

        self.emailLabel = tk.Label(window, text='Email:', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.emailLabel.place(x=560, y=240)


        self.emailEntry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.emailEntry.place(x=570, y=275)
        tk.Frame(window, width=240, height=2, bg='black').place(x=570, y=305)

        self.submitButton = tk.Button(window, text='DELETE', font=('Open Sans', 16, 'bold'), bd=3, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=7, command=connect_database)
        self.submitButton.place(x=570, y=340)
        self.clearButton=tk.Button(window,text='CLEAR',font=('Open Sans',16,'bold'),bd=3,bg='cyan',fg='black',activebackground='black',activeforeground='cyan',width=7,command=clear)
        self.clearButton.place(x=720, y=340)

        self.backButton = tk.Button(window, text='Back', font=('Open Sans', 16, 'bold'), bd=0, bg='cyan', fg='black',
                                      cursor='hand2', activebackground='black', activeforeground='cyan',  command=on_button_click)
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
video_source = 'deleteuser.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
