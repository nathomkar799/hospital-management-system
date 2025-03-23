from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS doctors 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, specialty TEXT)''')
    c.execute('INSERT OR IGNORE INTO doctors (id, name, specialty) VALUES (1, "Dr. Smith", "Cardiology")')
    c.execute('INSERT OR IGNORE INTO doctors (id, name, specialty) VALUES (2, "Dr. Jones", "Neurology")')
    c.execute('INSERT OR IGNORE INTO doctors (id, name, specialty) VALUES (3, "Dr. Brown", "Pediatrics")')
    c.execute('INSERT OR IGNORE INTO doctors (id, name, specialty) VALUES (4, "Dr. Taylor", "Orthopedics")')
    c.execute('INSERT OR IGNORE INTO doctors (id, name, specialty) VALUES (5, "Dr. Wilson", "Dermatology")')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    patients = c.fetchall()
    c.execute('''SELECT a.id, a.patient_id, p.name, a.doctor_id, a.date 
                 FROM appointments a 
                 JOIN patients p ON a.patient_id = p.id''')
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
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('SELECT * FROM doctors')
    doctors = c.fetchall()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        c.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = c.fetchone()
        if not patient:
            conn.close()
            return "Error: Patient ID does not exist!"
        c.execute('INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)', 
                  (patient_id, doctor_id, date))
        conn.commit()
        conn.close()
        return "Appointment booked!"
    conn.close()
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/cancel_appointment/<int:appt_id>')
def cancel_appointment(appt_id):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('DELETE FROM appointments WHERE id = ?', (appt_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)