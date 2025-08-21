import sqlite3

def connect_db():
    conn = sqlite3.connect("medical_appointments.db")
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    conn, cursor = connect_db()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, age INTEGER, gender TEXT, contact TEXT,
                        username TEXT UNIQUE, password TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, specialization TEXT,
                        username TEXT UNIQUE, password TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        doctor_id INTEGER,
                        date TEXT,
                        time TEXT,
                        status TEXT DEFAULT 'Pending',
                        FOREIGN KEY(patient_id) REFERENCES patients(id),
                        FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
    
    conn.commit()
    conn.close()

# Initialize database
if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")