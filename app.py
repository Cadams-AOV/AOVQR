import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import qrcode

app = Flask(__name__)
app.secret_key = 'some-secret-key'  # <-- Replace with a real secret in production

DB_NAME = 'certificates.db'
QR_FOLDER = 'static/images/qrcodes'

#######################
#  QR Code Generation #
#######################
def generate_qr_code(license_serial):
    """
    Generates a personalized QR code linking to the verification page
    on your Render deployment.
    """
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)

    qr_data = f"https://aovqr.onrender.com/verify/{license_serial}"
    qr = qrcode.make(qr_data)

    qr_path = os.path.join(QR_FOLDER, f"{license_serial}.png")
    qr.save(qr_path)
    
    return qr_path

###################
#    HOME ROUTE    #
###################
@app.route('/')
def index():
    """
    Simple home route to confirm the app is live.
    """
    return "AOVQR is live! Visit /admin-login to manage licenses."

###################
#  ADMIN LOGIN    #
###################
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login route with hard-coded credentials.
    For production, store credentials securely or use a database.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hard-coded credentials (replace for production)
        if username == 'CadamsII' and password == 'A7d5A0m3$!':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('admin_login.html')

###################
#  ADMIN PANEL    #
###################
@app.route('/admin-panel')
def admin_panel():
    """
    Protected admin panel route.
    Only accessible if 'admin' in session.
    """
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

###################
#     LOGOUT      #
###################
@app.route('/logout')
def logout():
    """
    Logout the admin user by clearing the session.
    """
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

############################
#  LICENSE REGISTRATION    #
############################
@app.route('/register-license', methods=['POST'])
def register_license():
    """
    Handle license registration from the admin panel.
    Expects form data with license details.
    """
    if 'admin' not in session:
        return "Unauthorized", 403

    data = request.form
    license_serial = data.get('license_serial')
    licensee = data.get('licensee')
    license_type = data.get('license_type')
    license_status = data.get('license_status')
    license_exclusivity = data.get('license_exclusivity')
    issue_date = data.get('issue_date')
    expiration_date = data.get('expiration_date')
    company_name = data.get('company_name')
    company_address = data.get('company_address')
    phone_number = data.get('phone_number')
    card_type = data.get('card_type')
    card_last4 = data.get('card_last4')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            license_serial TEXT PRIMARY KEY,
            licensee TEXT,
            license_type TEXT,
            license_status TEXT,
            license_exclusivity TEXT,
            issue_date TEXT,
            expiration_date TEXT,
            company_name TEXT,
            company_address TEXT,
            phone_number TEXT,
            card_type TEXT,
            card_last4 TEXT
        )
    ''')

    # Insert or replace the license data
    cursor.execute('''
        INSERT OR REPLACE INTO licenses
        (license_serial, licensee, license_type, license_status, license_exclusivity,
         issue_date, expiration_date, company_name, company_address, phone_number,
         card_type, card_last4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        license_serial, licensee, license_type, license_status, license_exclusivity,
        issue_date, expiration_date, company_name, company_address, phone_number,
        card_type, card_last4
    ))

    conn.commit()
    conn.close()

    # Generate a QR code for the newly registered license
    generate_qr_code(license_serial)

    return f"License {license_serial} registered successfully!"

##########################
#  LICENSE VERIFICATION  #
##########################
@app.route('/verify/<license_serial>')
def verify_license(license_serial):
    """
    Retrieves license data from the database and renders a detailed verification page.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM licenses WHERE license_serial=?", (license_serial,))
    license_data = cursor.fetchone()
    conn.close()

    if not license_data:
        return "License not found", 404

    # Map the fetched data to the field names
    field_names = [
        'license_serial', 'licensee', 'license_type', 'license_status',
        'license_exclusivity', 'issue_date', 'expiration_date', 'company_name',
        'company_address', 'phone_number', 'card_type', 'card_last4'
    ]
    license_dict = dict(zip(field_names, license_data))

    return render_template('verify_detailed.html', **license_dict)

###################
#  RUN THE APP    #
###################
if __name__ == '__main__':
    app.run(debug=True)
