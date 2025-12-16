# IceMail Support MCP Server

A FastMCP server providing support operations for IceMail - mailbox management, wallet credits, domain configuration, and more.

**Hosted on:** FastMCP Cloud  
**URL:** `https://diplomatic-lavender-pike.fastmcp.app/mcp/`

---

## 🚀 Quick Start for Users

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions.

---

## Tools Available (23 total)

### User & Workspace
- `get_user_workspaces` - Get all workspaces for a user
- `get_user_by_domain` - Get user information by domain
- `get_user_by_mailbox` - Get user information by mailbox

### Wallet
- `add_wallet_credits` - Add credits to a user's wallet
- `subtract_wallet_credits` - Subtract credits from a user's wallet

### Mailbox Purchases
- `buy_google_mailbox` - Purchase Google mailboxes
- `buy_microsoft_mailbox` - Purchase Microsoft mailboxes
- `buy_custom_mailbox` - Purchase custom mailboxes
- `delete_mailbox_purchase` - Delete mailbox purchases

### Mailbox Status
- `set_export_active` - Set export as active for usernames
- `set_mailbox_active` - Set mailboxes as active
- `mailbox_reactivate` - Reactivate mailboxes with new billing
- `mailbox_deactivate` - Deactivate mailboxes

### Domain Management
- `get_domain_map` - Get domain IDs for domains
- `trigger_dkim` - Trigger DKIM setup
- `google_authenticate` - Trigger Google authentication
- `domain_republish` - Republish/retrigger domain setup
- `domain_dns_flags` - Update DNS flags (SPF, DMARC, MX)
- `clean_domain` - Clean domain data

### Security & Authentication
- `trigger_2fa` - Trigger 2FA setup for mailboxes
- `make_profile_public` - Make mailbox profiles public
- `set_secret_key` - Set 2FA secret keys
- `set_app_password` - Set app passwords

---

## For Developers

### Local Development

```bash
# Clone the repo
git clone https://github.com/Mohammed-farook-28/icemail-mcp.git
cd icemail-mcp

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python server.py
```

### Environment Variables

```bash
ICEMAIL_BASE_URL=https://app.icemail.ai/api/support  # Optional (default)
ICEMAIL_API_KEY=your_api_key                         # For authenticated requests
LOG_LEVEL=INFO                                       # DEBUG, INFO, WARNING, ERROR
REQUEST_TIMEOUT=30                                   # Seconds
MAX_RETRIES=3                                        # Retry count
```

### Test with FastMCP Inspector

```bash
source venv/bin/activate
fastmcp dev server.py
```

---

## Deployment

This server is deployed on **FastMCP Cloud**.

To redeploy:
1. Push changes to GitHub
2. FastMCP Cloud auto-deploys from main branch

---

## License

MIT
