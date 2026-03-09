"""
Bill calculation utilities
"""

from decimal import Decimal, getcontext
from datetime import datetime

# Set decimal precision
getcontext().prec = 10

def calculate_summary(roommate_names, bills, adjustments):
    """
    Calculate bill summaries using daily rate for fair splitting with PRECISE decimal math.
    
    EXAMPLE: 円25 bill for 30 days among 5 people
    - Daily rate: 円25 ÷ 30 = 円0.833333... per day (using Decimal for precision)
    - Normal: Each pays 円5.000
    - If one person absent 15 days (present 15 days):
      * Absent person's share: (円0.833333... × 15) ÷ 5 = 円2.500
      * Remaining: 円25.000 - 円2.500 = 円22.500
      * Each of 4 present: 円22.500 ÷ 4 = 円5.625
      * Verification: 円2.500 + (4 × 円5.625) = 円25.000 ✓
    
    This ensures:
    1. Absent person pays only for days present
    2. Remaining people split the rest fairly
    3. Total always equals bill amount
    4. NO ROUNDING ERRORS - every cent is accounted for
    """
    # Initialize summary with Decimal for precision
    summary = {member: {
        'total': Decimal('0'), 
        'paid': Decimal('0'), 
        'balance': Decimal('0'), 
        'bills_breakdown': {}
    } for member in roommate_names}
    
    for bill in bills:
        # Determine who should pay for this bill
        included = bill.get_included_members()
        excluded = bill.get_excluded_members()
        
        if included:
            applicable_members = [m for m in included if m in roommate_names]
        else:
            applicable_members = [m for m in roommate_names if m not in excluded]
        
        if not applicable_members:
            continue
        
        # Calculate bill period
        bill_start = bill.from_date
        bill_end = bill.to_date
        total_bill_days = (bill_end - bill_start).days + 1
        
        # Convert to Decimal for precise calculation
        bill_amount = Decimal(str(bill.amount))
        total_days_decimal = Decimal(str(total_bill_days))
        
        # Calculate daily rate with high precision
        daily_rate = bill_amount / total_days_decimal
        
        # Track days present for each member (start with full period)
        member_days_present = {member: total_bill_days for member in applicable_members}
        
        # Apply adjustments (absence periods)
        for adj in adjustments:
            if adj.member in applicable_members and adj.bill_type == bill.bill_type:
                # Calculate overlap between bill period and absent period
                absent_start = adj.from_date
                absent_end = adj.to_date
                
                # Find the overlap
                overlap_start = max(bill_start, absent_start)
                overlap_end = min(bill_end, absent_end)
                
                # If there's an overlap, subtract absent days
                if overlap_start <= overlap_end:
                    absent_days = (overlap_end - overlap_start).days + 1
                    member_days_present[adj.member] = max(0, member_days_present[adj.member] - absent_days)
        
        # Count total people and who was fully present
        total_people = Decimal(str(len(applicable_members)))
        fully_present_members = [m for m, days in member_days_present.items() if days == total_bill_days]
        partially_present_members = [m for m, days in member_days_present.items() if days < total_bill_days and days > 0]
        
        # Calculate shares with Decimal precision
        total_allocated = Decimal('0')
        
        # First, calculate share for partially present members
        for member in partially_present_members:
            days_present = Decimal(str(member_days_present[member]))
            # Their share is: (daily_rate × days_present) ÷ total_people
            share = (daily_rate * days_present) / total_people
            summary[member]['total'] += share
            total_allocated += share
            
            # Track bills breakdown
            bill_type = bill.bill_type
            if bill.sub_type:
                bill_type = f"{bill.bill_type} - {bill.sub_type}"
            
            if bill_type not in summary[member]['bills_breakdown']:
                summary[member]['bills_breakdown'][bill_type] = Decimal('0')
            summary[member]['bills_breakdown'][bill_type] += share
        
        # Remaining amount to split among fully present members
        remaining_amount = bill_amount - total_allocated
        
        # Split remaining among fully present members
        if fully_present_members:
            num_fully_present = Decimal(str(len(fully_present_members)))
            share_per_person = remaining_amount / num_fully_present
            for member in fully_present_members:
                summary[member]['total'] += share_per_person
                
                # Track bills breakdown
                bill_type = bill.bill_type
                if bill.sub_type:
                    bill_type = f"{bill.bill_type} - {bill.sub_type}"
                
                if bill_type not in summary[member]['bills_breakdown']:
                    summary[member]['bills_breakdown'][bill_type] = Decimal('0')
                summary[member]['bills_breakdown'][bill_type] += share_per_person
        
        # Track who paid
        paid_by = bill.paid_by
        if paid_by in summary and bill.already_paid:
            summary[paid_by]['paid'] += bill_amount
    
    # Calculate final balances and convert to float for JSON serialization
    for member in summary:
        summary[member]['balance'] = summary[member]['total'] - summary[member]['paid']
        
        # Convert Decimal to float for display (keeping full precision)
        summary[member]['total'] = float(summary[member]['total'])
        summary[member]['paid'] = float(summary[member]['paid'])
        summary[member]['balance'] = float(summary[member]['balance'])
        
        # Convert bills_breakdown to float
        for bill_type in summary[member]['bills_breakdown']:
            summary[member]['bills_breakdown'][bill_type] = float(summary[member]['bills_breakdown'][bill_type])
    
    return summary
