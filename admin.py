import ttkbootstrap as tb
from ttkbootstrap.constants import *
from db import connect_db
from tkinter import ttk

def run():
    win = tb.Toplevel()
    win.title("Doctor Portal")
    win.geometry("600x650")
    
    # ---------------- Doctor Registration ----------------
    tb.Label(win, text="Doctor Registration", font=("Arial", 14)).pack(pady=10)
    
    reg_frame = tb.Frame(win)
    reg_frame.pack(pady=5)
    
    reg_entries = {}
    for field in ["Name", "Specialization", "Username", "Password"]:
        tb.Label(reg_frame, text=field+":").pack(pady=2)
        ent = tb.Entry(reg_frame, show="*" if field=="Password" else None)
        ent.pack(pady=2)
        reg_entries[field] = ent
    
    def register_doctor():
        conn, cursor = connect_db()
        try:
            cursor.execute(
                "INSERT INTO doctors (name, specialization, username, password) VALUES (?, ?, ?, ?)",
                (reg_entries["Name"].get(), reg_entries["Specialization"].get(),
                 reg_entries["Username"].get(), reg_entries["Password"].get())
            )
            conn.commit()
            tb.Label(win, text="Doctor Registered Successfully!", bootstyle=SUCCESS).pack(pady=5)
        except:
            tb.Label(win, text="Username already exists!", bootstyle=DANGER).pack(pady=5)
        finally:
            conn.close()
    
    tb.Button(win, text="Register Doctor", bootstyle=SUCCESS, command=register_doctor).pack(pady=10)
    
    tb.Label(win, text="---------------- OR ----------------").pack(pady=10)
    
    # ---------------- Doctor Login ----------------
    tb.Label(win, text="Doctor Login", font=("Arial", 14)).pack(pady=10)
    
    login_frame = tb.Frame(win)
    login_frame.pack(pady=5)
    
    login_entries = {}
    for field in ["Username", "Password"]:
        tb.Label(login_frame, text=field+":").pack(pady=2)
        ent = tb.Entry(login_frame, show="*" if field=="Password" else None)
        ent.pack(pady=2)
        login_entries[field] = ent
    
    def login():
        conn, cursor = connect_db()
        cursor.execute("SELECT id, name FROM doctors WHERE username=? AND password=?",
                       (login_entries["Username"].get(), login_entries["Password"].get()))
        user = cursor.fetchone()
        conn.close()
        if user:
            tb.Label(win, text=f"Welcome Dr.{user[1]}!", bootstyle=SUCCESS).pack(pady=5)
            doctor_dashboard(user[0])
        else:
            tb.Label(win, text="Invalid Credentials!", bootstyle=DANGER).pack(pady=5)
    
    tb.Button(win, text="Login", bootstyle=PRIMARY, command=login).pack(pady=10)
    
    # ---------------- Doctor Dashboard ----------------
    def doctor_dashboard(doctor_id):
        dash = tb.Toplevel()
        dash.title("Doctor Dashboard")
        dash.geometry("750x500")
        
        tb.Label(dash, text="Patient Appointments", font=("Arial", 14)).pack(pady=10)
        
        # Treeview table
        columns = ("ID", "Patient", "Date", "Time", "Status")
        tree = ttk.Treeview(dash, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(pady=10, fill="x")
        
        # Fetch appointments
        conn, cursor = connect_db()
        cursor.execute("""
            SELECT appointments.id, patients.name, date, time, status
            FROM appointments
            JOIN patients ON appointments.patient_id=patients.id
            WHERE doctor_id=?
        """, (doctor_id,))
        appointments = cursor.fetchall()
        conn.close()
        
        for appt in appointments:
            tree.insert("", "end", values=appt)
        
        # Approve / Cancel functions
        def approve():
            selected = tree.selection()
            if not selected:
                return
            appt_id = tree.item(selected[0])['values'][0]
            conn, cursor = connect_db()
            cursor.execute("UPDATE appointments SET status='Approved' WHERE id=?", (appt_id,))
            conn.commit()
            conn.close()
            # Update table
            current_values = list(tree.item(selected[0])['values'])
            current_values[4] = 'Approved'
            tree.item(selected[0], values=current_values)
        
        def cancel():
            selected = tree.selection()
            if not selected:
                return
            appt_id = tree.item(selected[0])['values'][0]
            conn, cursor = connect_db()
            cursor.execute("UPDATE appointments SET status='Cancelled' WHERE id=?", (appt_id,))
            conn.commit()
            conn.close()
            # Update table
            current_values = list(tree.item(selected[0])['values'])
            current_values[4] = 'Cancelled'
            tree.item(selected[0], values=current_values)
        
        # Buttons
        btn_frame = tb.Frame(dash)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="Approve Selected", bootstyle=SUCCESS, command=approve).pack(side="left", padx=10)
        tb.Button(btn_frame, text="Cancel Selected", bootstyle=DANGER, command=cancel).pack(side="left", padx=10)