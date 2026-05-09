import os
import pyodbc
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ============================================
# YOUR AZURE SQL DATABASE CONNECTION
# ============================================
SERVER = 'pitp.database.windows.net'
DATABASE = 'mydatabase'
USERNAME = 'pitp'
PASSWORD = 'mar123@890//'  # Your password

# Connection string
connection_string = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = pyodbc.connect(connection_string)
        print("✅ Database connected successfully")
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def init_db():
    """Create tables if they don't exist"""
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot initialize database - connection failed")
        return
    
    cursor = conn.cursor()
    
    # Create contact messages table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='contact_messages' AND xtype='U')
        CREATE TABLE contact_messages (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            email NVARCHAR(100) NOT NULL,
            subject NVARCHAR(200),
            message NVARCHAR(MAX) NOT NULL,
            created_at DATETIME DEFAULT GETDATE()
        )
    """)
    
    # Create newsletter subscribers table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='newsletter_subscribers' AND xtype='U')
        CREATE TABLE newsletter_subscribers (
            id INT IDENTITY(1,1) PRIMARY KEY,
            email NVARCHAR(100) NOT NULL UNIQUE,
            interest NVARCHAR(50),
            subscribed_at DATETIME DEFAULT GETDATE()
        )
    """)
    
    # Create feedback table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='feedbacks' AND xtype='U')
        CREATE TABLE feedbacks (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100),
            rating INT,
            message NVARCHAR(MAX) NOT NULL,
            created_at DATETIME DEFAULT GETDATE()
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database tables created successfully")

@app.route('/')
def index():
    return render_template('index.html')

# API: Save contact message
@app.route('/api/contact', methods=['POST'])
def save_contact():
    try:
        data = request.get_json()
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        """, (data['name'], data['email'], data.get('subject', ''), data['message']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Message saved to database!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API: Save newsletter subscriber
@app.route('/api/newsletter', methods=['POST'])
def save_newsletter():
    try:
        data = request.get_json()
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO newsletter_subscribers (email, interest)
            VALUES (?, ?)
        """, (data['email'], data.get('interest', 'all')))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Subscribed successfully!'}), 200
    except Exception as e:
        if 'UNIQUE' in str(e):
            return jsonify({'success': False, 'error': 'Email already subscribed!'}), 400
        return jsonify({'success': False, 'error': str(e)}), 500

# API: Save feedback
@app.route('/api/feedback', methods=['POST'])
def save_feedback():
    try:
        data = request.get_json()
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedbacks (name, rating, message)
            VALUES (?, ?, ?)
        """, (data.get('name', 'Anonymous'), data.get('rating', 5), data['message']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Feedback saved!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API: Get all feedbacks
@app.route('/api/feedback/list', methods=['GET'])
def get_feedbacks():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify([]), 200
        
        cursor = conn.cursor()
        cursor.execute("SELECT name, rating, message, created_at FROM feedbacks ORDER BY created_at DESC")
        
        rows = cursor.fetchall()
        feedbacks = []
        for row in rows:
            feedbacks.append({
                'name': row[0],
                'rating': row[1],
                'message': row[2],
                'created_at': row[3].isoformat() if row[3] else None
            })
        
        conn.close()
        return jsonify(feedbacks), 200
    except Exception as e:
        return jsonify([]), 200

# API: Get all contact messages (admin)
@app.route('/api/admin/messages', methods=['GET'])
def get_messages():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify([]), 200
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, subject, message, created_at FROM contact_messages ORDER BY created_at DESC")
        
        rows = cursor.fetchall()
        messages = []
        for row in rows:
            messages.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'subject': row[3],
                'message': row[4],
                'created_at': row[5].isoformat() if row[5] else None
            })
        
        conn.close()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify([]), 200

# Health check endpoint
@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
