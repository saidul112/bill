// Profile page specific JavaScript

function toggleRoommateInput() {
    const inputGroup = document.getElementById('roommateInputGroup');
    if (inputGroup.style.display === 'none') {
        inputGroup.style.display = 'block';
        document.getElementById('newRoommateName').focus();
    } else {
        inputGroup.style.display = 'none';
        document.getElementById('newRoommateName').value = '';
    }
}

function toggleSubType() {
    const billType = document.getElementById('billType').value;
    const subTypeGroup = document.getElementById('subTypeGroup');
    
    if (billType === 'Extras') {
        subTypeGroup.style.display = 'block';
    } else {
        subTypeGroup.style.display = 'none';
        document.getElementById('billSubType').value = '';
    }
}

function togglePaidBy() {
    const alreadyPaid = document.getElementById('billAlreadyPaid').checked;
    const paidByGroup = document.getElementById('paidByGroup');
    const paidBySelect = document.getElementById('billPaidBy');
    
    if (alreadyPaid) {
        paidByGroup.style.display = 'block';
        paidBySelect.required = true;
    } else {
        paidByGroup.style.display = 'none';
        paidBySelect.required = false;
        paidBySelect.value = '';
    }
}

function setCurrentMonthDates() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    
    const fromDate = `${year}-${month}-01`;
    const toDate = `${year}-${month}-30`;
    
    document.getElementById('billFromDate').value = fromDate;
    document.getElementById('billToDate').value = toDate;
}

function openNewBillModal() {
    // If on profile page
    if (typeof profileId !== 'undefined') {
        resetBillForm();
        setCurrentMonthDates();
        openModal('billModal');
    } else {
        // If on dashboard, redirect to first profile or show message
        alert('Please select a profile first');
    }
}

function resetBillForm() {
    document.getElementById('billForm').reset();
    document.getElementById('billId').value = '';
    document.getElementById('billModalTitle').textContent = 'Add New Bill';
    document.getElementById('billSubmitBtn').textContent = 'Add Bill';
    document.getElementById('paidByGroup').style.display = 'none';
    document.getElementById('billPaidBy').required = false;
    document.getElementById('subTypeGroup').style.display = 'none';
    document.getElementById('billSubType').value = '';
    document.getElementById('billType').value = '';
    document.getElementById('billAmount').value = '';
    document.getElementById('billDescription').value = '';
    
    // Clear excluded members checkboxes
    document.querySelectorAll('input[name="excludeMembers"]').forEach(checkbox => {
        checkbox.checked = false;
    });
}

function resetAdjustmentForm() {
    document.getElementById('adjustmentForm').reset();
    document.getElementById('adjId').value = '';
    document.getElementById('adjustmentModalTitle').textContent = 'Add Usage Adjustment';
    document.getElementById('adjSubmitBtn').textContent = 'Add Adjustment';
}

async function addRoommate() {
    const name = document.getElementById('newRoommateName').value.trim();
    if (!name) return;
    
    try {
        const response = await fetch(`/profiles/${profileId}/roommates/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to add roommate');
        }
    } catch (error) {
        alert('Error adding roommate');
    }
}

async function removeRoommate(roommateId) {
    if (!confirm('Remove this roommate?')) return;
    
    try {
        const response = await fetch(`/profiles/${profileId}/roommates/${roommateId}/delete`, {
            method: 'POST'
        });
        
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        alert('Error removing roommate');
    }
}

async function saveBill(event) {
    event.preventDefault();
    
    const billId = document.getElementById('billId').value;
    const isEdit = billId !== '';
    
    const alreadyPaid = document.getElementById('billAlreadyPaid').checked;
    const paidBy = alreadyPaid ? document.getElementById('billPaidBy').value : null;
    
    // Collect excluded members
    const excludedMembers = [];
    document.querySelectorAll('input[name="excludeMembers"]:checked').forEach(checkbox => {
        excludedMembers.push(checkbox.value);
    });
    
    const billData = {
        type: document.getElementById('billType').value,
        sub_type: document.getElementById('billSubType').value,
        amount: parseFloat(document.getElementById('billAmount').value),
        from_date: document.getElementById('billFromDate').value,
        to_date: document.getElementById('billToDate').value,
        paid_by: paidBy,
        already_paid: alreadyPaid,
        description: document.getElementById('billDescription').value,
        included_members: [],
        excluded_members: excludedMembers
    };
    
    // Add bill_group_id if it exists (for bill groups page)
    if (typeof billGroupId !== 'undefined') {
        billData.bill_group_id = billGroupId;
    }
    
    try {
        const url = isEdit 
            ? `/api/bills/${profileId}/${billId}`
            : `/api/bills/${profileId}`;
        const method = isEdit ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(billData)
        });
        
        if (response.ok) {
            if (!isEdit) {
                // Reset form after adding new bill
                resetBillForm();
                setCurrentMonthDates();
            }
            location.reload();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to save bill');
        }
    } catch (error) {
        alert('Error saving bill');
    }
}

function editBill(billId) {
    const bill = billsData.find(b => b.id === billId);
    if (!bill) return;
    
    document.getElementById('billId').value = bill.id;
    document.getElementById('billType').value = bill.bill_type;
    document.getElementById('billSubType').value = bill.sub_type || '';
    document.getElementById('billAmount').value = bill.amount;
    document.getElementById('billFromDate').value = bill.from_date;
    document.getElementById('billToDate').value = bill.to_date;
    document.getElementById('billAlreadyPaid').checked = bill.already_paid;
    document.getElementById('billPaidBy').value = bill.paid_by || '';
    document.getElementById('billDescription').value = bill.description || '';
    
    // Set excluded members checkboxes
    document.querySelectorAll('input[name="excludeMembers"]').forEach(checkbox => {
        checkbox.checked = bill.excluded_members && bill.excluded_members.includes(checkbox.value);
    });
    
    document.getElementById('billModalTitle').textContent = 'Edit Bill';
    document.getElementById('billSubmitBtn').textContent = 'Update Bill';
    
    toggleSubType();
    togglePaidBy();
    openModal('billModal');
}

async function deleteBill(billId) {
    if (!confirm('Delete this bill? This will also delete associated adjustments.')) return;
    
    try {
        const response = await fetch(`/api/bills/${profileId}/${billId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        alert('Error deleting bill');
    }
}

async function saveAdjustment(event) {
    event.preventDefault();
    
    const adjId = document.getElementById('adjId').value;
    const isEdit = adjId !== '';
    
    const adjData = {
        member: document.getElementById('adjMember').value,
        bill_type: document.getElementById('adjBillType').value,
        from_date: document.getElementById('adjFromDate').value,
        to_date: document.getElementById('adjToDate').value,
        reason: document.getElementById('adjReason').value
    };
    
    try {
        const url = isEdit 
            ? `/api/adjustments/${profileId}/${adjId}`
            : `/api/adjustments/${profileId}`;
        const method = isEdit ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(adjData)
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to save adjustment');
        }
    } catch (error) {
        alert('Error saving adjustment');
    }
}

function editAdjustment(adjId) {
    const adj = adjustmentsData.find(a => a.id === adjId);
    if (!adj) return;
    
    document.getElementById('adjId').value = adj.id;
    document.getElementById('adjMember').value = adj.member;
    document.getElementById('adjBillType').value = adj.bill_type;
    document.getElementById('adjFromDate').value = adj.from_date;
    document.getElementById('adjToDate').value = adj.to_date;
    document.getElementById('adjReason').value = adj.reason;
    
    document.getElementById('adjustmentModalTitle').textContent = 'Edit Adjustment';
    document.getElementById('adjSubmitBtn').textContent = 'Update Adjustment';
    
    openModal('adjustmentModal');
}

async function deleteAdjustment(adjId) {
    if (!confirm('Delete this adjustment?')) return;
    
    try {
        const response = await fetch(`/api/adjustments/${profileId}/${adjId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        alert('Error deleting adjustment');
    }
}

// Auto-populate dates when opening bill modal for new bill
document.addEventListener('DOMContentLoaded', function() {
    const roommateInput = document.getElementById('newRoommateName');
    if (roommateInput) {
        roommateInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addRoommate();
            }
        });
    }
    
    // Override the openModal function for billModal to set dates and reset form
    const originalOpenModal = window.openModal;
    window.openModal = function(modalId) {
        if (modalId === 'billModal') {
            const billId = document.getElementById('billId').value;
            if (!billId) {
                // Only reset and set dates if creating new bill (not editing)
                resetBillForm();
                setCurrentMonthDates();
            }
        }
        if (modalId === 'adjustmentModal') {
            const adjId = document.getElementById('adjId').value;
            if (!adjId) {
                resetAdjustmentForm();
            }
        }
        if (typeof originalOpenModal === 'function') {
            originalOpenModal(modalId);
        } else {
            document.getElementById(modalId).style.display = 'flex';
        }
    };
});
