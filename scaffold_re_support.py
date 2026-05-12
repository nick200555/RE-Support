import os
import json

app_dir = r"C:\Seria Internship\RE_Support\re_support"

def make_dirs(path):
    os.makedirs(os.path.join(app_dir, path), exist_ok=True)

def write_file(path, content):
    full_path = os.path.join(app_dir, path)
    make_dirs(os.path.dirname(path))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# --- 1. Base Files ---
write_file("requirements.txt", "")
write_file("setup.py", """
from setuptools import setup, find_packages
with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\\n")
setup(name="re_support", version="1.0.0", description="Real estate post-handover customer support application", author="Your Company Name", author_email="user@example.com", packages=find_packages(), zip_safe=False, include_package_data=True, install_requires=install_requires)
""")

write_file("re_support/__init__.py", "__version__ = '1.0.0'")
write_file("re_support/patches.txt", "")
write_file("re_support/modules.txt", "Complaint Management\nDefect Snagging\nPossession Management\nRERA Escalation\nBuyer Portal\nReports Analytics")

write_file("re_support/hooks.py", """
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
""")

# --- 2. Config ---
write_file("re_support/config/__init__.py", "")
write_file("re_support/config/docs.py", "")
write_file("re_support/config/desktop.py", """
from frappe import _

def get_data():
    return [
        {
            "module_name": "Complaint Management",
            "color": "#C0392B",
            "icon": "octicon octicon-issue-opened",
            "label": _("Complaint Management"),
            "type": "module",
        },
        {
            "module_name": "Defect Snagging",
            "color": "#E67E22",
            "icon": "octicon octicon-tools",
            "label": _("Defect Snagging"),
            "type": "module",
        },
        {
            "module_name": "Possession Management",
            "color": "#2980B9",
            "icon": "octicon octicon-home",
            "label": _("Possession Management"),
            "type": "module",
        },
        {
            "module_name": "RERA Escalation",
            "color": "#8E44AD",
            "icon": "octicon octicon-law",
            "label": _("RERA Escalation"),
            "type": "module",
        },
        {
            "module_name": "Buyer Portal",
            "color": "#27AE60",
            "icon": "octicon octicon-globe",
            "label": _("Buyer Portal Settings"),
            "type": "module",
        },
        {
            "module_name": "Reports Analytics",
            "color": "#F39C12",
            "icon": "octicon octicon-bar-chart",
            "label": _("Reports & Analytics"),
            "type": "module",
        }
    ]
""")

# --- 3. Complaint Management ---
write_file("re_support/complaint_management/__init__.py", "")
write_file("re_support/complaint_management/doctype/__init__.py", "")

st_fields = [
    {"fieldname": "ticket_no", "fieldtype": "Data", "read_only": 1},
    {"fieldname": "buyer", "fieldtype": "Link", "options": "Contact", "reqd": 1},
    {"fieldname": "buyer_mobile", "fieldtype": "Data", "fetch_from": "buyer.mobile_no", "read_only": 1},
    {"fieldname": "project", "fieldtype": "Link", "options": "Project", "reqd": 1},
    {"fieldname": "unit_no", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "tower_block", "fieldtype": "Data"},
    {"fieldname": "floor_no", "fieldtype": "Int"},
    {"fieldname": "category", "fieldtype": "Link", "options": "Ticket Category", "reqd": 1},
    {"fieldname": "sub_category", "fieldtype": "Data"},
    {"fieldname": "priority", "fieldtype": "Select", "options": "Low\\nMedium\\nHigh\\nCritical"},
    {"fieldname": "description", "fieldtype": "Text", "reqd": 1},
    {"fieldname": "attachments", "fieldtype": "Attach"},
    {"fieldname": "assigned_to", "fieldtype": "Link", "options": "User"},
    {"fieldname": "assigned_team", "fieldtype": "Link", "options": "Department"},
    {"fieldname": "sla_policy", "fieldtype": "Link", "options": "SLA Policy"},
    {"fieldname": "sla_response_due", "fieldtype": "Datetime", "read_only": 1},
    {"fieldname": "sla_resolution_due", "fieldtype": "Datetime", "read_only": 1},
    {"fieldname": "first_response_at", "fieldtype": "Datetime"},
    {"fieldname": "response_breached", "fieldtype": "Check", "read_only": 1},
    {"fieldname": "resolution_breached", "fieldtype": "Check", "read_only": 1},
    {"fieldname": "status", "fieldtype": "Select", "options": "Open\\nAssigned\\nIn Progress\\nAwaiting Buyer\\nResolved\\nClosed\\nEscalated"},
    {"fieldname": "resolution_notes", "fieldtype": "Text Editor"},
    {"fieldname": "closed_at", "fieldtype": "Datetime"},
    {"fieldname": "buyer_rating", "fieldtype": "Rating"},
    {"fieldname": "buyer_feedback", "fieldtype": "Small Text"},
    {"fieldname": "rera_complaint", "fieldtype": "Link", "options": "RERA Complaint"},
    {"fieldname": "defect_report", "fieldtype": "Link", "options": "Defect Report"},
    {"fieldname": "internal_notes", "fieldtype": "Text Editor"},
    {"fieldname": "escalation_reason", "fieldtype": "Small Text"}
]
write_file("re_support/complaint_management/doctype/support_ticket/support_ticket.json", json.dumps({"is_submittable": 1, "custom": 1, "module": "Complaint Management", "name": "Support Ticket", "autoname": "TICK-.YYYY.MM.-.####", "fields": st_fields}, indent=4))
write_file("re_support/complaint_management/doctype/support_ticket/support_ticket.py", "import frappe\nfrom frappe.model.document import Document\nclass SupportTicket(Document):\n\tpass")
write_file("re_support/complaint_management/doctype/support_ticket/support_ticket.js", "// JS for Support Ticket")

tc_fields = [
    {"fieldname": "category_name", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "department", "fieldtype": "Select", "options": "Civil\\nElectrical\\nPlumbing\\nLegal\\nFinance\\nGeneral", "reqd": 1},
    {"fieldname": "default_sla", "fieldtype": "Link", "options": "SLA Policy"},
    {"fieldname": "auto_assign_role", "fieldtype": "Link", "options": "Role"},
    {"fieldname": "rera_risk", "fieldtype": "Check"},
    {"fieldname": "allow_buyer_create", "fieldtype": "Check"},
    {"fieldname": "email_template", "fieldtype": "Link", "options": "Email Template"},
    {"fieldname": "color_code", "fieldtype": "Color"},
    {"fieldname": "is_active", "fieldtype": "Check", "default": "1"}
]
write_file("re_support/complaint_management/doctype/ticket_category/ticket_category.json", json.dumps({"custom": 1, "module": "Complaint Management", "name": "Ticket Category", "fields": tc_fields}, indent=4))
write_file("re_support/complaint_management/doctype/ticket_category/ticket_category.py", "import frappe\nfrom frappe.model.document import Document\nclass TicketCategory(Document):\n\tpass")

sla_fields = [
    {"fieldname": "policy_name", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "applies_to_priority", "fieldtype": "Select", "options": "Low\\nMedium\\nHigh\\nCritical\\nAll"},
    {"fieldname": "response_time_hrs", "fieldtype": "Int", "reqd": 1},
    {"fieldname": "resolution_time_hrs", "fieldtype": "Int", "reqd": 1},
    {"fieldname": "escalate_after_hrs", "fieldtype": "Int"},
    {"fieldname": "escalate_to", "fieldtype": "Link", "options": "User"},
    {"fieldname": "notify_buyer_on_breach", "fieldtype": "Check"},
    {"fieldname": "notify_manager_on_breach", "fieldtype": "Check"},
    {"fieldname": "working_days_only", "fieldtype": "Check"},
    {"fieldname": "breach_message", "fieldtype": "Small Text"}
]
write_file("re_support/complaint_management/doctype/sla_policy/sla_policy.json", json.dumps({"custom": 1, "module": "Complaint Management", "name": "SLA Policy", "fields": sla_fields}, indent=4))
write_file("re_support/complaint_management/doctype/sla_policy/sla_policy.py", "import frappe\nfrom frappe.model.document import Document\nclass SLAPolicy(Document):\n\tpass")

make_dirs("re_support/complaint_management/report/sla_breach_report")
make_dirs("re_support/complaint_management/report/ticket_tat_by_category")

# --- 4. Defect Snagging ---
write_file("re_support/defect_snagging/__init__.py", "")
write_file("re_support/defect_snagging/doctype/__init__.py", "")

dr_fields = [
    {"fieldname": "report_no", "fieldtype": "Data", "read_only": 1},
    {"fieldname": "project", "fieldtype": "Link", "options": "Project", "reqd": 1},
    {"fieldname": "unit_no", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "tower_block", "fieldtype": "Data"},
    {"fieldname": "floor_no", "fieldtype": "Int"},
    {"fieldname": "buyer", "fieldtype": "Link", "options": "Contact", "reqd": 1},
    {"fieldname": "buyer_mobile", "fieldtype": "Data", "fetch_from": "buyer.mobile_no", "read_only": 1},
    {"fieldname": "inspection_date", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "inspector", "fieldtype": "Link", "options": "User", "reqd": 1},
    {"fieldname": "source_ticket", "fieldtype": "Link", "options": "Support Ticket"},
    {"fieldname": "inspection_type", "fieldtype": "Select", "options": "Pre-Handover Inspection\\nPost-Handover\\nRe-Inspection\\nAnnual"},
    {"fieldname": "defects", "fieldtype": "Table", "options": "Defect Item"},
    {"fieldname": "total_defects", "fieldtype": "Int", "read_only": 1},
    {"fieldname": "open_defects", "fieldtype": "Int", "read_only": 1},
    {"fieldname": "status", "fieldtype": "Select", "options": "Draft\\nUnder Review\\nIn Rectification\\nQC Pending\\nCompleted\\nBuyer Accepted"},
    {"fieldname": "qc_date", "fieldtype": "Date"},
    {"fieldname": "qc_inspector", "fieldtype": "Link", "options": "User"},
    {"fieldname": "qc_notes", "fieldtype": "Small Text"},
    {"fieldname": "buyer_remarks", "fieldtype": "Small Text"},
    {"fieldname": "buyer_signature", "fieldtype": "Signature"},
    {"fieldname": "completion_date", "fieldtype": "Date"},
    {"fieldname": "internal_notes", "fieldtype": "Text Editor"}
]
write_file("re_support/defect_snagging/doctype/defect_report/defect_report.json", json.dumps({"is_submittable": 1, "custom": 1, "module": "Defect Snagging", "name": "Defect Report", "autoname": "DEF-.YYYY.-.####", "fields": dr_fields}, indent=4))
write_file("re_support/defect_snagging/doctype/defect_report/defect_report.py", "import frappe\nfrom frappe.model.document import Document\nclass DefectReport(Document):\n\tpass")

di_fields = [
    {"fieldname": "area", "fieldtype": "Select", "options": "Living Room\\nKitchen\\nMaster Bedroom\\nBedroom 2\\nBathroom\\nToilet\\nBalcony\\nCommon Area\\nExterior", "reqd": 1},
    {"fieldname": "location_detail", "fieldtype": "Data"},
    {"fieldname": "defect_type", "fieldtype": "Select", "options": "Crack\\nSeepage\\nTiling\\nPaint\\nFixture\\nElectrical\\nPlumbing\\nCarpentry\\nFalse Ceiling\\nWaterproofing\\nOther", "reqd": 1},
    {"fieldname": "description", "fieldtype": "Small Text", "reqd": 1},
    {"fieldname": "photo", "fieldtype": "Attach"},
    {"fieldname": "severity", "fieldtype": "Select", "options": "Minor\\nModerate\\nMajor", "reqd": 1},
    {"fieldname": "contractor", "fieldtype": "Link", "options": "Supplier"},
    {"fieldname": "due_date", "fieldtype": "Date"},
    {"fieldname": "contractor_notes", "fieldtype": "Small Text"},
    {"fieldname": "rectification_photo", "fieldtype": "Attach"},
    {"fieldname": "resolved_on", "fieldtype": "Date"},
    {"fieldname": "item_status", "fieldtype": "Select", "options": "Open\\nAssigned\\nIn Progress\\nDone\\nRejected\\nCannot Rectify"},
    {"fieldname": "rejection_reason", "fieldtype": "Small Text"}
]
write_file("re_support/defect_snagging/doctype/defect_item/defect_item.json", json.dumps({"istable": 1, "custom": 1, "module": "Defect Snagging", "name": "Defect Item", "fields": di_fields}, indent=4))
write_file("re_support/defect_snagging/doctype/defect_item/defect_item.py", "import frappe\nfrom frappe.model.document import Document\nclass DefectItem(Document):\n\tpass")

ca_fields = [
    {"fieldname": "defect_report", "fieldtype": "Link", "options": "Defect Report", "reqd": 1},
    {"fieldname": "contractor", "fieldtype": "Link", "options": "Supplier", "reqd": 1},
    {"fieldname": "assignment_date", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "due_date", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "items_assigned", "fieldtype": "Int"},
    {"fieldname": "items_completed", "fieldtype": "Int", "read_only": 1},
    {"fieldname": "status", "fieldtype": "Select", "options": "Pending\\nIn Progress\\nCompleted\\nPartially Done\\nDefaulted"},
    {"fieldname": "remarks", "fieldtype": "Small Text"},
    {"fieldname": "purchase_order", "fieldtype": "Link", "options": "Purchase Order"}
]
write_file("re_support/defect_snagging/doctype/contractor_assignment/contractor_assignment.json", json.dumps({"custom": 1, "module": "Defect Snagging", "name": "Contractor Assignment", "autoname": "CASS-.YYYY.-.####", "fields": ca_fields}, indent=4))
write_file("re_support/defect_snagging/doctype/contractor_assignment/contractor_assignment.py", "import frappe\nfrom frappe.model.document import Document\nclass ContractorAssignment(Document):\n\tpass")

make_dirs("re_support/defect_snagging/report/defect_heatmap_by_unit")

# --- 5. Possession Management ---
write_file("re_support/possession_management/__init__.py", "")
write_file("re_support/possession_management/doctype/__init__.py", "")

pr_fields = [
    {"fieldname": "possession_no", "fieldtype": "Data", "read_only": 1},
    {"fieldname": "project", "fieldtype": "Link", "options": "Project", "reqd": 1},
    {"fieldname": "unit_no", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "tower_block", "fieldtype": "Data"},
    {"fieldname": "floor_no", "fieldtype": "Int"},
    {"fieldname": "buyer", "fieldtype": "Link", "options": "Contact", "reqd": 1},
    {"fieldname": "co_buyer", "fieldtype": "Link", "options": "Contact"},
    {"fieldname": "buyer_mobile", "fieldtype": "Data", "fetch_from": "buyer.mobile_no", "read_only": 1},
    {"fieldname": "booking_ref", "fieldtype": "Data"},
    {"fieldname": "sale_deed_date", "fieldtype": "Date"},
    {"fieldname": "total_consideration", "fieldtype": "Currency"},
    {"fieldname": "outstanding_dues", "fieldtype": "Currency"},
    {"fieldname": "dues_verified_by", "fieldtype": "Link", "options": "User"},
    {"fieldname": "dues_cleared", "fieldtype": "Check"},
    {"fieldname": "dues_cleared_date", "fieldtype": "Date"},
    {"fieldname": "oc_received", "fieldtype": "Check"},
    {"fieldname": "oc_number", "fieldtype": "Data"},
    {"fieldname": "oc_date", "fieldtype": "Date"},
    {"fieldname": "oc_copy", "fieldtype": "Attach"},
    {"fieldname": "noc_list", "fieldtype": "Table", "options": "NOC Document"},
    {"fieldname": "all_nocs_received", "fieldtype": "Check", "read_only": 1},
    {"fieldname": "scheduled_date", "fieldtype": "Datetime"},
    {"fieldname": "confirmed_by_buyer", "fieldtype": "Check"},
    {"fieldname": "pre_inspection_done", "fieldtype": "Check"},
    {"fieldname": "pre_inspection_date", "fieldtype": "Date"},
    {"fieldname": "defect_report", "fieldtype": "Link", "options": "Defect Report"},
    {"fieldname": "key_handover_date", "fieldtype": "Date"},
    {"fieldname": "handover_by", "fieldtype": "Link", "options": "User"},
    {"fieldname": "keys_count", "fieldtype": "Int"},
    {"fieldname": "welcome_kit_issued", "fieldtype": "Check"},
    {"fieldname": "utility_connections", "fieldtype": "Table", "options": "Utility Item"},
    {"fieldname": "buyer_signature", "fieldtype": "Signature"},
    {"fieldname": "witness_name", "fieldtype": "Data"},
    {"fieldname": "status", "fieldtype": "Select", "options": "Initiated\\nDues Check\\nNOC Collection\\nScheduled\\nKey Handover\\nCompleted"},
    {"fieldname": "remarks", "fieldtype": "Text Editor"}
]
write_file("re_support/possession_management/doctype/possession_request/possession_request.json", json.dumps({"is_submittable": 1, "custom": 1, "module": "Possession Management", "name": "Possession Request", "autoname": "POSS-.YYYY.MM.-.####", "fields": pr_fields}, indent=4))
write_file("re_support/possession_management/doctype/possession_request/possession_request.py", "import frappe\nfrom frappe.model.document import Document\nclass PossessionRequest(Document):\n\tpass")

noc_fields = [
    {"fieldname": "noc_type", "fieldtype": "Select", "options": "Bank NOC\\nSociety NOC\\nWater Connection NOC\\nFire NOC\\nLift Inspection\\nProperty Tax Clearance\\nOther", "reqd": 1},
    {"fieldname": "issuing_authority", "fieldtype": "Data"},
    {"fieldname": "mandatory", "fieldtype": "Check"},
    {"fieldname": "received", "fieldtype": "Check"},
    {"fieldname": "received_date", "fieldtype": "Date"},
    {"fieldname": "expiry_date", "fieldtype": "Date"},
    {"fieldname": "document", "fieldtype": "Attach"},
    {"fieldname": "remarks", "fieldtype": "Small Text"}
]
write_file("re_support/possession_management/doctype/noc_document/noc_document.json", json.dumps({"istable": 1, "custom": 1, "module": "Possession Management", "name": "NOC Document", "fields": noc_fields}, indent=4))
write_file("re_support/possession_management/doctype/noc_document/noc_document.py", "import frappe\nfrom frappe.model.document import Document\nclass NOCDocument(Document):\n\tpass")

# Dummy Utility Item so Frappe table works
ui_fields = [{"fieldname": "utility", "fieldtype": "Data"}]
write_file("re_support/possession_management/doctype/utility_item/utility_item.json", json.dumps({"istable": 1, "custom": 1, "module": "Possession Management", "name": "Utility Item", "fields": ui_fields}, indent=4))
write_file("re_support/possession_management/doctype/utility_item/utility_item.py", "import frappe\nfrom frappe.model.document import Document\nclass UtilityItem(Document):\n\tpass")

pc_fields = [
    {"fieldname": "checklist_name", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "project_type", "fieldtype": "Select", "options": "Apartment\\nVilla\\nCommercial\\nPlotted"},
    {"fieldname": "items", "fieldtype": "Table", "options": "Utility Item"},
    {"fieldname": "is_active", "fieldtype": "Check", "default": "1"}
]
write_file("re_support/possession_management/doctype/possession_checklist/possession_checklist.json", json.dumps({"custom": 1, "module": "Possession Management", "name": "Possession Checklist", "fields": pc_fields}, indent=4))
write_file("re_support/possession_management/doctype/possession_checklist/possession_checklist.py", "import frappe\nfrom frappe.model.document import Document\nclass PossessionChecklist(Document):\n\tpass")

write_file("re_support/possession_management/workflow/possession_workflow.json", "{}")

# --- 6. RERA Escalation ---
write_file("re_support/rera_escalation/__init__.py", "")
write_file("re_support/rera_escalation/doctype/__init__.py", "")

rc_fields = [
    {"fieldname": "rera_complaint_no", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "rera_portal_ref", "fieldtype": "Data"},
    {"fieldname": "source_ticket", "fieldtype": "Link", "options": "Support Ticket"},
    {"fieldname": "buyer", "fieldtype": "Link", "options": "Contact", "reqd": 1},
    {"fieldname": "buyer_advocate", "fieldtype": "Data"},
    {"fieldname": "project", "fieldtype": "Link", "options": "Project", "reqd": 1},
    {"fieldname": "unit_no", "fieldtype": "Data"},
    {"fieldname": "complaint_type", "fieldtype": "Select", "options": "Delay in Possession\\nConstruction Defect\\nFalse Representation\\nNon-disclosure\\nAgreement Breach\\nOther"},
    {"fieldname": "filed_date", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "state_rera", "fieldtype": "Select", "options": "MahaRERA\\nRERA Karnataka\\nUP RERA\\nGujarat RERA\\nHaryana RERA\\nOther"},
    {"fieldname": "authority_address", "fieldtype": "Small Text"},
    {"fieldname": "first_notice_date", "fieldtype": "Date"},
    {"fieldname": "response_deadline", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "legal_team", "fieldtype": "Link", "options": "User"},
    {"fieldname": "external_counsel", "fieldtype": "Data"},
    {"fieldname": "hearing_date", "fieldtype": "Date"},
    {"fieldname": "hearing_venue", "fieldtype": "Data"},
    {"fieldname": "response_logs", "fieldtype": "Table", "options": "RERA Response Log"},
    {"fieldname": "attachments", "fieldtype": "Attach"},
    {"fieldname": "developer_position", "fieldtype": "Text Editor"},
    {"fieldname": "settlement_offered", "fieldtype": "Check"},
    {"fieldname": "settlement_amount", "fieldtype": "Currency"},
    {"fieldname": "outcome", "fieldtype": "Select", "options": "Pending\\nIn Favour of Developer\\nAgainst Developer\\nSettled\\nWithdrawn\\nDismissed"},
    {"fieldname": "outcome_date", "fieldtype": "Date"},
    {"fieldname": "penalty_amount", "fieldtype": "Currency"},
    {"fieldname": "penalty_paid", "fieldtype": "Check"},
    {"fieldname": "penalty_jv", "fieldtype": "Link", "options": "Journal Entry"},
    {"fieldname": "appeal_filed", "fieldtype": "Check"},
    {"fieldname": "appeal_tribunal", "fieldtype": "Data"},
    {"fieldname": "remarks", "fieldtype": "Text Editor"}
]
write_file("re_support/rera_escalation/doctype/rera_complaint/rera_complaint.json", json.dumps({"is_submittable": 1, "custom": 1, "module": "RERA Escalation", "name": "RERA Complaint", "autoname": "RERA-.YYYY.-.####", "fields": rc_fields}, indent=4))
write_file("re_support/rera_escalation/doctype/rera_complaint/rera_complaint.py", "import frappe\nfrom frappe.model.document import Document\nclass RERAComplaint(Document):\n\tpass")

rrl_fields = [
    {"fieldname": "log_date", "fieldtype": "Date", "reqd": 1},
    {"fieldname": "activity_type", "fieldtype": "Select", "options": "Response Filed\\nHearing Attended\\nDocument Submitted\\nNotice Received\\nSettlement Discussion\\nOrder Received", "reqd": 1},
    {"fieldname": "description", "fieldtype": "Text", "reqd": 1},
    {"fieldname": "filed_by", "fieldtype": "Link", "options": "User"},
    {"fieldname": "document", "fieldtype": "Attach"},
    {"fieldname": "next_action", "fieldtype": "Small Text"},
    {"fieldname": "next_action_date", "fieldtype": "Date"}
]
write_file("re_support/rera_escalation/doctype/rera_response_log/rera_response_log.json", json.dumps({"istable": 1, "custom": 1, "module": "RERA Escalation", "name": "RERA Response Log", "fields": rrl_fields}, indent=4))
write_file("re_support/rera_escalation/doctype/rera_response_log/rera_response_log.py", "import frappe\nfrom frappe.model.document import Document\nclass RERAResponseLog(Document):\n\tpass")

make_dirs("re_support/rera_escalation/report/rera_risk_dashboard")

# --- 7. Buyer Portal ---
write_file("re_support/buyer_portal/__init__.py", "")
write_file("re_support/buyer_portal/doctype/__init__.py", "")

bps_fields = [
    {"fieldname": "portal_enabled", "fieldtype": "Check"},
    {"fieldname": "portal_url", "fieldtype": "Data"},
    {"fieldname": "allow_ticket_create", "fieldtype": "Check"},
    {"fieldname": "allow_ticket_attachment", "fieldtype": "Check"},
    {"fieldname": "allowed_categories", "fieldtype": "Table MultiSelect"},
    {"fieldname": "show_possession_status", "fieldtype": "Check"},
    {"fieldname": "show_defect_report", "fieldtype": "Check"},
    {"fieldname": "whatsapp_notify", "fieldtype": "Check"},
    {"fieldname": "whatsapp_api_provider", "fieldtype": "Select", "options": "Interakt\\nWati\\nAiSensy\\nGupshup\\nCustom"},
    {"fieldname": "whatsapp_api_key", "fieldtype": "Password"},
    {"fieldname": "email_notify", "fieldtype": "Check"},
    {"fieldname": "email_notify_template", "fieldtype": "Link", "options": "Email Template"},
    {"fieldname": "support_email", "fieldtype": "Data"},
    {"fieldname": "support_phone", "fieldtype": "Data"},
    {"fieldname": "office_hours", "fieldtype": "Data"},
    {"fieldname": "portal_logo", "fieldtype": "Attach Image"},
    {"fieldname": "welcome_message", "fieldtype": "Text"},
    {"fieldname": "footer_links", "fieldtype": "Table"},
    {"fieldname": "buyer_auth_method", "fieldtype": "Select", "options": "OTP via Mobile\\nEmail OTP\\nPassword\\nBoth"},
    {"fieldname": "session_timeout_mins", "fieldtype": "Int"}
]
write_file("re_support/buyer_portal/doctype/buyer_portal_settings/buyer_portal_settings.json", json.dumps({"issingle": 1, "custom": 1, "module": "Buyer Portal", "name": "Buyer Portal Settings", "fields": bps_fields}, indent=4))
write_file("re_support/buyer_portal/doctype/buyer_portal_settings/buyer_portal_settings.py", "import frappe\nfrom frappe.model.document import Document\nclass BuyerPortalSettings(Document):\n\tpass")

pn_fields = [
    {"fieldname": "buyer", "fieldtype": "Link", "options": "Contact", "reqd": 1},
    {"fieldname": "notification_type", "fieldtype": "Select", "options": "Ticket Created\\nStatus Changed\\nSLA Breach\\nPossession Update\\nDefect Update\\nRERA Notice"},
    {"fieldname": "channel", "fieldtype": "Select", "options": "WhatsApp\\nEmail\\nSMS\\nIn-App"},
    {"fieldname": "source_document", "fieldtype": "Dynamic Link"},
    {"fieldname": "message", "fieldtype": "Text"},
    {"fieldname": "sent_at", "fieldtype": "Datetime"},
    {"fieldname": "delivery_status", "fieldtype": "Select", "options": "Sent\\nDelivered\\nRead\\nFailed"},
    {"fieldname": "failure_reason", "fieldtype": "Small Text"}
]
write_file("re_support/buyer_portal/doctype/portal_notification/portal_notification.json", json.dumps({"custom": 1, "module": "Buyer Portal", "name": "Portal Notification", "autoname": "PNOT-.YYYY.MM.DD.-.##", "fields": pn_fields}, indent=4))
write_file("re_support/buyer_portal/doctype/portal_notification/portal_notification.py", "import frappe\nfrom frappe.model.document import Document\nclass PortalNotification(Document):\n\tpass")

write_file("re_support/buyer_portal/templates/pages/buyer_portal.html", "<!-- Buyer Portal -->")
write_file("re_support/buyer_portal/templates/pages/ticket_detail.html", "<!-- Ticket Detail -->")
write_file("re_support/buyer_portal/templates/pages/possession_status.html", "<!-- Possession Status -->")

write_file("re_support/buyer_portal/api.py", """
import frappe

@frappe.whitelist(allow_guest=False)
def get_buyer_tickets(buyer_mobile):
    \"\"\"Return all tickets for the authenticated buyer.\"\"\"
    return frappe.get_list('Support Ticket',
        filters={'buyer_mobile': buyer_mobile},
        fields=['ticket_no','category','status','sla_resolution_due','priority'],
        order_by='creation desc')

@frappe.whitelist(allow_guest=False)
def create_ticket(project, unit_no, category, description, attachments=None):
    \"\"\"Create a new support ticket from the buyer portal.\"\"\"
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
    \"\"\"Return possession request status for buyer's unit.\"\"\"
    return frappe.db.get_value('Possession Request',
        {'unit_no': unit_no, 'project': project},
        ['possession_no','status','scheduled_date','key_handover_date'],
        as_dict=True)
""")

# --- 8. Reports Analytics ---
make_dirs("re_support/reports_analytics/report/support_dashboard")
make_dirs("re_support/reports_analytics/report/team_productivity")
write_file("re_support/reports_analytics/dashboard_chart/open_tickets_by_project.json", "{}")
write_file("re_support/reports_analytics/dashboard_chart/sla_compliance_rate.json", "{}")

# --- 9. Utils ---
write_file("re_support/utils/__init__.py", "")

write_file("re_support/utils/sla_engine.py", """
import frappe
from frappe.utils import add_to_date, now_datetime

def set_sla_due_dates(doc, method=None):
    \"\"\"Auto-set SLA response and resolution deadlines on ticket creation.\"\"\"
    if not doc.sla_policy:
        cat = frappe.get_doc("Ticket Category", doc.category)
        doc.sla_policy = cat.default_sla
    if doc.sla_policy:
        sla = frappe.get_doc("SLA Policy", doc.sla_policy)
        now = now_datetime()
        doc.sla_response_due   = add_to_date(now, hours=sla.response_time_hrs)
        doc.sla_resolution_due = add_to_date(now, hours=sla.resolution_time_hrs)

def check_sla_breaches():
    \"\"\"Scheduled job: flag breached tickets and escalate.\"\"\"
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
""")

write_file("re_support/utils/notifications.py", "")
write_file("re_support/utils/validators.py", "")

print("Scaffolding complete.")
