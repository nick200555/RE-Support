app_name = "re_support"
app_title = "RE Support System"
app_publisher = "Your Company Name"
app_description = "Real estate post-handover customer support application"
app_version = "1.0.0"
required_apps = ["frappe", "erpnext"]

# Exported as fixtures/roles.json
roles = [
    "Support Manager",
    "Support Agent",
    "Site Inspector",
    "Legal Team",
    "Possession Exec",
    "Finance Team",
    "Buyer",
]

doc_events = {
    "Support Ticket": {
        "before_insert": "re_support.utils.sla_engine.set_sla_due_dates",
        "on_update": [
            "re_support.utils.notifications.notify_buyer_status_change",
            "re_support.complaint_management.doctype.support_ticket.support_ticket.check_first_response"
        ],
        "on_submit": "re_support.complaint_management.doctype.support_ticket.support_ticket.create_defect_if_applicable",
    },
    "Defect Report": {
        "on_submit": "re_support.defect_snagging.doctype.defect_report.defect_report.assign_contractors_on_submit",
        "on_update": "re_support.defect_snagging.doctype.defect_report.defect_report.update_open_defect_count",
    },
    "Possession Request": {
        "on_update": "re_support.possession_management.doctype.possession_request.possession_request.notify_buyer_possession_update",
        "before_save": "re_support.possession_management.doctype.possession_request.possession_request.check_all_nocs_received",
    },
    "RERA Complaint": {
        "before_save": "re_support.rera_escalation.doctype.rera_complaint.rera_complaint.check_response_deadline",
        "on_submit": "re_support.rera_escalation.doctype.rera_complaint.rera_complaint.notify_legal_team",
    },
}

scheduler_events = {
    "cron": {
        "*/30 * * * *": [
            "re_support.utils.sla_engine.check_sla_breaches"
        ],
        "0 * * * *": [
            "re_support.rera_escalation.rera_alert.check_response_deadlines"
        ],
    },
    "daily": [
        "re_support.utils.notifications.send_daily_sla_summary_to_managers",
        "re_support.rera_escalation.rera_alert.send_hearing_reminders",
        "re_support.possession_management.tasks.update_possession_aging",
    ],
    "weekly": [
        "re_support.reports_analytics.tasks.generate_weekly_kpi_report",
    ],
}

website_route_rules = [
    {"from_route": "/support",               "to_route": "buyer_portal"},
    {"from_route": "/support/<ticket_no>",   "to_route": "ticket_detail"},
    {"from_route": "/possession/<unit_no>",  "to_route": "possession_status"},
]

fixtures = [
    "Custom Field",
    "Property Setter",
    "Role",
    "Workflow",
    "Workspace",
]
