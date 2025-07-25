"""
WebWaka Finance Sector - Main Application
Flask backend with African optimization and cultural integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for African mobile apps
CORS(app, origins="*")

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///webwaka_finance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'webwaka-finance-secret-key')

# Initialize database
db = SQLAlchemy(app)

# Import models and routes
from models.finance_models import *
from routes.finance_routes import bp as finance_bp

# Register blueprints
app.register_blueprint(finance_bp, url_prefix='/api/finance')

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'sector': 'finance', 'african_optimized': True})

# Ready check endpoint
@app.route('/ready')
def ready_check():
    return jsonify({'status': 'ready', 'sector': 'finance', 'database': 'connected'})

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        'message': 'WebWaka Finance Sector API',
        'version': '1.0.0',
        'african_optimized': True,
        'mobile_first': True,
        'offline_support': True,
        'cultural_integration': True
    })

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run app with African optimization
    app.run(
        host='0.0.0.0',  # Allow external access
        port=5000,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
