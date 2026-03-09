"""
Profile management routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.profile import Profile, Roommate
from models.bill import Bill
from models.adjustment import Adjustment
from utils.calculations import calculate_summary

profiles_bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@profiles_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Profile name is required', 'danger')
            return redirect(url_for('profiles.create'))
        
        profile = Profile(name=name, user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        
        flash('Profile created! Now create your first monthly period.', 'success')
        # Redirect to create first monthly period for this profile
        return redirect(url_for('profiles.create_first_month', profile_id=profile.id))
    
    return render_template('create_profile.html')

@profiles_bp.route('/<int:profile_id>/create-first-month', methods=['GET'])
@login_required
def create_first_month(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.index'))
    
    return render_template('create_first_month.html', profile=profile)

@profiles_bp.route('/<int:profile_id>')
@login_required
def view(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.index'))
    
    roommates = Roommate.query.filter_by(profile_id=profile_id).all()
    bills = Bill.query.filter_by(profile_id=profile_id).order_by(Bill.created_at.desc()).all()
    
    # Get bill IDs that exist
    bill_ids = {bill.id for bill in bills}
    
    # Filter adjustments to only show those with existing parent bills or no parent bill
    all_adjustments = Adjustment.query.filter_by(profile_id=profile_id).order_by(Adjustment.created_at.desc()).all()
    adjustments = [adj for adj in all_adjustments if adj.bill_id is None or adj.bill_id in bill_ids]
    
    # Calculate summary
    roommate_names = [r.name for r in roommates]
    summary = calculate_summary(roommate_names, bills, adjustments)
    
    # Convert bills to dictionaries for JSON serialization
    bills_data = []
    for bill in bills:
        bills_data.append({
            'id': bill.id,
            'bill_type': bill.bill_type,
            'sub_type': bill.sub_type,
            'amount': float(bill.amount),
            'from_date': bill.from_date.strftime('%Y-%m-%d'),
            'to_date': bill.to_date.strftime('%Y-%m-%d'),
            'paid_by': bill.paid_by,
            'already_paid': bill.already_paid,
            'description': bill.description,
            'included_members': bill.get_included_members(),
            'excluded_members': bill.get_excluded_members()
        })
    
    # Convert adjustments to dictionaries
    adjustments_data = []
    for adj in adjustments:
        adjustments_data.append({
            'id': adj.id,
            'member': adj.member,
            'bill_type': adj.bill_type,
            'from_date': adj.from_date.strftime('%Y-%m-%d'),
            'to_date': adj.to_date.strftime('%Y-%m-%d'),
            'reason': adj.reason
        })
    
    return render_template('profile.html', 
                         profile=profile, 
                         roommates=roommates, 
                         bills=bills,
                         adjustments=adjustments,
                         summary=summary,
                         bills_data=bills_data,
                         adjustments_data=adjustments_data)

@profiles_bp.route('/<int:profile_id>/delete', methods=['POST'])
@login_required
def delete(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard.index'))
    
    db.session.delete(profile)
    db.session.commit()
    
    flash('Profile deleted successfully', 'success')
    return redirect(url_for('dashboard.index'))

@profiles_bp.route('/<int:profile_id>/roommates/add', methods=['POST'])
@login_required
def add_roommate(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({'success': False, 'error': 'Name is required'}), 400
    
    # Check if roommate already exists
    existing = Roommate.query.filter_by(profile_id=profile_id, name=name).first()
    if existing:
        return jsonify({'success': False, 'error': 'Roommate already exists'}), 400
    
    roommate = Roommate(name=name, profile_id=profile_id)
    db.session.add(roommate)
    db.session.commit()
    
    return jsonify({'success': True, 'roommate': {'id': roommate.id, 'name': roommate.name}})

@profiles_bp.route('/<int:profile_id>/roommates/<int:roommate_id>/delete', methods=['POST'])
@login_required
def delete_roommate(profile_id, roommate_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    roommate = Roommate.query.get_or_404(roommate_id)
    
    if roommate.profile_id != profile_id:
        return jsonify({'success': False, 'error': 'Invalid roommate'}), 400
    
    db.session.delete(roommate)
    db.session.commit()
    
    return jsonify({'success': True})

@profiles_bp.route('/api/<int:profile_id>/roommates', methods=['GET'])
@login_required
def get_roommates_api(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    roommates = Roommate.query.filter_by(profile_id=profile_id).all()
    roommates_list = [{'id': r.id, 'name': r.name} for r in roommates]
    
    return jsonify({'success': True, 'roommates': roommates_list})
