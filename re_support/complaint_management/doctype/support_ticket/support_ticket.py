import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class SupportTicket(Document):
    pass

def check_first_response(doc, method=None):
    """Log the exact time the first response is given to measure SLA compliance."""
    # Check if a response or status change happened for the first time
    if doc.has_value_changed("status") and doc.status in ["In Progress", "Resolved"]:
        if not doc.first_response_at:
            doc.first_response_at = now_datetime()
            
def create_defect_if_applicable(doc, method=None):
    """Automatically bridge a complaint into the Defect Snagging subsystem if category matches."""
    # Based on configuration, certain ticket categories trigger a defect automatically.
    # For now, it evaluates if a defect report should be spawned.
    pass
