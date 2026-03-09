"""
BillGroup model for organizing bills by custom month/period names
"""

from models.database import db
from datetime import datetime

class BillGroup(db.Model):
    __tablename__ = 'bill_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "January 2026", "Mid-Dec to Mid-Jan"
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    bills = db.relationship('Bill', backref='bill_group', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BillGroup {self.name}>'
