import os, shutil
import schedule
import time
import threading
from tkinter import *
import customtkinter as ctk
import customtkinter
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  

window = ctk.CTk()
window.geometry("400x400")
window.title("Filer")
window.config(background="#00FFFF")


frame = customtkinter.CTkFrame(window, corner_radius=35,bg_color="#00FFFF")
frame.pack(pady=40,padx=20,fill="both",expand=True)

label = customtkinter.CTkLabel(frame, text="📂 Filer", font=('Arial',28,'bold'))
label.pack(pady=(20,10))

path1 = ""

def directory():
    global path1
    path1 = entry.get()

    if os.path.exists(path1):
        folders = ["Image files","document files","text files","CAD files"]

        for folder in folders:
            folder_path = os.path.join(path1, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
    else:
        messagebox.showerror("Error", "The folder path provided does not exist.")

entry = customtkinter.CTkEntry(frame,width=250,height=40,placeholder_text="Enter folder path...",font=("ariel",20,"bold"))
entry.pack(pady=10)

def Images():
    for file in os.listdir(path1):
        if file.endswith((".png", ".jpg")):
            shutil.move(os.path.join(path1, file),
                        os.path.join(path1, "Image files", file))

def documents():
    for file in os.listdir(path1):
        if file.endswith((".exe", ".xlsx")):
            shutil.move(os.path.join(path1, file),
                        os.path.join(path1, "document files", file))

def text():
    for file in os.listdir(path1):
        if file.endswith((".txt", ".docx")):
            shutil.move(os.path.join(path1, file),
                        os.path.join(path1, "text files", file))

def CAD():
    for file in os.listdir(path1):
        if file.endswith((".step", ".FCStd")):
            shutil.move(os.path.join(path1, file),
                        os.path.join(path1, "CAD files", file))

def enter():
    if path1 == "":
        status.configure(text="❌ No folder selected")
        messagebox.showerror("Error", "Enter a folder path first!")
        return
    status.configure(text="⏳ Sorting...")
    Images()
    documents()
    text()
    CAD()
    status.configure(text="✅ Sorting Complete")

def EVERY_HOUR():
    schedule.every().hour.do(enter)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

button1 = customtkinter.CTkButton(frame, text="Auto sort (Hourly)",
                width=200,
                height=40,
                fg_color="orange",
                command=EVERY_HOUR)
button1.pack(pady=10)
button2 = customtkinter.CTkButton(frame, text="Set Folder",
                width=200,
                height=40,
                command=directory)
button2.pack(pady=5)

button3 = customtkinter.CTkButton(frame, text="Sort Now",
                width=200,
                height=40,
                fg_color="green",
                command=enter)
button3.pack(pady=5)

status = customtkinter.CTkLabel(frame,text="Status: Waiting...",text_color="gray")
status.pack(pady=10)

window.mainloop()
