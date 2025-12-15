#!/usr/bin/env python3
"""
IceMail Support MCP Server
A FastMCP server for IceMail support operations.
"""

import os
import httpx
from fastmcp import FastMCP
from typing import Optional
from pydantic import Field

# Configuration
BASE_URL = os.getenv("ICEMAIL_BASE_URL", "https://app.icemail.ai/api/support")
API_KEY = os.getenv("ICEMAIL_API_KEY", "")

# Initialize FastMCP server
mcp = FastMCP(
    "icemail-support-mcp",
    description="MCP server for IceMail support operations"
)

# HTTP client setup
def get_client() -> httpx.Client:
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return httpx.Client(base_url=BASE_URL, headers=headers, timeout=30.0)


# ============== User & Workspace Tools ==============

@mcp.tool()
def get_user_workspaces(user: str = Field(description="User email address")) -> str:
    """Get all workspaces for a user"""
    with get_client() as client:
        response = client.post("/get-user-workspace", json={"user": user})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def get_user_by_domain(domain: str = Field(description="Domain name to look up")) -> str:
    """Get user information by domain"""
    with get_client() as client:
        response = client.get("/user", params={"domain": domain})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def get_user_by_mailbox(mailbox: str = Field(description="Mailbox email address to look up")) -> str:
    """Get user information by mailbox"""
    with get_client() as client:
        response = client.get("/user", params={"mailbox": mailbox})
        response.raise_for_status()
        return response.json()


# ============== Wallet Tools ==============

@mcp.tool()
def add_wallet_credits(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    amount: float = Field(description="Amount to add"),
    description: Optional[str] = Field(default="", description="Description for the transaction")
) -> str:
    """Add credits to a user's wallet"""
    with get_client() as client:
        response = client.post("/add-wallet-credits", json={
            "user": user,
            "workspace_id": workspace_id,
            "amount": amount,
            "description": description or ""
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def subtract_wallet_credits(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    amount: float = Field(description="Amount to subtract"),
    description: Optional[str] = Field(default="", description="Description for the transaction")
) -> str:
    """Subtract credits from a user's wallet"""
    with get_client() as client:
        response = client.post("/subtract-wallet-credits", json={
            "user": user,
            "workspace_id": workspace_id,
            "amount": amount,
            "description": description or ""
        })
        response.raise_for_status()
        return response.json()


# ============== Mailbox Purchase Tools ==============

@mcp.tool()
def buy_google_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase Google mailboxes for a workspace"""
    with get_client() as client:
        response = client.post("/buy-google-mailbox", json={
            "user": user,
            "workspace_id": workspace_id,
            "next_billing_date": next_billing_date,
            "quantity": quantity,
            "admin_panel": admin_panel,
            "billing_cycle": billing_cycle
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def buy_microsoft_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase Microsoft mailboxes for a workspace"""
    with get_client() as client:
        response = client.post("/buy-microsoft-mailbox", json={
            "user": user,
            "workspace_id": workspace_id,
            "next_billing_date": next_billing_date,
            "quantity": quantity,
            "admin_panel": admin_panel,
            "billing_cycle": billing_cycle
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def buy_custom_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase custom mailboxes for a workspace"""
    with get_client() as client:
        response = client.post("/buy-custom-mailbox", json={
            "user": user,
            "workspace_id": workspace_id,
            "next_billing_date": next_billing_date,
            "quantity": quantity,
            "admin_panel": admin_panel,
            "billing_cycle": billing_cycle
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def delete_mailbox_purchase(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    usernames: list[str] = Field(description="Array of mailbox usernames to delete")
) -> str:
    """Delete mailbox purchases"""
    with get_client() as client:
        response = client.post("/delete-mailbox-purchase", json={
            "user": user,
            "workspace_id": workspace_id,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


# ============== Mailbox Status Tools ==============

@mcp.tool()
def set_export_active(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    export_id: str = Field(description="Export ID"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Set export as active for specified usernames"""
    with get_client() as client:
        response = client.put("/set-export-active", json={
            "user": user,
            "workspace_id": workspace_id,
            "export_id": export_id,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def set_mailbox_active(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames to activate")
) -> str:
    """Set mailboxes as active"""
    with get_client() as client:
        response = client.put("/set-mailbox-active", json={
            "user": user,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mailbox_reactivate(
    user: str = Field(description="User email address"),
    unit_price: str = Field(description="Unit price for the mailbox"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    usernames: list[str] = Field(description="Array of mailbox usernames to reactivate")
) -> str:
    """Reactivate mailboxes with new billing settings"""
    with get_client() as client:
        response = client.put("/mailbox-reactivate", json={
            "user": user,
            "unit_price": unit_price,
            "next_billing_date": next_billing_date,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mailbox_deactivate(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames to deactivate")
) -> str:
    """Deactivate mailboxes"""
    with get_client() as client:
        response = client.put("/mailbox-deactivate", json={
            "user": user,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


# ============== Domain Tools ==============

@mcp.tool()
def get_domain_map(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Get domain IDs for a list of domains"""
    with get_client() as client:
        response = client.post("/get-domain-map", json={"domains": domains})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def trigger_dkim(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Trigger DKIM setup for domains"""
    with get_client() as client:
        response = client.post("/trigger-dkim", json={"domains": domains})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def google_authenticate(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Trigger Google authentication for domains"""
    with get_client() as client:
        response = client.post("/google-authenticate", json={"domains": domains})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def domain_republish(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Republish/retrigger domain setup"""
    with get_client() as client:
        response = client.post("/domain-republish", json={"domains": domains})
        response.raise_for_status()
        return response.json()


@mcp.tool()
def domain_dns_flags(
    user: str = Field(description="User email address"),
    domains: list[str] = Field(description="Array of domain names"),
    spf: Optional[bool] = Field(default=None, description="SPF flag"),
    dmarc: Optional[bool] = Field(default=None, description="DMARC flag"),
    mx_records: Optional[bool] = Field(default=None, description="MX records flag")
) -> str:
    """Update DNS flags for domains"""
    payload = {"user": user, "domains": domains}
    if spf is not None:
        payload["spf"] = spf
    if dmarc is not None:
        payload["dmarc"] = dmarc
    if mx_records is not None:
        payload["mx_records"] = mx_records
    
    with get_client() as client:
        response = client.put("/domain-dns-flags", json=payload)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def clean_domain(
    user: str = Field(description="User email address"),
    domains: list[str] = Field(description="Array of domain names to clean")
) -> str:
    """Clean domain data"""
    with get_client() as client:
        response = client.post("/clean-domain", json={
            "user": user,
            "domains": domains
        })
        response.raise_for_status()
        return response.json()


# ============== Security & Authentication Tools ==============

@mcp.tool()
def trigger_2fa(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Trigger 2FA setup for mailboxes"""
    with get_client() as client:
        response = client.post("/trigger-2fa", json={
            "user": user,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def make_profile_public(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Make mailbox profiles public"""
    with get_client() as client:
        response = client.post("/make-profile-public", json={
            "user": user,
            "usernames": usernames
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def set_secret_key(
    user: str = Field(description="User email address"),
    data: list[dict] = Field(description="Array of {username, secret_key} pairs for 2FA")
) -> str:
    """Set secret keys for mailboxes (2FA)"""
    with get_client() as client:
        response = client.put("/set-secret-key", json={
            "user": user,
            "data": data
        })
        response.raise_for_status()
        return response.json()


@mcp.tool()
def set_app_password(
    user: str = Field(description="User email address"),
    data: list[dict] = Field(description="Array of {username, app_password} pairs")
) -> str:
    """Set app passwords for mailboxes"""
    with get_client() as client:
        response = client.put("/set-app-password", json={
            "user": user,
            "data": data
        })
        response.raise_for_status()
        return response.json()


# Entry point for running the server
if __name__ == "__main__":
    mcp.run()
