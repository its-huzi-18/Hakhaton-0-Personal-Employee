---
type: email
action: send
status: pending_approval
recipients: ["john.client@example.com"]
subject: Invoice for January Services - $1,500
created: 2026-02-21T16:25:00Z
expires: 2026-02-22T16:25:00Z
priority: high
source_task: EMAIL_test_client_invoice.md
related_plan: PLAN_EMAIL_test_client_invoice.md
---

# Email Approval Request

## What Will Happen
Send invoice email to John Client (john.client@example.com) regarding January consulting services.

## Email Details

**To:** john.client@example.com
**From:** you@yourcompany.com
**Subject:** Invoice for January Services - $1,500

## Email Body

```
Dear John,

Thank you for your email. I hope you're doing well!

Please find attached the invoice for consulting services provided in January 2026.

Invoice Details:
- Amount: $1,500.00
- Service: Consulting Services - January 2026
- Due Date: March 7, 2026 (14 days from today)

Payment Methods:
- Bank Transfer: [Account details would be here]
- Check: Payable to Your Company Name
- Online Payment: [Payment link would be here]

If you have any questions about this invoice or need any additional information, please don't hesitate to reach out.

Thank you for your business!

Best regards,
Your AI Employee
On behalf of Your Company

---
Note: This email was prepared by AI Employee with human approval.
```

## Company Handbook Compliance

### Section 1: Autonomy Thresholds
- ⏳ **Requires Approval** - "Sending emails or messages"

### Section 2: Communication Guidelines
- ✅ Known contact (John Client)
- ✅ Professional tone
- ✅ Clear and concise
- ✅ AI assistance note included

### Section 3: Financial Rules
- ✅ Not a payment (this is invoicing)
- ✅ Positive financial impact (requesting payment)

### Section 9: Security Boundaries
- ✅ No credentials exposed
- ✅ No sensitive information shared

## Risk Assessment

| Factor | Level | Notes |
|--------|-------|-------|
| Financial Risk | None | Requesting payment, not sending |
| Relationship Risk | Low | Professional communication |
| Security Risk | None | No sensitive data shared |
| Compliance Risk | None | Follows all guidelines |

## To Approve
**Move this file to `/Approved/` folder**

This will trigger the email orchestrator to send the email.

## To Reject
**Move this file to `/Rejected/` folder**

This will cancel the email sending and log the rejection.

## Additional Notes

- Original email from client is in: `Needs_Action/EMAIL_test_client_invoice.md`
- Full action plan is in: `Plans/PLAN_EMAIL_test_client_invoice.md`
- This approval expires in 24 hours (per Company Handbook)

---
*Approval Request created following Company Handbook v1.0*
*AI Employee Version: 0.1 (Bronze Tier)*
