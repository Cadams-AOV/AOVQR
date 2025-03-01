from flask import Flask, request, jsonify
import qrcode
import os
import hashlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificates.db'  # Change to MySQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.String(100), unique=True, nullable=False)
    qr_code_path = db.Column(db.String(200), unique=True, nullable=False)

def generate_qr_code(certificate_id):
    """Generate a QR code with an encrypted verification URL."""
    verification_url = f"https://onyxvisions.net/verify-license?certificate_id={certificate_id}"
    qr = qrcode.make(verification_url)
    qr_code_folder = "static/qrcodes"
    os.makedirs(qr_code_folder, exist_ok=True)  # Ensure folder exists
    qr_code_path = os.path.join(qr_code_folder, f"{certificate_id}.png")
    qr.save(qr_code_path)
    return qr_code_path

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    """Generate a certificate with a QR code."""
    data = request.json
    certificate_id = hashlib.sha256(data['name'].encode()).hexdigest()[:10]  # Unique ID based on name
    
    if Certificate.query.filter_by(certificate_id=certificate_id).first():
        return jsonify({"error": "Certificate already exists."}), 400
    
    qr_code_path = generate_qr_code(certificate_id)
    new_certificate = Certificate(certificate_id=certificate_id, qr_code_path=qr_code_path)
    db.session.add(new_certificate)
    db.session.commit()
    
    return jsonify({"certificate_id": certificate_id, "qr_code_url": qr_code_path})

@app.route('/verify/<certificate_id>', methods=['GET'])
def verify_certificate(certificate_id):
    """Verify if a certificate is valid."""
    certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
    if certificate:
        return jsonify({"status": "Valid", "certificate_id": certificate_id})
    else:
        return jsonify({"status": "Invalid"}), 404

@app.route('/api/verify/<certificate_id>', methods=['GET'])
def api_verify_certificate(certificate_id):
    """API Endpoint to verify certificate validity"""
    certificate = Certificate.query.filter_by(certificate_id=certificate_id).first()
    
    if certificate:
        return jsonify({"status": "Valid", "certificate_id": certificate_id})
    else:
        return jsonify({"status": "Invalid"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)