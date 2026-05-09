"""
Maryam Fatima Portfolio - Flask Backend
"""
import os
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__, 
            template_folder='templates',  # Explicitly set templates folder
            static_folder='static')       # Explicitly set static folder

# Ensure proper MIME types
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    """Serve the main portfolio page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files with correct MIME types"""
    return send_from_directory('static', filename)

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'Maryam Fatima Portfolio'})

# API endpoint for portfolio data
@app.route('/api/portfolio')
def get_portfolio():
    """Return portfolio data"""
    portfolio_data = {
        "name": "Maryam Fatima",
        "title": "Full Stack Developer",
        "email": "maryamfatima28022003@gmail.com",
        "phone": "+92 310 3024004",
        "location": "Hyderabad, Pakistan",
        "skills": ["React.js", "Python", "Flask", "Next.js", "TypeScript", "Tailwind CSS"],
        "stats": {
            "projects": "10+",
            "experience": "1+",
            "technologies": "8",
            "satisfaction": "99%"
        }
    }
    return jsonify(portfolio_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)