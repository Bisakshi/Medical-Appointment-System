import ttkbootstrap as tb
from ttkbootstrap.constants import *
from db import connect_db

def run():
    win = tb.Toplevel()
    win.title("Patient Portal")
    win.geometry("400x500")
    
    tb.Label(win, text="Patient Registration", font=("Arial", 14)).pack(pady=10)
    
    # Entry fields
    entries = {}
    for field in ["Name", "Age", "Gender", "Contact", "Username", "Password"]:
        tb.Label(win, text=field+":").pack()
        ent = tb.Entry(win, show="*" if field=="Password" else None)
        ent.pack()
        entries[field] = ent
    
    def register():
        conn, cursor = connect_db()
        try:
            cursor.execute(
                "INSERT INTO patients (name, age, gender, contact, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                (entries["Name"].get(), entries["Age"].get(), entries["Gender"].get(), 
                 entries["Contact"].get(), entries["Username"].get(), entries["Password"].get())
            )
            conn.commit()
            tb.Label(win, text="Registered Successfully!", bootstyle=SUCCESS).pack()
        except:
            tb.Label(win, text="Username already exists!", bootstyle=DANGER).pack()
        finally:
            conn.close()
    
    tb.Button(win, text="Register", bootstyle=SUCCESS, command=register).pack(pady=10)
    
    tb.Label(win, text="---------------- OR ----------------").pack(pady=10)
    tb.Label(win, text="Patient Login", font=("Arial", 14)).pack(pady=10)
    
    login_entries = {}
    for field in ["Username", "Password"]:
        tb.Label(win, text=field+":").pack()
        ent = tb.Entry(win, show="*" if field=="Password" else None)
        ent.pack()
        login_entries[field] = ent
    
    def login():
        conn, cursor = connect_db()
        cursor.execute("SELECT id, name FROM patients WHERE username=? AND password=?",
                       (login_entries["Username"].get(), login_entries["Password"].get()))
        user = cursor.fetchone()
        conn.close()
        if user:
            tb.Label(win, text=f"Welcome {user[1]}!", bootstyle=SUCCESS).pack()
            patient_dashboard(user[0])
        else:
            tb.Label(win, text="Invalid Credentials!", bootstyle=DANGER).pack()
    
    tb.Button(win, text="Login", bootstyle=PRIMARY, command=login).pack(pady=10)
    
    def patient_dashboard(patient_id):
        dash = tb.Toplevel()
        dash.title("Patient Dashboard")
        dash.geometry("500x500")
        
        tb.Label(dash, text="Book an Appointment", font=("Arial", 14)).pack(pady=10)
        
        tb.Label(dash, text="Doctor ID:").pack()
        doctor_entry = tb.Entry(dash)
        doctor_entry.pack()
        tb.Label(dash, text="Date (YYYY-MM-DD):").pack()
        date_entry = tb.Entry(dash)
        date_entry.pack()
        tb.Label(dash, text="Time (HH:MM):").pack()
        time_entry = tb.Entry(dash)
        time_entry.pack()
        
        def book():
            conn, cursor = connect_db()
            cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                           (patient_id, doctor_entry.get(), date_entry.get(), time_entry.get()))
            conn.commit()
            conn.close()
            tb.Label(dash, text="Appointment Requested!", bootstyle=SUCCESS).pack()
        
        tb.Button(dash, text="Book Appointment", bootstyle=PRIMARY, command=book).pack(pady=10)
        
        tb.Label(dash, text="Your Appointments", font=("Arial", 14)).pack(pady=10)
        
        conn, cursor = connect_db()
        cursor.execute("SELECT id, doctor_id, date, time, status FROM appointments WHERE patient_id=?", (patient_id,))
        appointments = cursor.fetchall()
        conn.close()
        
        for appt in appointments:
            tb.Label(dash, text=f"ID:{appt[0]} | Doctor:{appt[1]} | {appt[2]} {appt[3]} | Status:{appt[4]}").pack()