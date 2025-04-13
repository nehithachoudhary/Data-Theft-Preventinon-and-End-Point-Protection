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
import datetime


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
        time_limit = 120
        self.start_time = time.time()

        def update_timer():
            remaining_time = max(0, time_limit - (time.time() - self.start_time))
            self.timer_label.config(text=f"Expires in: {int(remaining_time)} sec")
            window.after(1000, update_timer)

        def history(oper):
            current_timestamp = datetime.datetime.now()
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
                cursor = conn.cursor()
            except:
                messagebox.showerror('Error', 'Database Connectivity issue, Please Try Again')
                return
            query = 'select email from temp'
            cursor.execute(query)
            row = cursor.fetchone()
            query_History_insert = 'INSERT INTO history(email, time_stamp , operation) VALUES (%s, %s,%s)'
            cursor.execute(query_History_insert, (row[0] , current_timestamp, oper))
            conn.commit()
            conn.close()


        def check():
            self.count += 1
            if self.count > 4:
                messagebox.showinfo('Error', 'Your chances are completed. Please try after some time')
                enablepass_window.destroy()
                subprocess.run(["python", "sprint1.py"])
            else:
                authenticate()

        def restart_timer():
            self.start_time = time.time()

        def authenticate():
            if self.passEntry.get() == '':
                messagebox.showerror('Error', 'All Fields Are Required')
            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
                    cursor = conn.cursor()
                except:
                    messagebox.showerror('Error', 'Database Connectivity issue, Please Try Again')
                    return
                query = 'select password from temp'
                cursor.execute(query)
                row = cursor.fetchone()
                if time.time() - self.start_time < time_limit:
                    if row is None:
                        history("Database conn Error")
                        messagebox.showinfo('Error', "An Unexpected Error has been raised, please try again.")
                        window.destroy()
                        subprocess.run(["python", "sprint1.py"])
                    elif row[0] == self.passEntry.get():
                        sql = "SELECT start_time, end_time FROM admin"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        if result:
                            start= str(result[0]) 
                            end = str(result[1])
                            start_time=datetime.datetime.strptime(start, "%H:%M:%S").time()
                            end_time=datetime.datetime.strptime(end, "%H:%M:%S").time()
                            current_time = datetime.datetime.now().time()
                            if start_time <= current_time <= end_time:
                                command = r'reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBSTOR /v "Start" /t REG_DWORD /d 4 /f > nul'
                                subprocess.call(command, shell=True)
                                history("Disabled the usb port")
                                messagebox.showinfo('Success', 'USB PORT DISABLED SUCCESSFULLY')
                                # query = 'DELETE FROM temp'
                                # cursor.execute(query)
                                # conn.commit()
                                window.destroy()
                                subprocess.run(["python", "sprint1.py"])
                            else:
                                messagebox.showerror("Error", "You could'nt disable the usb port now.\n Plese Try with in the permitted time.")
                        else:
                            messagebox.showerror("Error", "Please contact admin to update the time limit.")                                
                    else:
                        history("Access Denied")
                        self.chances = 5 - self.count
                        messagebox.showinfo('Error', f'Incorrect Password. Please Try Again, You have only {self.chances} chances.')
                else:
                    history("Time limit Exceeded")
                    messagebox.showinfo('Error', "Time limit exceeded. Access denied.")
                    query = 'delete from temp'
                    cursor.execute(query)
                    conn.commit()
                conn.close()

        def resend():
            history("Password resend")
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
                cursor = conn.cursor()
            except:
                messagebox.showerror('Error', 'Database Connectivity issue, Please Try Again')
                return

            query = 'select email from temp '
            cursor.execute(query)
            row = cursor.fetchone()

            if row is None:
                messagebox.showinfo('Error', "An Unexpected Error has been raised, please try again.")
                window.destroy()
                subprocess.run(["python", "sprint1.py"])
            else:
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
                receiver_email = row[0]
                subject = 'Password for disabling the Usb port'
                message = 'Password to disable your usb port :' + password
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
                query = 'DELETE FROM temp'
                cursor.execute(query)
                conn.commit()
                query_insert = 'INSERT INTO temp(email, password) VALUES (%s, %s)'
                cursor.execute(query_insert, (row[0], password))
                conn.commit()
                conn.close()
                self.restart_timer()
                self.count=0
                
        def on_button_click():
            window.destroy()
            subprocess.run(["python", "authenticate1.py"]) 
        self.passLabel = tk.Label(window, text='Password:', font=('arial', 12, 'bold'), bg='black', fg='cyan')
        self.passLabel.place(x=550, y=190)

        self.passEntry = tk.Entry(window, width=30, bg='LightSkyBlue1', fg='black', font=('arial', 11, 'bold'), bd=3)
        self.passEntry.place(x=560, y=230)
        tk.Frame(window, width=240, height=2, bg='black').place(x=560, y=253)
        self.count=0
        self.submitButton = tk.Button(window, text='DISABLE', font=('Open Sans', 16, 'bold'), bd=5, bg='cyan', fg='black',
                                    cursor='hand2', activebackground='black', activeforeground='cyan', width=15, command=check)
        self.submitButton.place(x=580, y=290)
        self.timer_label = tk.Label(window, text='Expires in:30 sec', font=('arial', 10, 'italic'), bg='black', fg='cyan')
        self.timer_label.place(x=750, y=262)

        self.newaccountButton = tk.Button(window, text="Didn't receive password? RESEND", font=('Open Sans', 9, 'bold underline'),
                                          fg='cyan', bg='black', activeforeground='cyan', activebackground='black', cursor='hand2', bd=0, command=resend)
        self.newaccountButton.place(x=660, y=346)

        self.backButton = tk.Button(window, text='Back', font=('Open Sans', 16, 'bold'), bd=0, bg='cyan', fg='black',
                                      cursor='hand2', activebackground='black', activeforeground='cyan',  command=on_button_click)
        self.backButton.place(x=20, y=20)
        update_timer()
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
        self.window.after(50, self.update)

    def restart_timer(self):
        self.start_time = time.time()


root = tk.Tk()
video_source = 'disable.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
