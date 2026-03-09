#!/usr/bin/env python3
"""
Roommate Bill Splitter - Multi-User Application
Main application entry point
"""

from flask import Flask
from flask_login import LoginManager
from models.database import init_db, db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profiles import profiles_bp
from routes.bills import bills_bp
from routes.bill_groups import bill_groups_bp
from routes.adjustments import adjustments_bp
from models.user import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bill_splitter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(bills_bp)
app.register_blueprint(bill_groups_bp)
app.register_blueprint(adjustments_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════╗
    ║  💰 Roommate Bill Splitter v3.0               ║
    ║  Multi-User with Database Support             ║
    ╚════════════════════════════════════════════════╝
    
    🚀 Server starting on http://localhost:5000
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
