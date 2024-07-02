import mysql.connector
from tkinter import *
from tkinter import messagebox, simpledialog
import random
import hashlib


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="260997",
    database="student_management"
)

cursor = db.cursor()

def generate_student_id():
    return random.randint(100000, 999999)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    first_name = entry_first_name.get()
    middle_name = entry_middle_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()
   
    if not first_name or not middle_name or not last_name or not email or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    hashed_password = hash_password(password)
    student_id = generate_student_id()

    try:
        cursor.execute("INSERT INTO users (first_name, middle_name, last_name, email, password, student_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, middle_name, last_name, email, hashed_password, student_id))
        db.commit()
        messagebox.showinfo("Success", f"Registration successful! Your student ID is: {student_id}")
        register_window.destroy()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Email already exists.")

def login():
    email = entry_login_email.get()
    password = entry_login_password.get()
   
    if not email or not password:
        messagebox.showerror("Error", "Email and Password are required.")
        return

    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user and user[5] == hashed_password:
        messagebox.showinfo("Success", "Login successful!")
        main_menu(user[0])
        login_window.destroy()
    else:
        messagebox.showerror("Error", "Invalid email or password.")

def forgot_password():
    email = entry_forgot_email.get()
    new_password = entry_new_password.get()
   
    if not email or not new_password:
        messagebox.showerror("Error", "Email and New Password are required.")
        return

    hashed_password = hash_password(new_password)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    if user:
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_password, email))
        db.commit()
        messagebox.showinfo("Success", "Password updated successfully.")
        forgot_password_window.destroy()
    else:
        messagebox.showerror("Error", "Email not found.")

def main_menu(user_id):
    main_window = Tk()
    main_window.title("Student Dashboard")
    main_window.geometry("300x200")
    main_window.configure(bg="#f0f0f0")

    Label(main_window, text="Welcome to the Student Dashboard!", bg="#f0f0f0", font=("Arial", 14)).pack(pady=10)

    Button(main_window, text="View Timetable", command=lambda: view_timetable(user_id), width=20, bg="#4CAF50", fg="white").pack(pady=5)
    Button(main_window, text="Manage Attendance", command=lambda: manage_attendance(user_id), width=20, bg="#4CAF50", fg="white").pack(pady=5)
    Button(main_window, text="View Circulars", command=view_circulars, width=20, bg="#4CAF50", fg="white").pack(pady=5)

    main_window.mainloop()

def view_timetable(user_id):
    cursor.execute("SELECT timetable FROM timetables WHERE student_id=%s", (user_id,))
    timetable = cursor.fetchone()
    if timetable:
        messagebox.showinfo("Timetable", f"Your Timetable: {timetable[0]}")
    else:
        messagebox.showinfo("Timetable", "No timetable found.")

def manage_attendance(user_id):
    attendance_window = Tk()
    attendance_window.title("Manage Attendance")
    attendance_window.geometry("300x150")
    attendance_window.configure(bg="#f0f0f0")

    Button(attendance_window, text="Mark Attendance", command=lambda: mark_attendance(user_id), width=20, bg="#4CAF50", fg="white").pack(pady=5)
    Button(attendance_window, text="View Attendance", command=lambda: view_attendance(user_id), width=20, bg="#4CAF50", fg="white").pack(pady=5)

    attendance_window.mainloop()

def mark_attendance(user_id):
    date = simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
    status = simpledialog.askstring("Input", "Enter status (Present/Absent):")
    if date and status:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                       (user_id, date, status))
        db.commit()
        messagebox.showinfo("Success", "Attendance marked successfully.")
    else:
        messagebox.showerror("Error", "Please provide both date and status.")

def view_attendance(user_id):
    cursor.execute("SELECT date, status FROM attendance WHERE student_id=%s", (user_id,))
    records = cursor.fetchall()
    record_str = "\n".join([f"Date: {record[0]}, Status: {record[1]}" for record in records])
    messagebox.showinfo("Attendance Records", record_str)

def view_circulars():
    cursor.execute("SELECT title, content FROM circulars WHERE active=1")
    circulars = cursor.fetchall()
    circular_str = "\n".join([f"Title: {circular[0]}, Content: {circular[1]}" for circular in circulars])
    messagebox.showinfo("Circulars", circular_str)

def open_register_window():
    global register_window, entry_first_name, entry_middle_name, entry_last_name, entry_email, entry_password
    register_window = Tk()
    register_window.title("Register")
    register_window.geometry("400x350")
    register_window.configure(bg="#f0f0f0")

    Label(register_window, text="First Name:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky=E)
    entry_first_name = Entry(register_window, width=30)
    
    entry_first_name.grid(row=0, column=1, padx=10, pady=5)

    Label(register_window, text="Middle Name:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky=E)
    entry_middle_name = Entry(register_window, width=30)
    entry_middle_name.grid(row=1, column=1, padx=10, pady=5)

    Label(register_window, text="Last Name:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky=E)
    entry_last_name = Entry(register_window, width=30)
    entry_last_name.grid(row=2, column=1, padx=10, pady=5)

    Label(register_window, text="Email:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky=E)
    entry_email = Entry(register_window, width=30)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    Label(register_window, text="Password:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky=E)
    entry_password = Entry(register_window, show='*', width=30)
    entry_password.grid(row=4, column=1, padx=10, pady=5)

    Button(register_window, text="Register", command=register, width=15, bg="#4CAF50", fg="white").grid(row=5, column=1, padx=10, pady=20, sticky=E)


def open_forgot_password_window():
    global forgot_password_window, entry_forgot_email, entry_new_password
    forgot_password_window = Tk()
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("400x200")
    forgot_password_window.configure(bg="#f0f0f0")

    Label(forgot_password_window, text="Email:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky=E)
    entry_forgot_email = Entry(forgot_password_window, width=30)
    entry_forgot_email.grid(row=0, column=1, padx=10, pady=5)

    Label(forgot_password_window, text="New Password:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky=E)
    entry_new_password = Entry(forgot_password_window, show='*', width=30)
    entry_new_password.grid(row=1, column=1, padx=10, pady=5)

    Button(forgot_password_window, text="Submit", command=forgot_password, width=15, bg="#4CAF50", fg="white").grid(row=2, column=1, padx=10, pady=20, sticky=E)


login_window = Tk()
login_window.title("Login")
login_window.geometry("400x250")
login_window.configure(bg="#f0f0f0")

Label(login_window, text="Email:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky=E)
entry_login_email = Entry(login_window, width=30)
entry_login_email.grid(row=0, column=1, padx=10, pady=10)

Label(login_window, text="Password:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky=E)
entry_login_password = Entry(login_window, show='*', width=30)
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

Button(login_window, text="Login", command=login, width=15, bg="#4CAF50", fg="white").grid(row=2, column=1, padx=10, pady=10, sticky=E)
Button(login_window, text="Register", command=open_register_window, width=15, bg="#4CAF50", fg="white").grid(row=3, column=1, padx=10, pady=10, sticky=E)
Button(login_window, text="Forgot Password", command=open_forgot_password_window, width=15, bg="#4CAF50", fg="white").grid(row=4, column=1, padx=10, pady=10, sticky=E)

login_window.mainloop()