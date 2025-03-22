from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    patients = c.fetchall()
    c.execute('SELECT * FROM appointments')
    appointments = c.fetchall()
    conn.close()
    return render_template('index.html', patients=patients, appointments=appointments)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute('INSERT INTO patients (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()
        return "Patient added to database!"
    return render_template('add_patient.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        # Validate patient_id
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = c.fetchone()
        if not patient:
            conn.close()
            return "Error: Patient ID does not exist!"
        # If valid, save the appointment
        c.execute('INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)', 
                  (patient_id, doctor_id, date))
        conn.commit()
        conn.close()
        return "Appointment booked!"
    return render_template('book_appointment.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)