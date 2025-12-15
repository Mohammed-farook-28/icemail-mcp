#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config({ quiet: true });

const BASE_URL = process.env.ICEMAIL_BASE_URL || "https://app.icemail.ai/api/support";
const API_KEY = process.env.ICEMAIL_API_KEY || "";

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
    ...(API_KEY && { Authorization: `Bearer ${API_KEY}` }),
  },
});

// Tool definitions
const tools = [
  {
    name: "get_user_workspaces",
    description: "Get all workspaces for a user",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
      },
      required: ["user"],
    },
  },
  {
    name: "add_wallet_credits",
    description: "Add credits to a user's wallet",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        amount: { type: "number", description: "Amount to add" },
        description: { type: "string", description: "Description for the transaction" },
      },
      required: ["user", "workspace_id", "amount"],
    },
  },
  {
    name: "subtract_wallet_credits",
    description: "Subtract credits from a user's wallet",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        amount: { type: "number", description: "Amount to subtract" },
        description: { type: "string", description: "Description for the transaction" },
      },
      required: ["user", "workspace_id", "amount"],
    },
  },
  {
    name: "buy_google_mailbox",
    description: "Purchase Google mailboxes for a workspace",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        next_billing_date: { type: "string", description: "Next billing date (YYYY-MM-DD)" },
        quantity: { type: "number", description: "Number of mailboxes to purchase" },
        admin_panel: { type: "boolean", description: "Whether to enable admin panel" },
        billing_cycle: { type: "string", enum: ["MONTHLY", "YEARLY"], description: "Billing cycle" },
      },
      required: ["user", "workspace_id", "next_billing_date", "quantity", "billing_cycle"],
    },
  },
  {
    name: "buy_microsoft_mailbox",
    description: "Purchase Microsoft mailboxes for a workspace",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        next_billing_date: { type: "string", description: "Next billing date (YYYY-MM-DD)" },
        quantity: { type: "number", description: "Number of mailboxes to purchase" },
        admin_panel: { type: "boolean", description: "Whether to enable admin panel" },
        billing_cycle: { type: "string", enum: ["MONTHLY", "YEARLY"], description: "Billing cycle" },
      },
      required: ["user", "workspace_id", "next_billing_date", "quantity", "billing_cycle"],
    },
  },
  {
    name: "buy_custom_mailbox",
    description: "Purchase custom mailboxes for a workspace",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        next_billing_date: { type: "string", description: "Next billing date (YYYY-MM-DD)" },
        quantity: { type: "number", description: "Number of mailboxes to purchase" },
        admin_panel: { type: "boolean", description: "Whether to enable admin panel" },
        billing_cycle: { type: "string", enum: ["MONTHLY", "YEARLY"], description: "Billing cycle" },
      },
      required: ["user", "workspace_id", "next_billing_date", "quantity", "billing_cycle"],
    },
  },
  {
    name: "delete_mailbox_purchase",
    description: "Delete mailbox purchases",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames to delete" },
      },
      required: ["user", "workspace_id", "usernames"],
    },
  },
  {
    name: "set_export_active",
    description: "Set export as active for specified usernames",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        workspace_id: { type: "string", description: "Workspace UUID" },
        export_id: { type: "string", description: "Export ID" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames" },
      },
      required: ["user", "workspace_id", "export_id", "usernames"],
    },
  },
  {
    name: "set_mailbox_active",
    description: "Set mailboxes as active",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames to activate" },
      },
      required: ["user", "usernames"],
    },
  },
  {
    name: "mailbox_reactivate",
    description: "Reactivate mailboxes with new billing settings",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        unit_price: { type: "string", description: "Unit price for the mailbox" },
        next_billing_date: { type: "string", description: "Next billing date (YYYY-MM-DD)" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames to reactivate" },
      },
      required: ["user", "unit_price", "next_billing_date", "usernames"],
    },
  },
  {
    name: "mailbox_deactivate",
    description: "Deactivate mailboxes",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames to deactivate" },
      },
      required: ["user", "usernames"],
    },
  },
  {
    name: "get_domain_map",
    description: "Get domain IDs for a list of domains",
    inputSchema: {
      type: "object",
      properties: {
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names" },
      },
      required: ["domains"],
    },
  },
  {
    name: "trigger_dkim",
    description: "Trigger DKIM setup for domains",
    inputSchema: {
      type: "object",
      properties: {
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names" },
      },
      required: ["domains"],
    },
  },
  {
    name: "google_authenticate",
    description: "Trigger Google authentication for domains",
    inputSchema: {
      type: "object",
      properties: {
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names" },
      },
      required: ["domains"],
    },
  },
  {
    name: "domain_republish",
    description: "Republish/retrigger domain setup",
    inputSchema: {
      type: "object",
      properties: {
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names" },
      },
      required: ["domains"],
    },
  },
  {
    name: "domain_dns_flags",
    description: "Update DNS flags for domains",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names" },
        spf: { type: "boolean", description: "SPF flag" },
        dmarc: { type: "boolean", description: "DMARC flag" },
        mx_records: { type: "boolean", description: "MX records flag" },
      },
      required: ["user", "domains"],
    },
  },
  {
    name: "clean_domain",
    description: "Clean domain data",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        domains: { type: "array", items: { type: "string" }, description: "Array of domain names to clean" },
      },
      required: ["user", "domains"],
    },
  },
  {
    name: "trigger_2fa",
    description: "Trigger 2FA setup for mailboxes",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames" },
      },
      required: ["user", "usernames"],
    },
  },
  {
    name: "make_profile_public",
    description: "Make mailbox profiles public",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        usernames: { type: "array", items: { type: "string" }, description: "Array of mailbox usernames" },
      },
      required: ["user", "usernames"],
    },
  },
  {
    name: "set_secret_key",
    description: "Set secret keys for mailboxes (2FA)",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        data: {
          type: "array",
          items: {
            type: "object",
            properties: {
              username: { type: "string", description: "Mailbox username" },
              secret_key: { type: "string", description: "Secret key for 2FA" },
            },
            required: ["username", "secret_key"],
          },
          description: "Array of username and secret key pairs",
        },
      },
      required: ["user", "data"],
    },
  },
  {
    name: "set_app_password",
    description: "Set app passwords for mailboxes",
    inputSchema: {
      type: "object",
      properties: {
        user: { type: "string", description: "User email address" },
        data: {
          type: "array",
          items: {
            type: "object",
            properties: {
              username: { type: "string", description: "Mailbox username" },
              app_password: { type: "string", description: "App password" },
            },
            required: ["username", "app_password"],
          },
          description: "Array of username and app password pairs",
        },
      },
      required: ["user", "data"],
    },
  },
  {
    name: "get_user_by_domain",
    description: "Get user information by domain",
    inputSchema: {
      type: "object",
      properties: {
        domain: { type: "string", description: "Domain name to look up" },
      },
      required: ["domain"],
    },
  },
  {
    name: "get_user_by_mailbox",
    description: "Get user information by mailbox",
    inputSchema: {
      type: "object",
      properties: {
        mailbox: { type: "string", description: "Mailbox email address to look up" },
      },
      required: ["mailbox"],
    },
  },
];

// Tool handlers
async function handleTool(name, args) {
  try {
    let response;

    switch (name) {
      case "get_user_workspaces":
        response = await axiosInstance.post("/get-user-workspace", { user: args.user });
        break;

      case "add_wallet_credits":
        response = await axiosInstance.post("/add-wallet-credits", {
          user: args.user,
          workspace_id: args.workspace_id,
          amount: args.amount,
          description: args.description || "",
        });
        break;

      case "subtract_wallet_credits":
        response = await axiosInstance.post("/subtract-wallet-credits", {
          user: args.user,
          workspace_id: args.workspace_id,
          amount: args.amount,
          description: args.description || "",
        });
        break;

      case "buy_google_mailbox":
        response = await axiosInstance.post("/buy-google-mailbox", {
          user: args.user,
          workspace_id: args.workspace_id,
          next_billing_date: args.next_billing_date,
          quantity: args.quantity,
          admin_panel: args.admin_panel ?? false,
          billing_cycle: args.billing_cycle,
        });
        break;

      case "buy_microsoft_mailbox":
        response = await axiosInstance.post("/buy-microsoft-mailbox", {
          user: args.user,
          workspace_id: args.workspace_id,
          next_billing_date: args.next_billing_date,
          quantity: args.quantity,
          admin_panel: args.admin_panel ?? false,
          billing_cycle: args.billing_cycle,
        });
        break;

      case "buy_custom_mailbox":
        response = await axiosInstance.post("/buy-custom-mailbox", {
          user: args.user,
          workspace_id: args.workspace_id,
          next_billing_date: args.next_billing_date,
          quantity: args.quantity,
          admin_panel: args.admin_panel ?? false,
          billing_cycle: args.billing_cycle,
        });
        break;

      case "delete_mailbox_purchase":
        response = await axiosInstance.post("/delete-mailbox-purchase", {
          user: args.user,
          workspace_id: args.workspace_id,
          usernames: args.usernames,
        });
        break;

      case "set_export_active":
        response = await axiosInstance.put("/set-export-active", {
          user: args.user,
          workspace_id: args.workspace_id,
          export_id: args.export_id,
          usernames: args.usernames,
        });
        break;

      case "set_mailbox_active":
        response = await axiosInstance.put("/set-mailbox-active", {
          user: args.user,
          usernames: args.usernames,
        });
        break;

      case "mailbox_reactivate":
        response = await axiosInstance.put("/mailbox-reactivate", {
          user: args.user,
          unit_price: args.unit_price,
          next_billing_date: args.next_billing_date,
          usernames: args.usernames,
        });
        break;

      case "mailbox_deactivate":
        response = await axiosInstance.put("/mailbox-deactivate", {
          user: args.user,
          usernames: args.usernames,
        });
        break;

      case "get_domain_map":
        response = await axiosInstance.post("/get-domain-map", {
          domains: args.domains,
        });
        break;

      case "trigger_dkim":
        response = await axiosInstance.post("/trigger-dkim", {
          domains: args.domains,
        });
        break;

      case "google_authenticate":
        response = await axiosInstance.post("/google-authenticate", {
          domains: args.domains,
        });
        break;

      case "domain_republish":
        response = await axiosInstance.post("/domain-republish", {
          domains: args.domains,
        });
        break;

      case "domain_dns_flags":
        response = await axiosInstance.put("/domain-dns-flags", {
          user: args.user,
          domains: args.domains,
          spf: args.spf,
          dmarc: args.dmarc,
          mx_records: args.mx_records,
        });
        break;

      case "clean_domain":
        response = await axiosInstance.post("/clean-domain", {
          user: args.user,
          domains: args.domains,
        });
        break;

      case "trigger_2fa":
        response = await axiosInstance.post("/trigger-2fa", {
          user: args.user,
          usernames: args.usernames,
        });
        break;

      case "make_profile_public":
        response = await axiosInstance.post("/make-profile-public", {
          user: args.user,
          usernames: args.usernames,
        });
        break;

      case "set_secret_key":
        response = await axiosInstance.put("/set-secret-key", {
          user: args.user,
          data: args.data,
        });
        break;

      case "set_app_password":
        response = await axiosInstance.put("/set-app-password", {
          user: args.user,
          data: args.data,
        });
        break;

      case "get_user_by_domain":
        response = await axiosInstance.get("/user", {
          params: { domain: args.domain },
        });
        break;

      case "get_user_by_mailbox":
        response = await axiosInstance.get("/user", {
          params: { mailbox: args.mailbox },
        });
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(response.data, null, 2),
        },
      ],
    };
  } catch (error) {
    const errorMessage = error.response?.data?.message || error.response?.data || error.message;
    return {
      content: [
        {
          type: "text",
          text: `Error: ${JSON.stringify(errorMessage, null, 2)}`,
        },
      ],
      isError: true,
    };
  }
}

// Create server
const server = new Server(
  {
    name: "icemail-support-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  return handleTool(name, args);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
