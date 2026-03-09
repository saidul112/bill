"""
Bill management routes
"""

from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db
from models.profile import Profile
from models.bill import Bill
from models.adjustment import Adjustment
from datetime import datetime

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('/api/bills/<int:profile_id>', methods=['POST'])
@login_required
def create_json(profile_id):
    """Create bill via JSON API"""
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    data = request.json
    
    bill = Bill(
        profile_id=profile_id,
        bill_group_id=data.get('bill_group_id'),
        bill_type=data.get('type'),
        sub_type=data.get('sub_type'),
        amount=float(data.get('amount', 0)),
        from_date=datetime.strptime(data.get('from_date'), '%Y-%m-%d').date(),
        to_date=datetime.strptime(data.get('to_date'), '%Y-%m-%d').date(),
        paid_by=data.get('paid_by'),
        already_paid=data.get('already_paid', False),
        description=data.get('description', '')
    )
    
    bill.set_included_members(data.get('included_members', []))
    bill.set_excluded_members(data.get('excluded_members', []))
    
    db.session.add(bill)
    db.session.commit()
    
    return jsonify({'success': True, 'bill_id': bill.id})

@bills_bp.route('/bills/<int:profile_id>/create', methods=['POST'])
@login_required
def create(profile_id):
    """Create bill via form submission"""
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.index'))
    
    try:
        bill = Bill(
            profile_id=profile_id,
            bill_group_id=request.form.get('bill_group_id'),
            bill_type=request.form.get('type'),
            sub_type=request.form.get('sub_type'),
            amount=float(request.form.get('amount', 0)),
            from_date=datetime.strptime(request.form.get('from_date'), '%Y-%m-%d').date(),
            to_date=datetime.strptime(request.form.get('to_date'), '%Y-%m-%d').date(),
            paid_by=request.form.get('paid_by') if request.form.get('already_paid') else None,
            already_paid=bool(request.form.get('already_paid')),
            description=request.form.get('description', '')
        )
        
        db.session.add(bill)
        db.session.commit()
        
        flash('Bill added successfully!', 'success')
        
        # Redirect to specified location or back to profile
        redirect_to = request.form.get('redirect_to')
        if redirect_to:
            return redirect(redirect_to)
        return redirect(url_for('profiles.view', profile_id=profile_id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding bill: {str(e)}', 'error')
        return redirect(url_for('profiles.view', profile_id=profile_id))

@bills_bp.route('/api/bills/<int:profile_id>/<int:bill_id>', methods=['PUT'])
@login_required
def update(profile_id, bill_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    bill = Bill.query.get_or_404(bill_id)
    
    if bill.profile_id != profile_id:
        return jsonify({'success': False, 'error': 'Invalid bill'}), 400
    
    data = request.json
    
    bill.bill_type = data.get('type', bill.bill_type)
    bill.sub_type = data.get('sub_type', bill.sub_type)
    bill.amount = float(data.get('amount', bill.amount))
    bill.from_date = datetime.strptime(data.get('from_date'), '%Y-%m-%d').date() if data.get('from_date') else bill.from_date
    bill.to_date = datetime.strptime(data.get('to_date'), '%Y-%m-%d').date() if data.get('to_date') else bill.to_date
    bill.paid_by = data.get('paid_by', bill.paid_by)
    bill.already_paid = data.get('already_paid', bill.already_paid)
    bill.description = data.get('description', bill.description)
    
    if 'included_members' in data:
        bill.set_included_members(data.get('included_members', []))
    if 'excluded_members' in data:
        bill.set_excluded_members(data.get('excluded_members', []))
    
    db.session.commit()
    
    return jsonify({'success': True})

@bills_bp.route('/bills/<int:bill_id>/delete', methods=['POST'])
@login_required
def delete(bill_id):
    """Delete bill via form submission"""
    bill = Bill.query.get_or_404(bill_id)
    
    # Verify access through profile
    if bill.profile.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.index'))
    
    try:
        # Manually delete associated adjustments as fallback
        Adjustment.query.filter_by(bill_id=bill_id).delete()
        
        # Delete the bill
        db.session.delete(bill)
        db.session.commit()
        
        flash('Bill deleted successfully', 'success')
        
        # Redirect to specified location or back to dashboard
        redirect_to = request.form.get('redirect_to')
        if redirect_to:
            return redirect(redirect_to)
        return redirect(url_for('dashboard.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bill: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@bills_bp.route('/api/bills/<int:profile_id>/<int:bill_id>', methods=['DELETE'])
@login_required
def delete_json(profile_id, bill_id):
    """Delete bill via JSON API"""
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    bill = Bill.query.get_or_404(bill_id)
    
    if bill.profile_id != profile_id:
        return jsonify({'success': False, 'error': 'Invalid bill'}), 400
    
    # Manually delete associated adjustments as fallback
    Adjustment.query.filter_by(bill_id=bill_id).delete()
    
    # Delete the bill
    db.session.delete(bill)
    db.session.commit()
    
    return jsonify({'success': True})

@bills_bp.route('/api/bills/<int:profile_id>/types', methods=['GET'])
@login_required
def get_bill_types(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    bills = Bill.query.filter_by(profile_id=profile_id).all()
    
    # Get unique bill types and sub-types
    bill_types = {}
    for bill in bills:
        if bill.bill_type not in bill_types:
            bill_types[bill.bill_type] = set()
        if bill.sub_type:
            bill_types[bill.bill_type].add(bill.sub_type)
    
    # Convert sets to lists for JSON serialization
    result = {k: list(v) for k, v in bill_types.items()}
    
    return jsonify({'success': True, 'bill_types': result})
