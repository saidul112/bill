"""
Adjustment model for managing usage adjustments
"""

from models.database import db
from datetime import datetime

class Adjustment(db.Model):
    __tablename__ = 'adjustments'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id', ondelete='CASCADE'), nullable=True)
    member = db.Column(db.String(100), nullable=False)
    bill_type = db.Column(db.String(50), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_total_days(self):
        return (self.to_date - self.from_date).days + 1
    
    def __repr__(self):
        return f'<Adjustment {self.member} - {self.bill_type}>'
