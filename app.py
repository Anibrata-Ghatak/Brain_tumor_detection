from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.units import mm
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
import qrcode
import numpy as np
import os


# --- App Config ---
app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = './uploads'
REPORT_FOLDER = './static/reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

# --- Load Model ---
model = load_model('models/model (1).h5')
class_labels = ['pituitary', 'glioma', 'notumor', 'meningioma']

# --- Prediction Function ---
def predict_tumor(image_path):
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    index = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    label = class_labels[index]
    return ("No Tumor" if label == "notumor" else f"Tumor: {label}"), confidence

# --- Enhanced PDF Report Generator ---
def generate_pdf_report(filename, prediction, confidence, image_path, name, age, gender):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    import qrcode
    import os
    from datetime import datetime

    path = os.path.join(REPORT_FOLDER, filename)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # --- Offwhite Background ---
    c.setFillColorRGB(0.98, 0.96, 0.92)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # --- Header Image with Title (changed from .jpg to .jpeg) ---
    header_img_path = os.path.abspath("static/images/hospital_image.jpg")
    if os.path.exists(header_img_path):
        c.drawImage(header_img_path, 0, height - 120, width=width, height=100, mask='auto')
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 70, "MRI Brain Tumor Analysis Report")

    # --- Date ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 135, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Patient Details Box ---
    c.setFillColorRGB(0.9, 0.95, 1)
    c.roundRect(40, height - 210, width - 80, 60, 10, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(55, height - 185, "Patient Information")
    c.setFont("Helvetica", 11)
    c.drawString(60, height - 200, f"Name: {name}    Age: {age}    Gender: {gender}")

    # --- Diagnosis Box ---
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(40, height - 290, width - 80, 60, 10, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(55, height - 265, "AI Diagnosis")
    c.setFont("Helvetica", 11)
    c.drawString(60, height - 280, f"Prediction: {prediction}    Confidence: {confidence * 100:.2f}%")

    # --- MRI Image (centered) ---
    if os.path.exists(image_path):
        mri_x = (width - 200) / 2
        mri_y = height - 590  # shifted down to prevent overlap
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, mri_y + 220, "MRI Scan Image:")
        try:
            c.drawImage(image_path, mri_x, mri_y, width=200, height=200, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            c.setFillColor(colors.red)
            c.drawString(50, mri_y, f"Error loading image: {e}")

    # --- Doctor Signature ---
    sig_path = os.path.abspath("static/images/doctor signature.png")
    if os.path.exists(sig_path):
        c.setFont("Helvetica", 10)
        c.drawString(width - 180, 160, "Dr. Sourendranath Roy")
        c.drawString(width - 180, 145, "Chief Radiologist")
        c.drawImage(sig_path, width - 190, 180, width=100, height=40, mask='auto')

    # --- QR Code ---
    qr_data = f"Name: {name}, Age: {age}, Gender: {gender}, Result: {prediction}, Confidence: {confidence:.2f}"
    qr_img = qrcode.make(qr_data)
    qr_path = os.path.join(REPORT_FOLDER, "qr_temp.png")
    qr_img.save(qr_path)
    if os.path.exists(qr_path):
        c.drawImage(qr_path, 60, 80, width=70, height=70, mask='auto')
        os.remove(qr_path)

    # --- Footer Info ---
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(140, 95, "Contact: +91-9876543210 | Lifecare Diagnostics, Kolkata")

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawString(140, 80, "Disclaimer: This is an AI-generated report. Please consult a certified doctor.")

    c.save()
    return path

# --- Signup Route ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        try:
            cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (uname, passwd))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return render_template('signup.html', error='Username already exists')

    return render_template('signup.html')

# --- Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (uname, passwd))
        user = cur.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

# --- Home Route ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')

    if request.method == 'POST':
        file = request.files.get('file')
        name = request.form.get('patient_name', 'Unknown')
        age = request.form.get('patient_age', 'Unknown')
        gender = request.form.get('patient_gender', 'Unknown')

        if file:
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            prediction, confidence = predict_tumor(img_path)
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            report_path = generate_pdf_report(report_name, prediction, confidence, img_path, name, age, gender)

            return render_template('index.html',
                result=prediction,
                confidence=f"{confidence * 100:.2f}%",
                file_path=url_for('uploaded_file', filename=filename),
                report_path=url_for('static', filename=f'reports/{report_name}'),
                patient_name=name,
                patient_age=age,
                patient_gender=gender,
                year=datetime.now().year
            )

    return render_template('index.html', result=None, year=datetime.now().year)

# --- Serve Uploaded File ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)