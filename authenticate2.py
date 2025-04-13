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
import pygame
import pygame.camera

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

        def send_email(to_email, subject, body, filename):
            from_email = 'lockyourusbport@gmail.com'
            password = 'sypu yyco rzmb jipp'
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject
            msg.attach(MIMEText(body))
            part = MIMEBase('application', 'octet-stream')
            with open(filename, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(filename))
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()

        def capture(Email):
            pygame.camera.init()
            camlist = pygame.camera.list_cameras()
            if not camlist:
                print("Error: No cameras found on the device.")
                return
            try:
                cam = pygame.camera.Camera(camlist[0], (640, 480))
                cam.start()
                time.sleep(2)  
                image = cam.get_image()
                filename = "captured_image.jpg"
                pygame.image.save(image, filename)
                print(f"Image captured and saved as '{filename}'")
                cam.stop()
                send_email('21kb1a0574@nbkrist.org', 'Subject: Someone are trying to access the USB Ports with Email:' + Email, 'Someone are trying to login with Email:' + Email , 'captured_image.jpg')     
            except Exception as e:
                print(f"An error occurred while accessing the camera: {e}")
            finally:
                pygame.camera.quit()

        def authenticate():
            Email= self.emailEntry.get()
            if Email == '':
                messagebox.showerror('Error', 'All Fields Are Required')
            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
                    cursor = conn.cursor()
                except:
                    messagebox.showerror('Error', 'Database Connectivity issue,  Please Try Again')
                    return
                query = 'select * from login where email=%s'
                cursor.execute(query, (self.emailEntry.get(),))
                row = cursor.fetchone()
                if row is None:
                    messagebox.showinfo('Error', 'Check your email and try again')   
                else:
                    query = 'select * from temp where email=%s'
                    cursor.execute(query, (self.emailEntry.get(),))
                    row1 = cursor.fetchone() 
                    if row1 is None:
                        messagebox.showinfo('Error', "Your Email doesn't match with login credentials") 
                    else:
                        capture(Email)
                        MAX_LEN = 8
                        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
                        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                                            'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 
                                            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 
                                            'z'] 
                        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                                            'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q', 
                                            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 
                                            'Z'] 
                        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', 
                                '*', '(', ')', '<'] 
                        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS 
                        rand_digit = random.choice(DIGITS) 
                        rand_upper = random.choice(UPCASE_CHARACTERS) 
                        rand_lower = random.choice(LOCASE_CHARACTERS) 
                        rand_symbol = random.choice(SYMBOLS)  
                        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol  
                        for x in range(MAX_LEN - 4): 
                            temp_pass = temp_pass + random.choice(COMBINED_LIST)  
                            temp_pass_list = array.array('u', temp_pass) 
                            random.shuffle(temp_pass_list)  
                        password = "" 
                        for x in temp_pass_list: 
                                password = password + x 
                        print(password) 
                        sender_email = 'lockyourusbport@gmail.com'
                        receiver_email = self.emailEntry.get()
                        subject = 'Password for enabling or disabling'
                        message = 'Password to disable your usb port :'+ password
                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = sender_email
                        smtp_password = "sypu yyco rzmb jipp"
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(message, 'plain'))
                        server = smtplib.SMTP(smtp_server, smtp_port)
                        server.starttls()
                        try:
                            server.login(smtp_username, smtp_password)
                        except smtplib.SMTPAuthenticationError:
                            messagebox.showerror("Error", "Wrong SMTP password")
                        else:
                            server.send_message(msg)
                            server.quit()
                            messagebox.showinfo("Success", "Message sent successfully")
                        query = 'select * from temp'
                        cursor.execute(query)
                        row1 = cursor.fetchone()
                        if row1 is not None:
                            query = 'delete from temp'
                            cursor.execute(query)
                            conn.commit()
                        query_insert = 'insert into temp(email, password) values(%s, %s)'
                        cursor.execute(query_insert, (self.emailEntry.get(), password))
                        conn.commit()
                        conn.close()
                        window.destroy()
                        subprocess.run(["python", "disable.py"]) 
                        
        def on_button_click():
            window.destroy()
            subprocess.run(["python", "sprint1.py"])
            
        self.emailLabel = tk.Label(window, text='Email:', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.emailLabel.place(x=550, y=190)

        self.emailEntry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.emailEntry.place(x=560, y=230)
        tk.Frame(window, width=240, height=2, bg='black').place(x=560, y=253)

        self.submitButton = tk.Button(window, text='AUTHENTICATE', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=authenticate)
        self.submitButton.place(x=580, y=290)

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
video_source = 'disable.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
