import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import mysql.connector
import subprocess

class VideoPlayerApp:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("setTimeLimit")

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 40
        window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))
        
        self.start_time_label = tk.Label(window, text='Start Time (HH:MM:SS):', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.start_time_label.place(x=560, y=160)
        self.start_time_entry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.start_time_entry.place(x=570, y=195)

        self.end_time_label = tk.Label(window, text='End Time (HH:MM:SS):', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.end_time_label.place(x=560, y=240)
        self.end_time_entry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.end_time_entry.place(x=570, y=275)

        self.submit_button = tk.Button(window, text='UPDATE', font=('Open Sans', 16, 'bold'), bd=3, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=7,command=self.connect_database)
        self.submit_button.place(x=570, y=340)

        self.clear_button = tk.Button(window, text='CLEAR', font=('Open Sans', 16, 'bold'), bd=3, bg='cyan', fg='black',activebackground='black', activeforeground='cyan', width=7, command=self.clear)
        self.clear_button.place(x=720, y=340)

        self.back_button = tk.Button(window, text='Back', font=('Open Sans', 16, 'bold'), bd=0, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', command=self.on_button_click)
        self.back_button.place(x=20, y=20)
        
        self.update()

    def connect_database(self):
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        
        if not start_time or not end_time:
            messagebox.showerror('Error', 'All Fields Are Required')
            return
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
            cursor = conn.cursor()
            sql = "UPDATE admin SET start_time = %s, end_time = %s"
            cursor.execute(sql, (start_time, end_time))
            conn.commit()
            messagebox.showinfo("Success", "time has set set successfully!")
            self.window.destroy()
            subprocess.run(["python", "admin.py"])
        except mysql.connector.Error as e:
            messagebox.showerror('Error', f'Database Connectivity issue: {e}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def clear(self):
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)

    def on_button_click(self):
        self.window.destroy()
        subprocess.run(["python", "admin.py"]) 

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)
        
root = tk.Tk()
video_source = 'AccessTime.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
