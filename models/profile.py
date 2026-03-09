"""
Profile model for managing roommate groups
"""

from models.database import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    roommates = db.relationship('Roommate', backref='profile', lazy=True, cascade='all, delete-orphan')
    bills = db.relationship('Bill', backref='profile', lazy=True, cascade='all, delete-orphan')
    adjustments = db.relationship('Adjustment', backref='profile', lazy=True, cascade='all, delete-orphan')
    bill_groups = db.relationship('BillGroup', backref='profile', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profile {self.name}>'


class Roommate(db.Model):
    __tablename__ = 'roommates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Roommate {self.name}>'
