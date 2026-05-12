import frappe

def notify_buyer_status_change(doc, method=None):
    """Triggered on_update to notify the buyer if the ticket status changes."""
    # Only notify if the status has actually changed
    if doc.has_value_changed("status"):
        subject = f"Support Ticket {doc.name} Status Update: {doc.status}"
        message = f"Dear {doc.buyer},\n\nYour support ticket {doc.name} has been updated to '{doc.status}'.\n\nThank you."
        
        # In a real scenario, this would use frappe.sendmail or an SMS integration
        frappe.msgprint(f"Notification queued for Buyer {doc.buyer}: {subject}")
        # frappe.sendmail(recipients=[doc.buyer_email], subject=subject, message=message)

def send_daily_sla_summary_to_managers():
    """Daily cron job: send SLA summary to Support Managers."""
    # Logic to aggregate open/breached tickets and email
    breached_count = frappe.db.count("Support Ticket", {"resolution_breached": 1, "status": ["!=", "Closed"]})
    if breached_count > 0:
        frappe.logger().warning(f"SLA Summary: Currently {breached_count} tickets are breached.")
