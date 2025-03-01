from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to SQLite
def get_db_connection():
    conn = sqlite3.connect('certificates.db')
    conn.row_factory = sqlite3.Row  # Allows dictionary-like access to rows
    return conn

# ✅ Route: Test database connection
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple test query
        conn.close()
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ✅ Route: Verify a certificate
@app.route('/verify/<cert_code>')
def verify_certificate(cert_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query for the certificate
    cursor.execute("SELECT * FROM certificates WHERE cert_code = ?", (cert_code,))
    certificate = cursor.fetchone()
    conn.close()

    if certificate:
        return jsonify({
            "status": "valid",
            "message": "Certificate is valid!",
            "name": certificate["name"],
            "issued_date": certificate["issued_date"]
        })
    else:
        return jsonify({
            "status": "invalid",
            "message": "Certificate not found."
        })

# ✅ Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
