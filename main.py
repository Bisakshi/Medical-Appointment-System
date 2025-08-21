import ttkbootstrap as tb
from ttkbootstrap.constants import *
from db import create_tables
import patient
import admin

# Ensure database tables exist
create_tables()

# Main window
root = tb.Window(themename="superhero")
root.title("Medical Appointment System")
root.geometry("500x350")

# Title
tb.Label(root, text="Welcome to Medical Appointment System", font=("Arial", 16)).pack(pady=20)

# ---------------- Patient Portal Button ----------------
tb.Button(root, text="Patient Portal", bootstyle=PRIMARY, command=patient.run).pack(pady=10)

# ---------------- Doctor Portal Button ----------------
tb.Button(root, text="Doctor Portal", bootstyle=SUCCESS, command=admin.run).pack(pady=10)

# Footer
tb.Label(root, text="Developed for Final Year Project", font=("Arial", 10, "italic")).pack(side="bottom", pady=10)

root.mainloop()