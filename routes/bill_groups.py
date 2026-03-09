"""
Bill Group routes for managing monthly bill groups
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.bill_group import BillGroup
from models.profile import Profile
from models.bill import Bill
from datetime import datetime

bill_groups_bp = Blueprint('bill_groups', __name__, url_prefix='/bill-groups')

@bill_groups_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new bill group"""
    try:
        name = request.form.get('name')
        profile_id = request.form.get('profile_id')
        
        if not name or not profile_id:
            flash('Name and profile are required', 'error')
            return redirect(url_for('dashboard.index'))
        
        # Verify the profile belongs to the user
        profile = Profile.query.filter_by(id=profile_id, user_id=current_user.id).first()
        if not profile:
            flash('Invalid profile', 'error')
            return redirect(url_for('dashboard.index'))
        
        # Create the bill group
        bill_group = BillGroup(
            name=name,
            profile_id=profile_id
        )
        
        db.session.add(bill_group)
        db.session.commit()
        
        flash(f'Bill group "{name}" created successfully!', 'success')
        return redirect(url_for('bill_groups.view', group_id=bill_group.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating bill group: {str(e)}', 'error')
        return redirect(url_for('dashboard.index'))

@bill_groups_bp.route('/<int:group_id>')
@login_required
def view(group_id):
    """View a bill group and its bills"""
    bill_group = BillGroup.query.get_or_404(group_id)
    
    # Verify the bill group's profile belongs to the user
    if bill_group.profile.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Get all bills in this group
    bills = Bill.query.filter_by(bill_group_id=group_id).order_by(Bill.from_date).all()
    
    # Get bill IDs that exist
    bill_ids = {bill.id for bill in bills}
    
    # Get adjustments for this bill group's bills
    from models.adjustment import Adjustment
    all_adjustments = Adjustment.query.filter_by(profile_id=bill_group.profile_id).all()
    adjustments = [adj for adj in all_adjustments if adj.bill_id is None or adj.bill_id in bill_ids]
    
    # Calculate summary
    from utils.calculations import calculate_summary
    roommate_names = [r.name for r in bill_group.profile.roommates]
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
    
    return render_template('bill_group.html', 
                         bill_group=bill_group, 
                         bills=bills,
                         adjustments=adjustments,
                         summary=summary,
                         bills_data=bills_data,
                         adjustments_data=adjustments_data)

@bill_groups_bp.route('/<int:group_id>/delete', methods=['POST'])
@login_required
def delete(group_id):
    """Delete a bill group and all its bills"""
    bill_group = BillGroup.query.get_or_404(group_id)
    
    # Verify the bill group's profile belongs to the user
    if bill_group.profile.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard.index'))
    
    try:
        group_name = bill_group.name
        db.session.delete(bill_group)
        db.session.commit()
        flash(f'Bill group "{group_name}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bill group: {str(e)}', 'error')
    
    return redirect(url_for('dashboard.index'))
