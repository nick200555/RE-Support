import frappe

@frappe.whitelist(allow_guest=False)
def get_buyer_tickets(buyer_mobile):
    """Return all tickets for the authenticated buyer."""
    return frappe.get_list('Support Ticket',
        filters={'buyer_mobile': buyer_mobile},
        fields=['ticket_no','category','status','sla_resolution_due','priority'],
        order_by='creation desc')

@frappe.whitelist(allow_guest=False)
def create_ticket(project, unit_no, category, description, attachments=None):
    """Create a new support ticket from the buyer portal."""
    doc = frappe.new_doc('Support Ticket')
    doc.buyer = frappe.session.user
    doc.project = project
    doc.unit_no = unit_no
    doc.category = category
    doc.description = description
    doc.insert(ignore_permissions=True)
    return doc.name

@frappe.whitelist(allow_guest=False)
def get_possession_status(unit_no, project):
    """Return possession request status for buyer's unit."""
    return frappe.db.get_value('Possession Request',
        {'unit_no': unit_no, 'project': project},
        ['possession_no','status','scheduled_date','key_handover_date'],
        as_dict=True)
