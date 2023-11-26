import cv2
import face_recognition
import tkinter as tk
from tkinter import Label, Entry, Button


class FaceRegistrationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng ký khuôn mặt")

        self.name_label = Label(self.master, text="Tên:")
        self.name_label.pack()

        self.name_entry = Entry(self.master)
        self.name_entry.pack()

        self.email_label = Label(self.master, text="Email:")
        self.email_label.pack()

        self.email_entry = Entry(self.master)
        self.email_entry.pack()

        self.register_button = Button(self.master, text="Đăng ký", command=self.register_face)
        self.register_button.pack()

        self.login_button = Button(self.master, text="Đăng nhập", command=self.login_face)
        self.login_button.pack()

        self.known_face_encodings = []
        self.known_face_names = []

    def register_face(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            print("Vui lòng nhập đầy đủ thông tin.")
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

        # Lưu thông tin và khuôn mặt vào cơ sở dữ liệu hoặc tập tin
        self.save_registration_info(name, email, face_encoding)

    def save_registration_info(self, name, email, face_encoding):
        # Ở đây, bạn có thể lưu thông tin và khuôn mặt vào cơ sở dữ liệu hoặc tập tin
        # Trong ví dụ này, tôi chỉ in ra để minh họa
        print(f"Đã đăng ký khuôn mặt cho {name} với email {email}.")
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)

    def login_face(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Login Face', frame)

            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                # So sánh với các khuôn mặt đã đăng ký
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    print(f"Đăng nhập thành công với tên: {name}")
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    app = FaceRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
