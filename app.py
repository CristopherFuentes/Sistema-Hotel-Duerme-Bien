import tkinter as tk
from tkinter import messagebox
from DAO import HotelDAO, Room, Guest
from login import run_login


class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel App")
        self.rooms = []
        self.guests = []
        self.dao = HotelDAO()

        self.room_number_var = tk.StringVar()
        self.guest_name_var = tk.StringVar()
        self.guest_rut_var = tk.StringVar()
        self.room_type_var = tk.StringVar()
        self.room_type_var.set("Grande")  # Valor predeterminado del tipo de habitación

        self.room_number_label = tk.Label(root, text="Número de habitación:")
        self.room_number_label.pack()
        self.room_number_entry = tk.Entry(root, textvariable=self.room_number_var)
        self.room_number_entry.pack()

        self.guest_name_label = tk.Label(root, text="Nombre del huésped:")
        self.guest_name_label.pack()
        self.guest_name_entry = tk.Entry(root, textvariable=self.guest_name_var)
        self.guest_name_entry.pack()

        self.guest_rut_label = tk.Label(root, text="RUT del huésped:")
        self.guest_rut_label.pack()
        self.guest_rut_entry = tk.Entry(root, textvariable=self.guest_rut_var)
        self.guest_rut_entry.pack()

        self.room_type_label = tk.Label(root, text="Tipo de habitación:")
        self.room_type_label.pack()
        self.room_type_entry = tk.OptionMenu(root, self.room_type_var, "Grande", "Mediano", "Pequeño")
        self.room_type_entry.pack()

        self.register_button = tk.Button(root, text="Registrar", command=self.register_guest)
        self.register_button.pack()

        self.summary_button = tk.Button(root, text="Resumen", command=self.show_summary)
        self.summary_button.pack()

    def register_guest(self):
        room_number = self.room_number_var.get()
        guest_name = self.guest_name_var.get()
        guest_rut = self.guest_rut_var.get()
        room_type = self.room_type_var.get()

        if not room_number or not guest_name or not guest_rut or not room_type:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        room = self.get_room_by_number(int(room_number))
        if not room:
            max_guests = 0
            if room_type == "Grande":
                max_guests = 3
            elif room_type == "Mediano":
                max_guests = 2
            elif room_type == "Pequeño":
                max_guests = 1
            room = Room(int(room_number), max_guests, room_type)
            self.dao.add_room(room)
            self.rooms.append(room)

        if len(room.guests) >= room.max_guests:
            messagebox.showerror("Error", "La habitación está llena. Por favor, elija otra habitación.")
            return

        guest = Guest(guest_name, guest_rut, room_number, room_type)  # Agregar el número de habitación
        self.dao.add_guest(guest)
        self.guests.append(guest)

        if room.add_guest(guest):
            messagebox.showinfo("Registro Exitoso", "El huésped se ha registrado correctamente.")
        else:
            messagebox.showinfo("Registro Exitoso", "El huésped se ha registrado correctamente, se ha asignado otra habitación debido al límite de pasajeros.")

        self.clear_fields()

    def get_room_by_number(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None

    def clear_fields(self):
        self.room_number_var.set("")
        self.guest_name_var.set("")
        self.guest_rut_var.set("")
        self.room_type_var.set("Grande")

    def show_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Resumen de Habitaciones")

        summary_table = tk.Label(summary_window, text="Habitación \t Pasajeros \t RUT \t Tipo")
        summary_table.pack()

        for room in self.rooms:
            guests = self.dao.get_guests_by_room(room.room_number)
            if guests:
                for guest in guests:
                    room_summary = f"{room.room_number}\t{guest.name}\t{guest.rut}\t{guest.room_type}"
                    room_summary_label = tk.Label(summary_window, text=room_summary)
                    room_summary_label.pack()
            else:
                room_summary = f"{room.room_number}\tVacante\t\t{room.room_type}"
                room_summary_label = tk.Label(summary_window, text=room_summary)
                room_summary_label.pack()


def validate_login(username, password):
    # Implementa tu lógica de validación de inicio de sesión aquí
    # Verifica si los campos no están vacíos y si el usuario y contraseña son correctos
    if not username or not password:
        messagebox.showerror("Error", "Por favor, ingrese el usuario y la contraseña.")
        return False

    if username == "admin" and password == "admin123":
        return True
    else:
        messagebox.showerror("Error", "Usuario y/o contraseña incorrectos.")
        return False


def on_login(username, password):
    if validate_login(username, password):
        root = tk.Toplevel()
        app = HotelApp(root)


def run_app():
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_login(on_login)
    run_app()
