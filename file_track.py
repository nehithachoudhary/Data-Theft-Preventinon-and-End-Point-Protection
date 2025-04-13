import os
import win32file
import win32con
import win32event
import wmi
import datetime
import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Define the action constants
FILE_ACTION_ADDED = 1
FILE_ACTION_REMOVED = 2
FILE_ACTION_MODIFIED = 3
FILE_ACTION_RENAMED_OLD_NAME = 4
FILE_ACTION_RENAMED_NEW_NAME = 5

def history(oper):
    current_timestamp = datetime.datetime.now()
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='root', database='login')
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror('Error', 'Database Connectivity issue, Please Try Again')
        return
    try:
        query = 'SELECT email FROM temp'
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            print("No email found in temp table.")
            return
        
        query_History_insert = 'INSERT INTO history(email, time_stamp, operation) VALUES (%s, %s, %s)'
        cursor.execute(query_History_insert, (row[0], current_timestamp, oper))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while inserting history: {err}")
    finally:
        conn.close()

def open_new_window(message):
    root.withdraw()  # Hide the main tkinter window
    new_window = tk.Toplevel(root)
    new_window.title("Notification")
    new_window.geometry("300x200")
    label = tk.Label(new_window, text=message)
    label.pack(pady=50)
    
    # Add a button to close the new window and re-show the main window if needed
    close_button = tk.Button(new_window, text="Close", command=lambda: (new_window.destroy(), root.deiconify()))
    close_button.pack(pady=20)

    root.after(2000, navigate_to_another_page)  # Navigate after 2 seconds

def navigate_to_another_page():
    root.withdraw()  # Hide the current window
    new_page = tk.Toplevel(root)
    new_page.title("New Page")
    new_page.geometry("400x300")
    label = tk.Label(new_page, text="This is the new page after USB activity.")
    label.pack(pady=100)
    
    close_button = tk.Button(new_page, text="Close", command=new_page.destroy)
    close_button.pack(pady=20)

def monitor_usb_drive(drive_path):
    directory_handle = win32file.CreateFile(
        drive_path,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    change_handle = win32file.FindFirstChangeNotification(
        drive_path,
        0,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
        win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
        win32con.FILE_NOTIFY_CHANGE_SIZE |
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
        win32con.FILE_NOTIFY_CHANGE_SECURITY
    )
    
    print(f"Monitoring changes on: {drive_path}")

    try:
        while True:
            result = win32event.WaitForSingleObject(change_handle, 500)  # Wait with a timeout
            if result == win32event.WAIT_OBJECT_0:
                win32file.FindNextChangeNotification(change_handle)
                changes = win32file.ReadDirectoryChangesW(
                    directory_handle,
                    1024,
                    True,
                    win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                    win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                    win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                    win32con.FILE_NOTIFY_CHANGE_SIZE |
                    win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                    win32con.FILE_NOTIFY_CHANGE_SECURITY,
                    None,
                    None
                )
                
                for action, file in changes:
                    full_filename = os.path.join(drive_path, file)
                    if action == FILE_ACTION_ADDED:
                        history(f"File created: {full_filename}")
                        print(f"File created: {full_filename}")
                    elif action == FILE_ACTION_REMOVED:
                        history(f"File deleted: {full_filename}")
                        print(f"File deleted: {full_filename}")
                    elif action == FILE_ACTION_MODIFIED:
                        history(f"File modified: {full_filename}")
                        print(f"File modified: {full_filename}")
                    elif action == FILE_ACTION_RENAMED_OLD_NAME:
                        history(f"File renamed from: {full_filename}")
                        print(f"File renamed from: {full_filename}")
                    elif action == FILE_ACTION_RENAMED_NEW_NAME:
                        history(f"File renamed to: {full_filename}")
                        print(f"File renamed to: {full_filename}")
                    else:
                        pass
            
            print("completed")
            # Check if the USB drive is still accessible
            if not os.path.exists(drive_path):
                print("completed")
                history(f"USB drive removed: {drive_path}")
                print(f"USB drive removed: {drive_path}")
                open_new_window("USB drive removed!")
                break

    finally:
        print(f"completed")
        win32file.FindCloseChangeNotification(change_handle)
        win32file.CloseHandle(directory_handle)

def detect_usb_drive():
    c = wmi.WMI()
    watcher = c.Win32_LogicalDisk.watch_for("creation")
    print("Waiting for USB drives to be connected...")
    while True:
        new_drive = watcher()
        drive_letter = new_drive.DeviceID
        if new_drive.Description == "Removable Disk":
            print(f"New USB drive detected: {drive_letter}")
            monitor_usb_drive(drive_letter + "\\")
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    detect_usb_drive()
    root.mainloop()  # Start the Tkinter event loop
