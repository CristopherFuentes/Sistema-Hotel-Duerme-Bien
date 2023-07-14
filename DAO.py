import mysql.connector
from credencial import get_credenciales
from tkinter import messagebox


class Room:
    def __init__(self, room_number, max_guests, room_type):
        self.room_number = room_number
        self.max_guests = max_guests
        self.room_type = room_type
        self.guests = []  # Variable para almacenar los huéspedes

    def add_guest(self, guest):
        if len(self.guests) < self.max_guests:
            self.guests.append(guest)
            return True
        else:
            return False

    def remove_guest(self, guest):
        if guest in self.guests:
            self.guests.remove(guest)


class Guest:
    def __init__(self, name, rut, room_number, room_type):
        self.name = name
        self.rut = rut
        self.room_number = room_number
        self.room_type = room_type


class HotelDAO:
    def __init__(self):
        credentials = get_credenciales()
        self.conn = mysql.connector.connect(**credentials)

    def add_room(self, room):
        cursor = self.conn.cursor()
        query = "SELECT COUNT(*) FROM rooms WHERE room_number = %s"
        values = (room.room_number,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        count = result[0]

        if count > 0:
            messagebox.showerror("Error", "El número de habitación ya existe.")
            return

        query = "INSERT INTO rooms (room_number, max_guests, room_type) VALUES (%s, %s, %s)"
        values = (room.room_number, room.max_guests, room.room_type)
        cursor.execute(query, values)
        self.conn.commit()

    def add_guest(self, guest):
        cursor = self.conn.cursor()
        query = "INSERT INTO guests (name, rut, room_number, room_type) VALUES (%s, %s, %s, %s)"
        values = (guest.name, guest.rut, guest.room_number, guest.room_type)
        cursor.execute(query, values)
        self.conn.commit()

    def get_rooms(self):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM rooms"
        cursor.execute(query)
        rows = cursor.fetchall()
        rooms = []
        for row in rows:
            room = Room(row['room_number'], row['max_guests'], row['room_type'])
            rooms.append(room)
        return rooms

    def get_guests_by_room(self, room_number):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM guests WHERE room_number = %s"
        values = (room_number,)
        cursor.execute(query, values)
        rows = cursor.fetchall()
        guests = []
        for row in rows:
            guest = Guest(row['name'], row['rut'], row['room_number'], row['room_type'])
            guests.append(guest)
        return guests

    def close(self):
        self.conn.close()
