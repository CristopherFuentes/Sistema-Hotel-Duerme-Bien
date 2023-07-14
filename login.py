import tkinter as tk
from tkinter import messagebox


class LoginApp:
    def __init__(self, root, on_login):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.on_login = on_login

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.username_label = tk.Label(root, text="Usuario:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Contraseña:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Iniciar Sesión", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese el usuario y la contraseña.")
            return

        if self.on_login(username, password):
            self.root.destroy()


def run_login(on_login):
    root = tk.Tk()
    login_app = LoginApp(root, on_login)
    root.mainloop()
