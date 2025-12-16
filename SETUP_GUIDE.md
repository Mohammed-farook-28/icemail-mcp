# 🚀 IceMail MCP Setup Guide

Follow these simple steps to add IceMail support tools to Claude.

---

## Step 1: Install Required Software

### Install Claude Desktop
Download from: **https://claude.ai/download**

### Install Node.js
Download from: **https://nodejs.org** (choose "LTS" version)

---

## Step 2: Create Config File

### On Mac

1. Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter)

2. Copy and paste this entire command, then press Enter:

```bash
mkdir -p ~/Library/Application\ Support/Claude && cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "icemail-support": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://diplomatic-lavender-pike.fastmcp.app/mcp/"
      ],
      "env": {
        "MCP_HEADERS": "Authorization: Bearer fmcp_9mFZ3V3NckbZHaRvNV3Rlfr3yALkpt-uhl0oho9XtA0"
      }
    }
  }
}
EOF
```

3. Press Enter. You should see no errors.

---

### On Windows

1. Press `Win + R`, type `cmd`, press Enter

2. Run this command to create the folder:
```cmd
mkdir "%APPDATA%\Claude"
```

3. Run this command to open Notepad:
```cmd
notepad "%APPDATA%\Claude\claude_desktop_config.json"
```

4. Click "Yes" to create a new file

5. Paste this content:
```json
{
  "mcpServers": {
    "icemail-support": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://diplomatic-lavender-pike.fastmcp.app/mcp/"
      ],
      "env": {
        "MCP_HEADERS": "Authorization: Bearer fmcp_9mFZ3V3NckbZHaRvNV3Rlfr3yALkpt-uhl0oho9XtA0"
      }
    }
  }
}
```

6. Save the file (`Ctrl + S`) and close Notepad

---

## Step 3: Restart Claude Desktop

1. **Quit Claude completely**
   - Mac: Press `Cmd + Q`
   - Windows: Right-click Claude in taskbar → Close

2. **Reopen Claude Desktop**

3. **Wait 10-15 seconds** for the MCP server to connect

---

## Step 4: Verify It Works

1. Open Claude Desktop Settings (gear icon)
2. Go to **Developer** section
3. You should see **"icemail-support"** listed

---

## Step 5: Start Using! ✅

Ask Claude things like:

- "Get workspaces for user@example.com"
- "What IceMail tools are available?"
- "Add 100 credits to user's wallet"
- "Trigger DKIM for domain.com"

---

## Available Tools (23 total)

| Category | Tools |
|----------|-------|
| **User** | get_user_workspaces, get_user_by_domain, get_user_by_mailbox |
| **Wallet** | add_wallet_credits, subtract_wallet_credits |
| **Mailbox** | buy_google_mailbox, buy_microsoft_mailbox, buy_custom_mailbox, delete_mailbox_purchase |
| **Status** | set_export_active, set_mailbox_active, mailbox_reactivate, mailbox_deactivate |
| **Domain** | get_domain_map, trigger_dkim, google_authenticate, domain_republish, domain_dns_flags, clean_domain |
| **Security** | trigger_2fa, make_profile_public, set_secret_key, set_app_password |

---

## Troubleshooting

### "Server disconnected" error
- Make sure Node.js is installed: run `node --version` in Terminal
- Restart Claude Desktop completely (Cmd+Q or Ctrl+Q)

### Tools not showing
- Wait 15-30 seconds after opening Claude
- Check Settings → Developer → icemail-support status

### Need help?
Contact your administrator.

---

**Setup complete!** 🎉

