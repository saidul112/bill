"""
Dashboard routes
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.profile import Profile
from models.bill_group import BillGroup
from models.bill import Bill
from collections import defaultdict
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    profiles = Profile.query.filter_by(user_id=current_user.id).all()
    
    # Organize bill groups by profile
    profile_bill_groups = defaultdict(list)
    
    for profile in profiles:
        groups = BillGroup.query.filter_by(profile_id=profile.id).order_by(BillGroup.created_at.desc()).all()
        for group in groups:
            # Count bills in each group
            bill_count = Bill.query.filter_by(bill_group_id=group.id).count()
            profile_bill_groups[profile.id].append({
                'group': group,
                'profile': profile,
                'bill_count': bill_count
            })
    
    # Create JSON-serializable version for JavaScript
    profiles_json = [{'id': p.id, 'name': p.name} for p in profiles]
    
    return render_template('dashboard.html', 
                         profiles=profiles,
                         profiles_json=profiles_json,
                         profile_bill_groups=dict(profile_bill_groups))
