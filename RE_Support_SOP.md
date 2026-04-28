# 📘 RE_Support — Standard Operating Procedure (SOP)

### Functional Guide for Real Estate Operations & Property Management Teams

---

> **Document Version:** 1.0  
> **Application:** RE_Support on ERPNext v15  
> **Audience:** Real Estate Managers, Sales Teams, CRM Executives, Legal Teams, Finance Teams, Property Coordinators, Support Teams  
> **Support:** support@resupport.internal

---

## 📋 Table of Contents

1. [Getting Started — First Login](#1-getting-started--first-login)
2. [Module 1 — Property & Inventory Management](#2-module-1--property--inventory-management)
3. [Module 2 — Lead & CRM Management](#3-module-2--lead--crm-management)
4. [Module 3 — Booking & Sales Management](#4-module-3--booking--sales-management)
5. [Module 4 — Lease & Rental Management](#5-module-4--lease--rental-management)
6. [Module 5 — Maintenance & Facility Support](#6-module-5--maintenance--facility-support)
7. [Module 6 — Finance & Payment Management](#7-module-6--finance--payment-management)
8. [Module 7 — Legal & Documentation](#8-module-7--legal--documentation)
9. [Module 8 — Reports & Analytics](#9-module-8--reports--analytics)
10. [Daily / Weekly / Monthly Operating Checklist](#10-daily--weekly--monthly-operating-checklist)
11. [User Roles & Who Does What](#11-user-roles--who-does-what)
12. [Frequently Asked Questions](#12-frequently-asked-questions)
13. [Support & Contact](#13-support--contact)

---

## 1. Getting Started — First Login

### 1.1 Access the Application

1. Open your browser and go to your RE_Support URL:  
   `https://erp.yourrealestate.com`
2. Login with your ERPNext credentials (provided by your administrator).
3. On the left sidebar, click **RE_Support** workspace.
4. You will see the **RE_Support Dashboard** with quick-access shortcuts at the top:
   - 🏢 Property Inventory
   - 🟢 Active Bookings
   - 🛠️ Maintenance SLAs
   - ⚖️ Legal & RERA Alerts

---

### 1.2 Initial Company Setup (One-Time — Admin Only)

> **Who does this:** Real Estate Admin (first time only)

| Step | Action | Where |
|---|---|---|
| 1 | Create your Branch/Company | ERPNext → Accounting → Company |
| 2 | Create Default Project | ERPNext → Projects → Project |
| 3 | Define Property Types | RE_Support → Setup → Property Type Master |
| 4 | Initialize Scheduler Overview | ERPNext → Settings → Scheduled Job Type |
| 5 | Run Demo Data (optional) | `bench execute re_support.setup.demo.run` |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator

Go to **ERPNext → HR → User** and assign each person their role:

| Role | Assign To |
|---|---|
| Real Estate Admin | System Admin / IT Lead |
| Sales Executive | Sales Reps / Brokers |
| CRM Executive | CRM Manager / Support Agent | 
| Property Manager | Inventory Manager |
| Leasing Manager | Rent Coordinator |
| Accounts Executive | Finance / Collections |
| Legal Officer | Legal / Compliance Team |
| Maintenance Supervisor| Facility Manager / Technician |

---

## 2. Module 1 — Property & Inventory Management

> **Purpose:** Setup and maintain real-time unit tracking. Manage everything from towers and floors down to unit status.

---

### 2.1 SOP — Property Creation

**Who:** Property Manager / Admin  
**When:** At the launch of a new project or property

| Step | Action |
|---|---|
| 1 | Go to **Property Management → Property Parent** |
| 2 | Click **+ New** |
| 3 | Enter **Property Name** and select **Company/Project** |
| 4 | Set **Property Type** (Residential / Commercial / Retail) |
| 5 | Define **Total Area** and **Location Details** |
| 6 | Set **Status** = "Under Construction" or "Ready to Move" |
| 7 | Click **Save** |

✅ **Expected Result:** Property is created. Default cost centres are automatically established.

---

### 2.2 SOP — Tower/Block and Floor Management

**Who:** Property Manager  
**When:** Setting up the internal architecture of a Property

| Step | Action |
|---|---|
| 1 | Go to **Property Management → Property Block / Tower** |
| 2 | Click **+ New** and link to the previously created **Property** |
| 3 | Specify **Tower Name** (e.g., Tower A) |
| 4 | Click Save. Then navigate to **Property Floor** |
| 5 | Click **+ New**, link to **Tower A**, and specify **Floor Number** |
| 6 | Click **Save** |

---

### 2.3 SOP — Unit Inventory Management

**Who:** Property Manager  
**When:** Generating addressable units for sale or lease

| Step | Action |
|---|---|
| 1 | Go to **Property Management → Unit Inventory** |
| 2 | Click **+ New** |
| 3 | Link **Property**, **Tower**, and **Floor** |
| 4 | Enter **Unit No** (e.g., A-101), **Carpet Area**, and **Facing** (e.g., North) |
| 5 | Designate **Unit Type** (e.g., 3BHK, Retail Shop) |
| 6 | Upload **Floor Plan** in the Media section |
| 7 | Save |

✅ **Expected Result:** Unit shows up on the inventory dashboard as "Available".

---

### 2.4 SOP — Amenity Mapping & Media Upload

**Who:** Property Manager  
**When:** Beautifying unit listings for brokers and portals

| Step | Action |
|---|---|
| 1 | Open the **Unit Inventory** record |
| 2 | Scroll to **Amenities** table and add features (e.g., Pool View, Corner Unit) |
| 3 | Go to the **Media & Attachments** section |
| 4 | Upload high-resolution images, walkthrough videos, and 3D tours |
| 5 | Define a primary thumbnail |
| 6 | Save |

---

### 2.5 SOP — Property Status & Availability Tracking

**Who:** Sales Executive / Property Manager  
**When:** Unit changes hands or becomes unavailable

| Step | Action |
|---|---|
| 1 | Open **Unit Inventory** |
| 2 | The field **Availability Status** acts as the single source of truth |
| 3 | Valid statuses: `Available`, `Hold`, `Booked`, `Sold`, `Leased`, `Maintenance` |
| 4 | Do not change status manually if booked — the system will auto-update it when a Booking is approved. |

---

## 3. Module 2 — Lead & CRM Management

> **Purpose:** Capture inquiries from multiple sources, assign to brokers, and push them down the sales funnel via site visits.

---

### 3.1 SOP — Lead Capture & Broker Assignment

**Who:** CRM Executive / Sales Admin  
**When:** A new inquiry arrives from website, portal, or walk-in

| Step | Action |
|---|---|
| 1 | Go to **CRM Management → Real Estate Lead** |
| 2 | Click **+ New** |
| 3 | Enter **Lead Name**, **Mobile Number**, and **Source** (e.g., 99acres) |
| 4 | Specify **Interested Property** or **Unit Type** |
| 5 | Go to **Broker Assignment** field and select a registered **Broker** or **Internal Sales Rep** |
| 6 | Save |

✅ **Expected Result:** Broker receives an automated WhatsApp/Email notification.

---

### 3.2 SOP — Site Visit Scheduling

**Who:** Sales Executive  
**When:** Lead agrees to visit the property

| Step | Action |
|---|---|
| 1 | Open the **Real Estate Lead** record |
| 2 | Click **Create → Site Visit** from the top right button |
| 3 | Enter **Visit Date** and **Time Slot** |
| 4 | Select the **Show Flat** or specific **Unit** to be inspected |
| 5 | Save. Status becomes `Scheduled` |
| 6 | After the visit, update Status to `Completed` and fill **Visit Feedback** |

---

### 3.3 SOP — CRM Follow-Up & Enquiry Management

**Who:** CRM Executive / Sales Executive  
**When:** Ongoing follow-downs

| Step | Action |
|---|---|
| 1 | From the Lead, click **Add Task** or use the **Communications** timeline |
| 2 | Log call outcomes (e.g., "Interested in 3BHK, needs loan details") |
| 3 | Schedule a **Next Follow-up Date** |
| 4 | System will send a reminder on the dashboard on the follow-up day |

---

### 3.4 SOP — Lead Conversion Tracking

**Who:** Sales Executive  
**When:** Lead is ready to pay a booking token

| Step | Action |
|---|---|
| 1 | Open the Lead |
| 2 | Click **Convert to Customer** |
| 3 | ERPNext creates a Customer profile |
| 4 | Set the lead's **Status** = `Converted` |
| 5 | Proceed to Module 3 (Booking) |

---

## 4. Module 3 — Booking & Sales Management

> **Purpose:** Process the financial transaction of locking a unit, managing commissions, and handling sales documentation.

---

### 4.1 SOP — Unit Booking & Token Advance Collection

**Who:** Sales Executive  
**When:** Customer commits to a unit

| Step | Action |
|---|---|
| 1 | Go to **Booking Management → Unit Booking** |
| 2 | Click **+ New**, select **Customer** and select the **Unit Inventory** |
| 3 | Set the **Agreed Value** (Total Sale Price) |
| 4 | Enter **Token Amount** received |
| 5 | Attach transaction proof or ERPNext Payment Entry reference |
| 6 | Set Status to `Pending Approval` |
| 7 | Save |

✅ **Expected Result:** Unit status auto-changes to `Hold`.

---

### 4.2 SOP — Booking Approval & Sales Agreement Workflow

**Who:** Sales Manager / Admin  
**When:** Formalizing the token

| Step | Action |
|---|---|
| 1 | Open `Pending Approval` **Unit Booking** |
| 2 | Verify KYC and payment details |
| 3 | Change Status to `Approved` |
| 4 | Unit status auto-updates to `Booked` |
| 5 | Click **Create → Sales Agreement** |
| 6 | Generate the Draft Agreement using ERPNext Print Formats |

---

### 4.3 SOP — Payment Plan Setup

**Who:** Accounts Executive / Sales Manager  
**When:** After booking approval

| Step | Action |
|---|---|
| 1 | In the **Unit Booking** record, navigate to the **Payment Schedule** table |
| 2 | Select a **Payment Plan Template** (e.g., Construction Linked, 10:90, CLP) |
| 3 | The system auto-calculates installment dates and amounts based on milestones |
| 4 | Click Save. |

✅ **Expected Result:** Finance dashboard will populate with upcoming tranche invoices.

---

### 4.4 SOP — Cancellation Handling & Booking Transfer

**Who:** CRM Manager / Finance  
**When:** User backs out or shifts units

**To Cancel:**
1. Open **Unit Booking** → click **Cancel Booking**.
2. Specify **Cancellation Reason**.
3. System will calculate **Cancellation Charges** based on company policy.
4. Unit inventory reverts to `Available`.

**To Transfer:**
1. Use **Create → Transfer Booking**.
2. Select the new **Unit Number**.
3. Adjust price differential via Journal Entry.

---

### 4.5 SOP — Brokerage Commission Tracking

**Who:** Accounts Executive  
**When:** Milestones are hit (e.g., 20% payment received)

| Step | Action |
|---|---|
| 1 | Go to **Booking Management → Brokerage Payout** |
| 2 | Create **+ New**, link to **Booking** and **Broker** |
| 3 | Calculate commission (e.g., 2% of Agreement Value) |
| 4 | Submit to accounts for clearance |

---

## 5. Module 4 — Lease & Rental Management

> **Purpose:** For leased commercial or residential assets — managing the tenant lifecycle from onboarding to exit.

---

### 5.1 SOP — Tenant Onboarding & Lease Agreement Creation

**Who:** Leasing Manager  
**When:** Tenant finalizes an asset

| Step | Action |
|---|---|
| 1 | Go to **Rental Management → Lease Agreement** |
| 2 | Click **+ New**, select **Tenant (Customer)** and **Unit** |
| 3 | Enter **Lease Start Date** & **Lease End Date** |
| 4 | Define **Monthly Rent Amount** & **Lock-in Period** |
| 5 | Enter **Security Deposit Amount** |
| 6 | Ensure KYC documents are uploaded in the attachments |
| 7 | Submit |

✅ **Expected Result:** Unit status changes to `Leased`. Rent scheduler activates.

---

### 5.2 SOP — Security Deposit Tracking

**Who:** Accounts Executive  
**When:** During onboarding or exit

1. Security Deposit amount is mapped to a liability Account.
2. Link the **Payment Entry** to the Lease Agreement.
3. Upon exit, use the **Refund Deposit** action to settle remaining dues minus repair costs.

---

### 5.3 SOP — Rent Schedule Generation & Reminders

**Who:** Accounts / System  
**When:** 1st of every month

| Step | Action |
|---|---|
| 1 | The ERPNext Scheduler automatically creates **Sales Invoices** for all active Lease Agreements on the specified billing day. |
| 2 | **Rent Reminders**: Email & SMS alerts are auto-dispatched 5 days before the due date. |
| 3 | To manually invoke, click **Generate Rent Invoice** on the Lease record. |

---

### 5.4 SOP — Penalty Calculation

**Who:** System / Accounts  
**When:** Invoice passes the due date

1. If standard rent = ₹50,000 and due date is 5th.
2. On 6th, the scheduler detects overdue invoice.
3. A **Debit Note** (Penalty) is created (e.g., ₹500/day or 2% late fee) and added to the tenant ledger.

---

### 5.5 SOP — Renewal Handling & Move-in / Move-out Process

**Who:** Facility Manager / Leasing Manager  
**When:** Lease nears expiry

| Step | Action |
|---|---|
| 1 | 60 days to expiry, Status changes to `Pending Renewal`. |
| 2 | Click **Renew Agreement**, adjust escalation %, save new term. |
| 3 | **Move-out**: Click **Initiate Vacating**. Inspect unit, define defect deductions, process full-and-final settlement (F&F), and revert Unit to `Available`. |

---

## 6. Module 5 — Maintenance & Facility Support

> **Purpose:** Manage post-handover support, ticketing, SLA compliance, and facility management tasks.

---

### 6.1 SOP — Complaint Registration & Ticket Assignment

**Who:** Buyer via Portal / Support Agent  
**When:** A defect or issue is reported

| Step | Action |
|---|---|
| 1 | Buyer logs into the portal and submits a ticket, OR Agent goes to **Support Management → Support Ticket** and clicks **+ New**. |
| 2 | Specify **Unit Number**, **Category** (e.g., Plumbing, Civil), and **Issue Description**. |
| 3 | Based on Category, the ticket is auto-assigned to the appropriate **Department/Technician**. |
| 4 | SLA Deadlines populate automatically (e.g., Resolve within 48h). |

---

### 6.2 SOP — Technician Scheduling & Vendor Allocation

**Who:** Maintenance Supervisor  
**When:** Execution requires third-party help

| Step | Action |
|---|---|
| 1 | Open the ticket (Status: `In Progress`) |
| 2 | If an external vendor is needed, click **Assign Vendor** and select from the Supplier master. |
| 3 | Schedule a **Visit Date** for the technician. |
| 4 | Once resolved, upload rectification photos. |

---

### 6.3 SOP — Preventive Maintenance & AMC Tracking

**Who:** Facility Manager  
**When:** Annual/Monthly facility upkeep (Lifts, Generators)

| Step | Action |
|---|---|
| 1 | Go to **Facility Support → Asset Maintenance** |
| 2 | Map the Asset (e.g., Tower A Lift 1) |
| 3 | Define frequency (e.g., Monthly Inspection) |
| 4 | System creates **Maintenance Task** auto-assigned to the vendor based on AMC terms. |

---

### 6.4 SOP — Escalation Management

**Who:** System / Support Manager  
**When:** SLA breaches occur

1. The Background job `check_sla_breaches` runs every 30 minutes.
2. If `sla_resolution_due` < NOW, status becomes `Escalated`.
3. Support Manager receives an immediate email/WhatsApp alert.

---

## 7. Module 6 — Finance & Payment Management

> **Purpose:** Complete ledger integration, invoicing, receipt processing, and reconciliation.

---

### 7.1 SOP — Invoice Generation & Customer Payment Tracking

**Who:** Accounts Executive  
**When:** A milestone block is completed

| Step | Action |
|---|---|
| 1 | On the **Unit Booking**, navigate to the **Payment Schedule** |
| 2 | If milestone = Reached, click **Generate Invoice** |
| 3 | Mail dispatched automatically to the Customer |
| 4 | When funds hit the bank, create a **Payment Entry**, linking it to the Sales Invoice |

---

### 7.2 SOP — EMI/Payment Plan Tracking & Overdue Follow-up

**Who:** Collections Team  
**When:** Payments are late

| Step | Action |
|---|---|
| 1 | Go to **Aging Report / Payment Overview Dashboard**. |
| 2 | Identify overdues > 15 days. |
| 3 | Use the bulk **Send Reminder** action to trigger Demand Letters. |
| 4 | Implement Dunning rules (interest addition on overdues). |

---

### 7.3 SOP — Refund Processing & GST Handling

**Who:** Accounts Manager  
**When:** Booking is cancelled

1. Approve the Cancellation document.
2. Ensure GST liability is reversed via **Credit Note**.
3. Generate **Payment Entry (Pay)** to the Customer's bank details for the refund amount.

---

## 8. Module 7 — Legal & Documentation

> **Purpose:** End-to-end possession orchestration, NOC management, RERA tracking, and compliance.

---

### 8.1 SOP — KYC Verification & Document Upload

**Who:** Legal Officer  
**When:** After Booking

| Step | Action |
|---|---|
| 1 | Open the **Customer** profile |
| 2 | Go to Attachments: upload Pan, Aadhar, Company COI |
| 3 | Use the **KYC Status** dropdown to approve |

---

### 8.2 SOP — Possession Workflow & NOC Issuance

**Who:** Legal Officer / Possession Exec  
**When:** Building OC received, unit ready for possession

**Possession Request — 6-State Workflow:**

```
Initiated ──► DuesCheck ──► NOCCollection ──► Scheduled ──► KeyHandover ──► Completed
```

| Step | Action |
|---|---|
| 1 | Create **Possession Request** for the Unit |
| 2 | Finance confirms `dues_cleared = Yes` |
| 3 | Legal collects Bank NOC, Society NOC, Fire NOC, etc. `all_nocs_received = Yes` |
| 4 | Upload `oc_copy` |
| 5 | Schedule key handover. Record `keys_count` and signature. Status → `Completed` |

---

### 8.3 SOP — Legal Approval Workflow & Ownership Transfer

**Who:** Legal Officer  
**When:** Transferring deeds

1. Execute **Sale Deed** registration in Sub-registrar office.
2. Record **Registration Number** in the Unit Booking record.
3. System registers **Ownership Transfer**, marking unit as `Sold`. Admin creates user credentials for the buyer portal.

---

### 8.4 SOP — RERA Compliance & Escalation Tracking

**Who:** Legal Team  
**When:** An official complaint is lodged

| Step | Action |
|---|---|
| 1 | Go to **Legal → RERA Complaint** |
| 2 | Create new record, link to existing **Support Ticket** (if any) |
| 3 | Fill in **RERA Reference Number** and **Response Deadline** |
| 4 | Use the **RERA Response Log** child table to document hearing dates, filings, and settlements |
| 5 | System issues 48hr alerts before response deadlines. |

---

## 9. Module 8 — Reports & Analytics

> **Purpose:** Leverage Frappe Script Reports and dashboards to execute data-driven management decisions.

---

### 9.1 SOP — Dashboards Overview

**Who:** Management / Leadership  
**When:** Daily review

- **Sales Pipeline Dashboard:** Track leads vs. scheduled visits vs. conversions.
- **Booking Conversion Reports:** Analyze lead source drop-offs.
- **Occupancy Analytics:** Visualize leased vs available units.
- **Maintenance SLA Dashboard:** Measure tickets resolved within SLA vs total breaches.

---

### 9.2 SOP — Generating Analytical Reports

**Who:** Analysts / Managers  
**When:** Weekly/Monthly reporting

| Report Name | What it shows | Filters |
|---|---|---|
| **Property Inventory Dashboard** | Real-time map of blocks/floors and Available/Booked/Hold statuses | Project, Status |
| **Rent Collection Reports** | Invoices generated vs collected; outstanding receivables | Month, Property |
| **Overdue Payment Analytics** | Customers defaulting on milestones, Dunning status | Aging Bucket |
| **Broker Performance Dashboard** | Leads converted by broker, payouts pending | Broker, Date Range|
| **Project Defect Heatmap** | High frequency snags mapped to specific contractors | Project, Severity |

---

## 10. Daily / Weekly / Monthly Operating Checklist

### 10.1 Daily Checklist (Ops / Support)
- [ ] **Lead Follow-ups**: Check pending calls and update CRMs.
- [ ] **Booking Reviews**: Approve any pending tokens submitted the prior day.
- [ ] **Ticket Triage**: Ensure zero unassigned tickets.
- [ ] **SLA Monitor**: Check for any tickets risking breach within 2 hours.
- [ ] **Customer Communication**: Verify WhatsApp/Email notification gateways tracking.

### 10.2 Weekly Checklist (Managers)
- [ ] **Broker Performance Review**: Analyze conversion ratios in weekly meeting.
- [ ] **Pending Booking Review**: Clear unapproved bookings holding up inventory.
- [ ] **Complaint Escalation Review**: Resolve manager-held tickets.
- [ ] **Payment Reconciliation**: Reconcile ERPNext ledgers against bank statements.
- [ ] **Legal Pending Review**: Check upcoming RERA deadlines.

### 10.3 Monthly Checklist (Finance / Operations)
- [ ] **Occupancy Analysis**: Generate leased vs vacant reports.
- [ ] **Rent Collection Reconciliation**: Ensure 100% invoice generation & collection follow-ups.
- [ ] **GST/Payment Audit**: Reconcile tax outputs and credit notes.
- [ ] **Commission Processing**: Disburse approved brokerage payouts.
- [ ] **SLA Performance Review**: Discuss Defect/Complaint TATs with facility agencies.

### 10.4 Quarterly Checklist (Leadership)
- [ ] **Property Inventory Audit**: Physical walk-through to prevent ghost units.
- [ ] **Vendor Contract Review**: Renew/terminate third party maintenance contracts.
- [ ] **Customer Retention Review**: Track NPS and buyer satisfaction scores.
- [ ] **Maintenance Performance Analysis**: Contractor TAT reviews via Heatmap reports.
- [ ] **Project Profitability Review**: Assess construction burn vs milestone receipts.

### 10.5 Annual Checklist (Compliance / Management)
- [ ] **Lease Renewal Audit**: Forecast expirations for next 12 months.
- [ ] **Property Valuation Review**: Update standard asking prices / base rents in system.
- [ ] **Legal Document Archive Review**: Ensure physical and digital compliance.
- [ ] **Compliance Verification**: Annual RERA audits, Fire NOC renewals.
- [ ] **Annual Maintenance Planning**: Schedule AMC closures.

---

## 11. User Roles & Who Does What

| Feature | Real Estate Admin | Sales Executive | CRM Executive | Property Manager | Leasing Manager | Accounts Executive | Legal Officer | Maintenance Supervisor |
|---|---|---|---|---|---|---|---|---|
| **Property Master** | ✅ Full | 👁 Read | 👁 Read | ✅ Full | 👁 Read | 👁 Read | 👁 Read | 👁 Read |
| **Leads & CRM** | ✅ Full | ✅ Assigned | ✅ Full | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Unit Booking** | ✅ Full | ✅ Create | 👁 Read | 👁 Read | ❌ | 👁 Read | 👁 Read | ❌ |
| **Lease & Rental** | ✅ Full | ❌ | ❌ | 👁 Read | ✅ Full | 👁 Read | ✅ Verify | ❌ |
| **Finance & Invoicing** | ✅ Full | ❌ | ❌ | ❌ | ❌ | ✅ Full | ❌ | ❌ |
| **Possession & NOC** | ✅ Full | 👁 Read | 👁 Read | 👁 Read | ❌ | ✅ Verify | ✅ Full | ❌ |
| **RERA Module** | ✅ Full | ❌ | ❌ | ❌ | ❌ | ✅ View | ✅ Full | ❌ |
| **Support Tickets** | ✅ Full | ❌ | 👁 Read | 👁 Read | ❌ | ❌ | ❌ | ✅ Full |

---

## 12. Frequently Asked Questions

**Q1: A booking was cancelled after payment. What happens to the money and unit?**  
A: Initiate a "Cancel Booking" workflow. The system will calculate deductions (if any). The Accounts team issues a Refund Payment Entry. The Unit automatically reverts to `Available` once the cancellation is approved.

---

**Q2: A customer made a payment but it is not reflecting on the dashboard. What should I do?**  
A: Check if the Payment Entry was submitted against the specific Sales Invoice. Unallocated or draft Payment Entries will not reflect in the milestone tracker.

---

**Q3: How do I renew an expiring lease?**  
A: Open the `Lease Agreement`, click **Renew Agreement**. Define the new duration and rent escalation percentage. Save the resulting new record.

---

**Q4: How do I assign a maintenance vendor for a plumbing issue?**  
A: Within the `Support Ticket` or `Defect Report`, use the "Assign Vendor" or "Contractor Assignment" child table to map a registered Supplier. They will be notified.

---

**Q5: Why does a unit still show as 'Hold' when the booking failed?**  
A: The `Unit Booking` may still be stuck in `Pending Approval` or rejected without cancellation. Have the Manager properly Reject or Cancel the booking to free the unit.

---

**Q6: Who issues the NOC and how is it tracked?**  
A: The Legal Team updates the NOC metrics in the `Possession Request` child table. Once marked `received = Yes` for all mandatory checkboxes, the system allows the next possession step.

---

**Q7: How to transfer ownership if the customer sells to a third party?**  
A: Execute a "Transfer Booking" or Name Change action in the system, provided RERA and registration allow. It creates a linked ledger to the new Customer profile.

---

**Q8: How do we process brokerage commissions?**  
A: Once a Booking milestone is met, use the `Brokerage Payout` doctype. After approval, the Finance team records a Purchase Invoice against the Broker's Supplier account.

---

**Q9: How are overdue penalties calculated on rent?**  
A: The overnight scheduler checks the due dates. If `NOW() > due date`, it automatically books a Debit Note against the tenant based on the configured % matrix in the layout.

---

**Q10: The maintenance SLA breached. Who escalates this?**  
A: It is fully automated. The system flags the ticket as `Escalated` and sends instant notifications to the Maintenance Supervisor and Support Manager.

---

**Q11: How do I upload KYC documents?**  
A: Go to the `Customer` record, use the sidebar attachment tool to upload Pan, Aadhar, etc. Alternatively, attach directly to the `Unit Booking`.

---

**Q12: How do I generate the final Sales Agreement?**  
A: In the approved `Unit Booking`, click **Create → Sales Agreement**. This pulls ERPNext Print Formats populated with buyer and property data ready for Word/PDF export.

---

**Q13: How do I export booking conversion reports for the board meeting?**  
A: From the `Sales Pipeline Dashboard` or `Script Report` view, click `Menu → Export → Excel/PDF`.

---

**Q14: A resolved ticket had the issue return. How to reopen?**  
A: If the ticket is in `Resolved` but not entirely `Closed`, a manager or buyer (via portal) can mark it `Reopen`. This returns status to `In Progress`.

---

**Q15: Can I manually update property availability?**  
A: No, to prevent inventory conflicts, availability shifts strictly through standard operations (Booking Approval, Lease Activation, Cancellation).

---

## 13. Support & Contact

| Channel | Details |
|---|---|
| 📧 Email | support@resupport.com |
| 📖 Documentation | https://docs.resupport.com |
| 🐛 IT Helpdesk | http://helpdesk.internal |
| 📱 WhatsApp | +1-XXX-XXX-XXXX (Internal Ops Support) |

---

*© 2026 RE_Support — Built for Modern Real Estate Enterprises*  
*Powered by Frappe Framework & ERPNext v15*
