import frappe
from frappe.utils import add_to_date, now_datetime

def set_sla_due_dates(doc, method=None):
    """Auto-set SLA response and resolution deadlines on ticket creation."""
    if not doc.sla_policy:
        cat = frappe.get_doc("Ticket Category", doc.category)
        doc.sla_policy = cat.default_sla
    if doc.sla_policy:
        sla = frappe.get_doc("SLA Policy", doc.sla_policy)
        now = now_datetime()
        doc.sla_response_due   = add_to_date(now, hours=sla.response_time_hrs)
        doc.sla_resolution_due = add_to_date(now, hours=sla.resolution_time_hrs)

def check_sla_breaches():
    """Scheduled job: flag breached tickets and escalate."""
    now = now_datetime()
    open_tickets = frappe.get_list("Support Ticket",
        filters={"status": ["in", ["Open","Assigned","In Progress"]]},
        fields=["name","sla_resolution_due","escalate_to"])
    for ticket in open_tickets:
        if ticket.sla_resolution_due and ticket.sla_resolution_due < now:
            frappe.db.set_value("Support Ticket", ticket.name,
                "resolution_breached", 1)
            if ticket.escalate_to:
                send_breach_alert(ticket.name, ticket.escalate_to)
    frappe.db.commit()

def send_breach_alert(ticket, user):
    pass
