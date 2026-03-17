from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecret"

reminders = []



patient_profile = {}
# -------------------- LOGIN --------------------
@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "admin@gmail.com" and password == "1234":
            return redirect(url_for('profile'))
        else:
            error = "Invalid credentials! Try admin@gmail.com / 1234"
    return render_template('login.html', error=error)

# -------------------- PROFILE --------------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global patient_profile
    if request.method == 'POST':
        patient_profile = {
            "name": request.form.get("name"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "contact": request.form.get("contact")
        }
        flash("✅ Profile saved successfully!")
        return redirect(url_for('dashboard'))
    return render_template('profile.html')

# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', profile=patient_profile)

# -------------------- ADD REMINDER --------------------
@app.route('/add_reminder', methods=['GET', 'POST'])
def add_reminder():
    if request.method == 'POST':
        medicine = request.form.get("medicine")
        dosage = request.form.get("dosage")
        time = request.form.get("time")
        duration = request.form.get("duration")

        reminders.append({
            "medicine": medicine,
            "dosage": dosage,
            "time": time,
            "duration": duration
        })

        flash(f"✅ Reminder added for {medicine}")
        return redirect(url_for('view_reminders'))

    return render_template('add_reminder.html')

# -------------------- VIEW ALL REMINDERS --------------------
@app.route('/reminders')
def view_reminders():
    return render_template('reminders.html', reminders=reminders)

# -------------------- EXPIRED MEDICINES --------------------
@app.route('/expired')
def expired():
    return render_template('expired.html')

# -------------------- UPLOAD FOR EXPIRY DETECTION --------------------
@app.route('/upload_medicine', methods=['GET', 'POST'])
def upload_medicine():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            flash("✅ File uploaded successfully (Expiry detection not implemented yet)")
            return redirect(url_for('dashboard'))
    return render_template('upload_medicine.html')

if __name__ == '__main__':
    app.run(debug=True)