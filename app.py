from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(_name_)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="health_tracker"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metrics ORDER BY created_at DESC")
    metrics = cursor.fetchall()
    return render_template('dashboard.html', metrics=metrics)

@app.route('/add-metric', methods=['POST'])
def add_metric():
    blood_pressure = request.form['bloodPressure']
    blood_sugar = request.form['bloodSugar']
    heart_rate = request.form['heartRate']

    if not blood_pressure or not blood_sugar or not heart_rate:
        flash("All fields are required!")
        return redirect('/')

    cursor = db.cursor()
    query = """
        INSERT INTO metrics (blood_pressure, blood_sugar, heart_rate)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (blood_pressure, blood_sugar, heart_rate))
    db.commit()
    flash("Metric added successfully!")
    return redirect('/dashboard')

if _name_ == '_main_':
    app.run(debug=True)