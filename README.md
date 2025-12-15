# IceMail Support MCP Server

A FastMCP server providing support operations for IceMail - mailbox management, wallet credits, domain configuration, and more.

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

## Environment Variables

```bash
ICEMAIL_BASE_URL=https://app.icemail.ai/api/support  # Optional, this is the default
ICEMAIL_API_KEY=your_api_key_here                    # Required for authenticated requests
```

## Local Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally (stdio mode)
```bash
python server.py
```

### Run with HTTP transport (for testing)
```bash
fastmcp dev server.py
```

## Deploy to FastMCP Cloud

1. **Push to GitHub** (if not already done)

2. **Go to [FastMCP Cloud](https://fastmcp.cloud)**
   - Sign in with GitHub
   - Create a new project
   - Link this repository

3. **Configure deployment**
   - Entry point: `server.py:mcp`
   - Add environment variables:
     - `ICEMAIL_API_KEY` (required)
     - `ICEMAIL_BASE_URL` (optional)

4. **Deploy**
   - Your server will be available at: `https://your-project.fastmcp.app/mcp`

## Usage with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

### For FastMCP Cloud deployment:
```json
{
  "mcpServers": {
    "icemail-support": {
      "url": "https://your-project.fastmcp.app/mcp"
    }
  }
}
```

### For local development:
```json
{
  "mcpServers": {
    "icemail-support": {
      "command": "python",
      "args": ["/path/to/icemail-mcp/server.py"],
      "env": {
        "ICEMAIL_API_KEY": "your_api_key"
      }
    }
  }
}
```

## License

MIT
