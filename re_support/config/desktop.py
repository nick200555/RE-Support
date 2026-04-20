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
            "type": "module"
        },
        {
            "module_name": "Reports Analytics",
            "color": "#F39C12",
            "icon": "octicon octicon-bar-chart",
            "label": _("Reports & Analytics"),
            "type": "module"
        }
    ]
