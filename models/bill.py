"""
Bill model for managing bills
"""

from models.database import db
from datetime import datetime
import json

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    bill_group_id = db.Column(db.Integer, db.ForeignKey('bill_groups.id'), nullable=True)
    bill_type = db.Column(db.String(50), nullable=False)  # Gas, Electricity, Water, Extras
    sub_type = db.Column(db.String(100))  # For extras: tissue, cleaning, etc.
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    paid_by = db.Column(db.String(100), nullable=True)
    already_paid = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    included_members = db.Column(db.Text)  # JSON array
    excluded_members = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with cascade delete
    adjustments = db.relationship('Adjustment', backref='parent_bill', cascade='all, delete-orphan')
    
    def get_included_members(self):
        if self.included_members:
            return json.loads(self.included_members)
        return []
    
    def set_included_members(self, members):
        self.included_members = json.dumps(members)
    
    def get_excluded_members(self):
        if self.excluded_members:
            return json.loads(self.excluded_members)
        return []
    
    def set_excluded_members(self, members):
        self.excluded_members = json.dumps(members)
    
    def get_total_days(self):
        return (self.to_date - self.from_date).days + 1
    
    def __repr__(self):
        return f'<Bill {self.bill_type} - {self.amount}>'
