import cv2
import face_recognition
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import sqlite3
import json

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('registration.db')

def authenticate_face(name):
    if not name:
        print("Vui lòng nhập tên đăng nhập.")
        return

    # Tìm thông tin và khuôn mặt tương ứng với tên đăng nhập
    registration_info = get_registration_info(name)

    if registration_info is None:
        messagebox.showerror("Lỗi", "Tài khoản không tồn tại.")
        return

    known_encoding = registration_info['face_encoding']

    cap = cv2.VideoCapture(0)
    authentication_successful = False

    while True:
        ret, frame = cap.read()

        # Nhận diện khuôn mặt từ video
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            results = face_recognition.compare_faces([known_encoding], face_encoding)

            if results[0]:
                authentication_successful = True
                break

        cv2.imshow('Face Authentication', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if authentication_successful:
        show_login_success_screen(registration_info['name'])
    else:
        messagebox.showerror("Lỗi", "Xác thực khuôn mặt thất bại.")

def show_registration_screen():
    registration_screen = tk.Toplevel(root)
    registration_screen.title("Đăng ký khuôn mặt")

    name_label = Label(registration_screen, text="Tên:")
    name_label.pack()

    name_entry = Entry(registration_screen)
    name_entry.pack()

    register_button = Button(registration_screen, text="Đăng ký", command=lambda: register_face(name_entry.get()))
    register_button.pack()

def register_face(name):
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

def get_registration_info(name):
    cursor = conn.execute('SELECT name, face_encoding FROM registrations WHERE name = ?', (name,))
    row = cursor.fetchone()

    if row:
        face_encoding_str = row[1]
        face_encoding = json.loads(face_encoding_str)
        return {'name': row[0], 'face_encoding': face_encoding}
    else:
        return None

def show_login_success_screen(name):
    success_screen = tk.Toplevel(root)
    success_screen.title("Đăng nhập thành công")

    success_label = Label(success_screen, text=f"Chào mừng {name}, bạn đã đăng nhập thành công!", font=("Arial", 12))
    success_label.pack(pady=10)

    close_button = Button(success_screen, text="Đóng", command=success_screen.destroy)
    close_button.pack(pady=10)

# Giao diện người dùng chính
root = tk.Tk()
root.title("Đăng nhập - Đăng ký bằng khuôn mặt")

name_label = Label(root, text="Tên đăng nhập:")
name_label.pack()

name_entry = Entry(root)
name_entry.pack()

login_button = Button(root, text="Đăng nhập", command=lambda: authenticate_face(name_entry.get()))
login_button.pack()

register_button = Button(root, text="Đăng ký", command=show_registration_screen)
register_button.pack()

# Chạy giao diện người dùng
root.mainloop()

# Đóng kết nối cơ sở dữ liệu khi không sử dụng nữa
conn.close()
