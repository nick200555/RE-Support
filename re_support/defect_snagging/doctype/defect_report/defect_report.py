import frappe
from frappe.model.document import Document

class DefectReport(Document):
    pass

def assign_contractors_on_submit(doc, method=None):
    """Automatically funnel assignments to selected contractors when approved."""
    pass

def update_open_defect_count(doc, method=None):
    """Update statistics over the total active defect items locally linked."""
    pass
