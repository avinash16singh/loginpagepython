import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '01Avni10@',
    'database': 'acadmic_db'
}

def connect_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def initialize_database():
    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:

       
        connection.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Initialization Error", f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def register_admin(username, password):
    connection = connect_db()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        messagebox.showinfo("Registration Successful", "Admin registered successfully!")
        return True
    except mysql.connector.IntegrityError:
        messagebox.showerror("Registration Error", "Username already exists!")
        return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def login_admin(username, password):
    connection = connect_db()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        return bool(admin)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def open_dashboard():
    login_frame.destroy()
    dashboard()

def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if login_admin(username, password):
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

def open_register_form():
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        reg_no = reg_no_entry.get()

        if not username or not password or not email or not phone or not reg_no:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        connection = connect_db()
        if not connection:
            return

        cursor = connection.cursor()
        try:
            # Insert data into the admin table
            cursor.execute(
                "INSERT INTO admin (username, password, email, phone, reg_no) VALUES (%s, %s, %s, %s, %s)",
                (username, password, email, phone, reg_no),
            )
            connection.commit()
            messagebox.showinfo("Success", "Registration completed successfully!")
            register_window.destroy()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Registration Error", "Username or Registration Number already exists!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    # Create a new window for registration
    register_window = tk.Toplevel(root)
    register_window.title("Register New Admin")
    register_window.geometry("400x500")

    # Form fields
    tk.Label(register_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")  # Hides the password input
    password_entry.pack(pady=5)

    tk.Label(register_window, text="email").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)

    tk.Label(register_window, text="Phone Number").pack(pady=5)
    phone_entry = tk.Entry(register_window)
    phone_entry.pack(pady=5)

    tk.Label(register_window, text="Registration Number").pack(pady=5)
    reg_no_entry = tk.Entry(register_window)
    reg_no_entry.pack(pady=5)

    # Submit button
    tk.Button(register_window, text="Submit", command=submit_registration).pack(pady=20)

# Update handle_register to call open_register_form
def handle_register():
    open_register_form()



def dashboard():
    def clear_fields():
        # Clear all entry fields
        email_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        school_level_entry.delete(0, tk.END)
        grades_entry.delete(0, tk.END)
        hours_spent_entry.delete(0, tk.END)
        study_methods_entry.delete(0, tk.END)
        attendance_rate_entry.delete(0, tk.END)
        engagement_level_entry.delete(0, tk.END)
        motivation_entry.delete(0, tk.END)
        career_goals_entry.delete(0, tk.END)

    def add_entry():
        # Get data from entry fields
        data = (
            email_entry.get(), username_entry.get(), age_entry.get(), gender_entry.get(),
            school_level_entry.get(), grades_entry.get(), hours_spent_entry.get(),
            study_methods_entry.get(), attendance_rate_entry.get(), engagement_level_entry.get(),
            motivation_entry.get(), career_goals_entry.get()
        )

        # Connect to the database
        connection = connect_db()
        if not connection:
            return

        cursor = connection.cursor()
        query = """
        INSERT INTO acadmic_dbs (
            email, username, age, gender, Current_school_Level, Grades,
            Average_Hours_Spent_Studying_per_Day, Preferred_Study_Methods,
            Attendance_Rate, Engagement_Level_in_Class, Primary_Motivation_for_Studying,
            Future_Career_Goals
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, data)
            connection.commit()
            messagebox.showinfo("Success", "Entry added successfully!")
            clear_fields()  # Clear the input fields
            display_data()  # Display the updated data
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    def display_data():
        # This function fetches data from the database and displays it.
        connection = connect_db()
        if not connection:
            return

        cursor = connection.cursor()
        query = "SELECT * FROM acadmic_dbs"
        
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            
            # Clear any existing data from previous display
            for widget in dashboard_window.winfo_children():
                widget.grid_forget()

            # Display headers
            headers = ["Email", "Username", "Age", "Gender", "School Level", "Grades", "Hours Spent", "Study Methods", "Attendance", "Engagement", "Motivation", "Career Goals"]
            for col, header in enumerate(headers):
                tk.Label(dashboard_window, text=header).grid(row=0, column=col)
            
            # Display the fetched data in a grid format
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    tk.Label(dashboard_window, text=value).grid(row=i+1, column=j)
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    # Destroy the root window
    root.destroy()

    # Create a new window for the dashboard
    dashboard_window = tk.Tk()
    dashboard_window.title("Admin Dashboard")
    dashboard_window.geometry("900x600")

    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(dashboard_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Create Entry widgets for the dashboard
    email_label = tk.Label(dashboard_window, text="Email")
    email_label.grid(row=0, column=0)
    email_entry = tk.Entry(dashboard_window)
    email_entry.grid(row=0, column=1)

    username_label = tk.Label(dashboard_window, text="Username")
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(dashboard_window)
    username_entry.grid(row=1, column=1)

    age_label = tk.Label(dashboard_window, text="Age")
    age_label.grid(row=2, column=0)
    age_entry = tk.Entry(dashboard_window)
    age_entry.grid(row=2, column=1)

    gender_label = tk.Label(dashboard_window, text="Gender")
    gender_label.grid(row=3, column=0)
    gender_entry = tk.Entry(dashboard_window)
    gender_entry.grid(row=3, column=1)

    school_level_label = tk.Label(dashboard_window, text="Current School Level")
    school_level_label.grid(row=4, column=0)
    school_level_entry = tk.Entry(dashboard_window)
    school_level_entry.grid(row=4, column=1)

    grades_label = tk.Label(dashboard_window, text="Grades")
    grades_label.grid(row=5, column=0)
    grades_entry = tk.Entry(dashboard_window)
    grades_entry.grid(row=5, column=1)

    hours_spent_label = tk.Label(dashboard_window, text="Average Hours Spent Studying per Day")
    hours_spent_label.grid(row=6, column=0)
    hours_spent_entry = tk.Entry(dashboard_window)
    hours_spent_entry.grid(row=6, column=1)

    study_methods_label = tk.Label(dashboard_window, text="Preferred Study Methods")
    study_methods_label.grid(row=7, column=0)
    study_methods_entry = tk.Entry(dashboard_window)
    study_methods_entry.grid(row=7, column=1)

    attendance_rate_label = tk.Label(dashboard_window, text="Attendance Rate")
    attendance_rate_label.grid(row=8, column=0)
    attendance_rate_entry = tk.Entry(dashboard_window)
    attendance_rate_entry.grid(row=8, column=1)

    engagement_level_label = tk.Label(dashboard_window, text="Engagement Level in Class")
    engagement_level_label.grid(row=9, column=0)
    engagement_level_entry = tk.Entry(dashboard_window)
    engagement_level_entry.grid(row=9, column=1)

    motivation_label = tk.Label(dashboard_window, text="Primary Motivation for Studying")
    motivation_label.grid(row=10, column=0)
    motivation_entry = tk.Entry(dashboard_window)
    motivation_entry.grid(row=10, column=1)

    career_goals_label = tk.Label(dashboard_window, text="Future Career Goals")
    career_goals_label.grid(row=11, column=0)
    career_goals_entry = tk.Entry(dashboard_window)
    career_goals_entry.grid(row=11, column=1)

    # Button to add entry
    tk.Button(dashboard_window, text="Add Entry", command=add_entry).grid(row=12, column=0, columnspan=2)

    dashboard_window.mainloop()

initialize_database()

root = tk.Tk()
root.title("Admin Login/Register")
root.geometry("400x300")

login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Username").pack()
username_entry = tk.Entry(login_frame)
username_entry.pack()

tk.Label(login_frame, text="Password").pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

tk.Button(login_frame, text="Login", command=handle_login).pack(pady=10)
tk.Button(login_frame, text="Register", command=handle_register).pack(pady=10)

root.mainloop()

