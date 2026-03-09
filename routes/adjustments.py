"""
Adjustment management routes
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.profile import Profile
from models.bill import Bill
from models.adjustment import Adjustment
from datetime import datetime

adjustments_bp = Blueprint('adjustments', __name__, url_prefix='/api/adjustments')

@adjustments_bp.route('/<int:profile_id>', methods=['POST'])
@login_required
def create(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    data = request.json
    
    adjustment = Adjustment(
        profile_id=profile_id,
        bill_id=data.get('bill_id'),
        member=data.get('member'),
        bill_type=data.get('bill_type'),
        from_date=datetime.strptime(data.get('from_date'), '%Y-%m-%d').date(),
        to_date=datetime.strptime(data.get('to_date'), '%Y-%m-%d').date(),
        reason=data.get('reason', '')
    )
    
    db.session.add(adjustment)
    db.session.commit()
    
    return jsonify({'success': True, 'adjustment_id': adjustment.id})

@adjustments_bp.route('/<int:profile_id>/<int:adjustment_id>', methods=['PUT'])
@login_required
def update(profile_id, adjustment_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    adjustment = Adjustment.query.get_or_404(adjustment_id)
    
    if adjustment.profile_id != profile_id:
        return jsonify({'success': False, 'error': 'Invalid adjustment'}), 400
    
    data = request.json
    
    adjustment.bill_id = data.get('bill_id', adjustment.bill_id)
    adjustment.member = data.get('member', adjustment.member)
    adjustment.bill_type = data.get('bill_type', adjustment.bill_type)
    adjustment.from_date = datetime.strptime(data.get('from_date'), '%Y-%m-%d').date() if data.get('from_date') else adjustment.from_date
    adjustment.to_date = datetime.strptime(data.get('to_date'), '%Y-%m-%d').date() if data.get('to_date') else adjustment.to_date
    adjustment.reason = data.get('reason', adjustment.reason)
    
    db.session.commit()
    
    return jsonify({'success': True})

@adjustments_bp.route('/<int:profile_id>/<int:adjustment_id>', methods=['DELETE'])
@login_required
def delete(profile_id, adjustment_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    adjustment = Adjustment.query.get_or_404(adjustment_id)
    
    if adjustment.profile_id != profile_id:
        return jsonify({'success': False, 'error': 'Invalid adjustment'}), 400
    
    db.session.delete(adjustment)
    db.session.commit()
    
    return jsonify({'success': True})
