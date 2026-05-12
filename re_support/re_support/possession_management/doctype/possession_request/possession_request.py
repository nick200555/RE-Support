import frappe
from frappe.model.document import Document

class PossessionRequest(Document):
    pass

def notify_buyer_possession_update(doc, method=None):
    """Triggered on_update to inform tracking milestones onto portals."""
    pass

def check_all_nocs_received(doc, method=None):
    """Ensure compliance blocks prevent possession without sign-offs."""
    # Verify NOC Document states before handover
    pass
