from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import cv2
import face_recognition
import json
import sqlite3

global name_entry
conn = sqlite3.connect('registration.db')

def show_registration_screen():
    global registration_screen, name_entry
    registration_screen = Toplevel(screen1)
    name_entry = Entry(registration_screen)
    name_entry.pack()

    register_button = Button(registration_screen, text="Đăng ký", command=lambda: register_face).pack()
    register_button.pack()

def register_face():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Lỗi", "Vui lòng nhập tên.")
        return

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Register Face', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    face_encoding = face_recognition.face_encodings(frame)[0]

    # Đăng ký người dùng mới và lưu thông tin vào cơ sở dữ liệu
    register_user(name, face_encoding)

    messagebox.showinfo("Thông báo", "Đăng ký thành công!")
def register_user(name, face_encoding):
    encoded_face_str = json.dumps(face_encoding.tolist())
    conn.execute('INSERT INTO registrations (name, face_encoding) VALUES (?, ?)', (name, encoded_face_str))
    conn.commit()


def register_normal():
    global screen1, username, password, email, email_entry, username_entry, password_entry
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("350x250")

    username = StringVar()
    password = StringVar()
    email = StringVar()

    Label(screen1, text="Please enter details below").pack()
    Label(screen1, text="").pack()
    Label(screen1, text="Username * ").pack()

    username_entry = Entry(screen1, textvariable=username)
    username_entry.pack()
    Label(screen1, text="Password * ").pack()
    password_entry = Entry(screen1, textvariable=password, show="*")
    password_entry.pack()
    Label(screen1, text="email").pack()
    email_entry = Entry(screen1, textvariable=email)
    email_entry.pack()
    Label(screen1, text="").pack()
    Button(screen1, text="Register", width=10, height=1, command=register_user).pack()

def show_success_screen():
    success_screen = Toplevel(screen2)
    success_screen.title("Đăng nhập thành công")

    success_label = Label(success_screen, text="Chào mừng bạn đã đăng nhập thành công!", font=("Calibri", 12))
    success_label.pack(pady=10)

    close_button = Button(success_screen, text="Đóng", command=success_screen.destroy)
    close_button.pack(pady=10)

    success_screen.mainloop()

def register_user():
    screen3 = Toplevel(screen1)
    screen3.geometry("250x100")
    Label(screen3, text="registration succes", fg="green", font=("calibri", 11)).pack()

    username_info = username.get()
    password_info = password.get()
    email_sent = email.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info + "\n")
    file.write(email_sent)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(screen1, text="Registration Sucess", fg="green", font=("calibri", 11)).pack()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            Label(screen2, text="login success").pack()
            # screen2.destroy()
            # screen.destroy()
        else:
            Label(screen2, text="Wrong pass").pack()
    else:
        Label(screen2, text="user not found").pack()

def register():
    global screen1
    screen1 = Tk()
    screen1.title("Register")
    screen1.geometry("350x250")

    Button(screen1, text="Register by normal", width=20, height=1, command=register_normal).pack()
    Button(screen1, text="Register by face-id", width=20, height=1, command=show_registration_screen).pack()

def login():
    global screen2, username_verify, password_verify, username_entry1, password_entry1
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("350x250")
    Label(screen2, text="Please enter details below to login").pack()
    Label(screen2, text="").pack()

    username_verify = StringVar()
    password_verify = StringVar()

    username_entry1 = Entry(screen2, textvariable=username_verify)
    username_entry1.pack()
    Label(screen2, text="").pack()
    Label(screen2, text="Password * ").pack()
    password_entry1 = Entry(screen2, textvariable=password_verify)
    password_entry1.pack()
    Label(screen2, text="").pack()
    Button(screen2, text="Face-id", width=10, height=1).pack()
    Button(screen2, text="Login", width=10, height=1, command=login_verify).pack()

def main_screen():
    global screen
    screen = Tk()
    screen.geometry("1280x720")
    screen.title("GAMELOL")
    bg = ImageTk.PhotoImage(file="bg1.webp")
    bg_image = Label(screen, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    screen.mainloop()

main_screen()
