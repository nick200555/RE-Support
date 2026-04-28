import frappe
from frappe.model.document import Document

class RESupport(Document):
	def on_update(self):
		pass

	def get_context(self, context):
		# Add workspace specific context here
		pass

@frappe.whitelist()
def get_property_stats():
	"""
	Helper method to get property statistics for the dashboard
	"""
	return {
		"open_leads": frappe.db.count("Property Lead", {"status": ["!=", "Converted"]}),
		"available_units": frappe.db.count("Unit Inventory", {"status": "Available"}),
		"active_leases": frappe.db.count("Lease Agreement", {"status": "Active"}),
		"pending_tickets": frappe.db.count("Maintenance Ticket", {"status": ["in", ["Open", "In Progress"]]})
	}

@frappe.whitelist()
def get_onboarding_status():
	"""
	Helper method to track onboarding progress
	"""
	return {
		"has_properties": frappe.db.count("Property Master") > 0,
		"has_units": frappe.db.count("Unit Inventory") > 0,
		"has_settings": frappe.db.count("RE Support Settings") > 0
	}

@frappe.whitelist()
def has_workspace_access(user=None):
	"""
	Role visibility helper to check if current user has access to the workspace features
	"""
	if not user:
		user = frappe.session.user
		
	roles = frappe.get_roles(user)
	allowed_roles = ["System Manager", "Property Manager", "Sales Manager", "Maintenance Manager", "Lease Manager", "Finance Manager"]
	
	return any(role in allowed_roles for role in roles)
