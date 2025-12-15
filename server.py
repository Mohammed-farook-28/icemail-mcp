#!/usr/bin/env python3
"""
IceMail Support MCP Server (Production Ready)
A FastMCP server for IceMail support operations.
"""

import os
import json
import logging
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastmcp import FastMCP
from pydantic import Field

# ============== Configuration ==============

BASE_URL = os.getenv("ICEMAIL_BASE_URL", "https://app.icemail.ai/api/support")
API_KEY = os.getenv("ICEMAIL_API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# ============== Logging Setup ==============

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("icemail-mcp")

# ============== HTTP Client ==============

# Global async client for connection pooling
_client: Optional[httpx.AsyncClient] = None


async def get_client() -> httpx.AsyncClient:
    """Get or create the async HTTP client with connection pooling."""
    global _client
    if _client is None or _client.is_closed:
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        # Production settings: connection pooling, retries, timeouts
        transport = httpx.AsyncHTTPTransport(
            retries=MAX_RETRIES,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            )
        )
        _client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=headers,
            timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=10.0),
            transport=transport
        )
    return _client


async def close_client():
    """Close the HTTP client gracefully."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


# ============== Lifecycle Management ==============

@asynccontextmanager
async def lifespan(app):
    """Manage server lifecycle - startup and shutdown."""
    logger.info(f"Starting IceMail MCP Server")
    logger.info(f"API Base URL: {BASE_URL}")
    logger.info(f"API Key configured: {'Yes' if API_KEY else 'No'}")
    yield
    logger.info("Shutting down IceMail MCP Server")
    await close_client()


# ============== Initialize FastMCP ==============

mcp = FastMCP("icemail-support-mcp", lifespan=lifespan)


# ============== Helper Functions ==============

async def api_request(method: str, endpoint: str, **kwargs) -> str:
    """
    Make an API request with proper error handling.
    
    Args:
        method: HTTP method (get, post, put, delete)
        endpoint: API endpoint path
        **kwargs: Additional arguments for the request
    
    Returns:
        JSON string response
    
    Raises:
        Exception with detailed error message on failure
    """
    client = await get_client()
    
    try:
        logger.debug(f"API Request: {method.upper()} {endpoint}")
        
        response = await getattr(client, method)(endpoint, **kwargs)
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"API Response: {response.status_code}")
        return json.dumps(result, indent=2)
        
    except httpx.HTTPStatusError as e:
        error_body = e.response.text
        try:
            error_json = e.response.json()
            error_msg = error_json.get("message", error_json.get("error", error_body))
        except Exception:
            error_msg = error_body
        
        logger.error(f"API Error {e.response.status_code}: {error_msg}")
        raise Exception(f"API Error ({e.response.status_code}): {error_msg}")
        
    except httpx.ConnectError as e:
        logger.error(f"Connection error: {e}")
        raise Exception(f"Failed to connect to IceMail API: {e}")
        
    except httpx.TimeoutException as e:
        logger.error(f"Request timeout: {e}")
        raise Exception(f"Request timed out after {REQUEST_TIMEOUT}s")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise Exception(f"Unexpected error: {e}")


# ============== User & Workspace Tools ==============

@mcp.tool()
async def get_user_workspaces(user: str = Field(description="User email address")) -> str:
    """Get all workspaces for a user"""
    return await api_request("post", "/get-user-workspace", json={"user": user})


@mcp.tool()
async def get_user_by_domain(domain: str = Field(description="Domain name to look up")) -> str:
    """Get user information by domain"""
    return await api_request("get", "/user", params={"domain": domain})


@mcp.tool()
async def get_user_by_mailbox(mailbox: str = Field(description="Mailbox email address to look up")) -> str:
    """Get user information by mailbox"""
    return await api_request("get", "/user", params={"mailbox": mailbox})


# ============== Wallet Tools ==============

@mcp.tool()
async def add_wallet_credits(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    amount: float = Field(description="Amount to add"),
    description: Optional[str] = Field(default="", description="Description for the transaction")
) -> str:
    """Add credits to a user's wallet"""
    return await api_request("post", "/add-wallet-credits", json={
        "user": user,
        "workspace_id": workspace_id,
        "amount": amount,
        "description": description or ""
    })


@mcp.tool()
async def subtract_wallet_credits(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    amount: float = Field(description="Amount to subtract"),
    description: Optional[str] = Field(default="", description="Description for the transaction")
) -> str:
    """Subtract credits from a user's wallet"""
    return await api_request("post", "/subtract-wallet-credits", json={
        "user": user,
        "workspace_id": workspace_id,
        "amount": amount,
        "description": description or ""
    })


# ============== Mailbox Purchase Tools ==============

@mcp.tool()
async def buy_google_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase Google mailboxes for a workspace"""
    return await api_request("post", "/buy-google-mailbox", json={
        "user": user,
        "workspace_id": workspace_id,
        "next_billing_date": next_billing_date,
        "quantity": quantity,
        "admin_panel": admin_panel,
        "billing_cycle": billing_cycle
    })


@mcp.tool()
async def buy_microsoft_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase Microsoft mailboxes for a workspace"""
    return await api_request("post", "/buy-microsoft-mailbox", json={
        "user": user,
        "workspace_id": workspace_id,
        "next_billing_date": next_billing_date,
        "quantity": quantity,
        "admin_panel": admin_panel,
        "billing_cycle": billing_cycle
    })


@mcp.tool()
async def buy_custom_mailbox(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    quantity: int = Field(description="Number of mailboxes to purchase"),
    billing_cycle: str = Field(description="Billing cycle: MONTHLY or YEARLY"),
    admin_panel: bool = Field(default=False, description="Whether to enable admin panel")
) -> str:
    """Purchase custom mailboxes for a workspace"""
    return await api_request("post", "/buy-custom-mailbox", json={
        "user": user,
        "workspace_id": workspace_id,
        "next_billing_date": next_billing_date,
        "quantity": quantity,
        "admin_panel": admin_panel,
        "billing_cycle": billing_cycle
    })


@mcp.tool()
async def delete_mailbox_purchase(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    usernames: list[str] = Field(description="Array of mailbox usernames to delete")
) -> str:
    """Delete mailbox purchases"""
    return await api_request("post", "/delete-mailbox-purchase", json={
        "user": user,
        "workspace_id": workspace_id,
        "usernames": usernames
    })


# ============== Mailbox Status Tools ==============

@mcp.tool()
async def set_export_active(
    user: str = Field(description="User email address"),
    workspace_id: str = Field(description="Workspace UUID"),
    export_id: str = Field(description="Export ID"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Set export as active for specified usernames"""
    return await api_request("put", "/set-export-active", json={
        "user": user,
        "workspace_id": workspace_id,
        "export_id": export_id,
        "usernames": usernames
    })


@mcp.tool()
async def set_mailbox_active(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames to activate")
) -> str:
    """Set mailboxes as active"""
    return await api_request("put", "/set-mailbox-active", json={
        "user": user,
        "usernames": usernames
    })


@mcp.tool()
async def mailbox_reactivate(
    user: str = Field(description="User email address"),
    unit_price: str = Field(description="Unit price for the mailbox"),
    next_billing_date: str = Field(description="Next billing date (YYYY-MM-DD)"),
    usernames: list[str] = Field(description="Array of mailbox usernames to reactivate")
) -> str:
    """Reactivate mailboxes with new billing settings"""
    return await api_request("put", "/mailbox-reactivate", json={
        "user": user,
        "unit_price": unit_price,
        "next_billing_date": next_billing_date,
        "usernames": usernames
    })


@mcp.tool()
async def mailbox_deactivate(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames to deactivate")
) -> str:
    """Deactivate mailboxes"""
    return await api_request("put", "/mailbox-deactivate", json={
        "user": user,
        "usernames": usernames
    })


# ============== Domain Tools ==============

@mcp.tool()
async def get_domain_map(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Get domain IDs for a list of domains"""
    return await api_request("post", "/get-domain-map", json={"domains": domains})


@mcp.tool()
async def trigger_dkim(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Trigger DKIM setup for domains"""
    return await api_request("post", "/trigger-dkim", json={"domains": domains})


@mcp.tool()
async def google_authenticate(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Trigger Google authentication for domains"""
    return await api_request("post", "/google-authenticate", json={"domains": domains})


@mcp.tool()
async def domain_republish(
    domains: list[str] = Field(description="Array of domain names")
) -> str:
    """Republish/retrigger domain setup"""
    return await api_request("post", "/domain-republish", json={"domains": domains})


@mcp.tool()
async def domain_dns_flags(
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
    
    return await api_request("put", "/domain-dns-flags", json=payload)


@mcp.tool()
async def clean_domain(
    user: str = Field(description="User email address"),
    domains: list[str] = Field(description="Array of domain names to clean")
) -> str:
    """Clean domain data"""
    return await api_request("post", "/clean-domain", json={
        "user": user,
        "domains": domains
    })


# ============== Security & Authentication Tools ==============

@mcp.tool()
async def trigger_2fa(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Trigger 2FA setup for mailboxes"""
    return await api_request("post", "/trigger-2fa", json={
        "user": user,
        "usernames": usernames
    })


@mcp.tool()
async def make_profile_public(
    user: str = Field(description="User email address"),
    usernames: list[str] = Field(description="Array of mailbox usernames")
) -> str:
    """Make mailbox profiles public"""
    return await api_request("post", "/make-profile-public", json={
        "user": user,
        "usernames": usernames
    })


@mcp.tool()
async def set_secret_key(
    user: str = Field(description="User email address"),
    data: list[dict] = Field(description="Array of {username, secret_key} pairs for 2FA")
) -> str:
    """Set secret keys for mailboxes (2FA)"""
    return await api_request("put", "/set-secret-key", json={
        "user": user,
        "data": data
    })


@mcp.tool()
async def set_app_password(
    user: str = Field(description="User email address"),
    data: list[dict] = Field(description="Array of {username, app_password} pairs")
) -> str:
    """Set app passwords for mailboxes"""
    return await api_request("put", "/set-app-password", json={
        "user": user,
        "data": data
    })


# ============== Entry Point ==============

if __name__ == "__main__":
    mcp.run()
