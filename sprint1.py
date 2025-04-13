import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
import os
import tempfile
import cv2
import subprocess
from tkinter import messagebox
import winreg


class VideoPlayerApp:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("USB Physical Security For Systems")
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
        image = Image.open("pic1.jpeg")
        background_image = ImageTk.PhotoImage(image)
        background_label = tk.Label(window, image=background_image)
        background_label.place(x=315, y=80)
        background_label.image = background_image

        self.info_Button = tk.Button(window, text='DEVELOPERS INFO', font=('Open Sans', 12, 'bold'), bd=5, bg='DeepSkyBlue4', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=self.project_info)
        self.info_Button.place(x=650, y=450)

        self.disable_Button = tk.Button(window, text='DISABLE', font=('Open Sans', 16, 'bold'), bd=5, bg='DeepSkyBlue4', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=self.button1_clicked)
        self.disable_Button.place(x=230, y=370)

        self.enableButton = tk.Button(window, text='ENABLE', font=('Open Sans', 16, 'bold'), bd=5, bg='DeepSkyBlue4', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=self.button2_clicked)
        self.enableButton.place(x=460, y=370)

        self.exitButton = tk.Button(window, text='EXIT', font=('Open Sans', 12, 'bold'), bd=5, bg='DeepSkyBlue4', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=12, command=self.button3_clicked)
        self.exitButton.place(x=120, y=450)

        self.project_label = tk.Label(window, text="!!! USB Physical Security !!!", font=("Arial", 20, "bold"), bg="black", fg="white")
        self.project_label.place(x=300, y=20)

        self.project_label1 = tk.Label(window, text="!!!   LOCK YOUR USB PORTS   !!!", font=("Arial", 12, "bold"), bg="black", fg="white")
        self.project_label1.place(x=330, y=290)

        try:
            # Open the registry key
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_READ)
            
            # Query the Start value
            self.value, regtype = winreg.QueryValueEx(registry_key, "Start")
            winreg.CloseKey(registry_key)
            if self.value == 3:
            	self.project_label2 = tk.Label(window, text="!!!   USB IS ENABLED   !!!", font=("Arial", 12, "bold"), bg="black", fg="white")
            	self.project_label2.place(x=350, y=320)
            elif self.value == 4:
            	self.project_label3 = tk.Label(window, text="!!!   USB IS DISABLED   !!!", font=("Arial", 12, "bold"), bg="black", fg="white")
            	self.project_label3.place(x=350, y=320)
            else:
                messagebox.showerror(f"USB ports are in an unknown state (Start value: {value}).")
        except FileNotFoundError:
            messagebox.showerror("Registry key not found.")
        except Exception as e:
            messagebox.showerror(f"An error occurred: {e}")

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def project_info(self):
        #open html file
        subprocess.run(["start", "developerinfo.html"], shell=True)    

    def button1_clicked(self):
        if self.value==3:
            self.window.destroy()
            subprocess.run(["python", "authenticate2.py"])
        else:
            messagebox.showerror("Error", "USB is already disabled")

    def button2_clicked(self):
        if self.value==4:
            self.window.destroy()
            subprocess.run(["python", "authenticate1.py"])
        else:
            messagebox.showerror("Error", "USB is already enabled")


        
    def button3_clicked(self):
        answer = messagebox.askquestion("Exit", "Are you sure you want to exit?")
        if answer == 'yes':
            # Open the registry key
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_READ)
            
            # Query the Start value
            self.value, regtype = winreg.QueryValueEx(registry_key, "Start")
            winreg.CloseKey(registry_key)
            if self.value == 4:
            	self.window.destroy()
            	subprocess.run(["python", "login.py"])

            else:
	            messagebox.showerror("Error", "USB is in enable state please disable the usb port before you exit.")


root = tk.Tk()
video_source = 'home.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
