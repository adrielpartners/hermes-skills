---
name: zoho-mail
description: "Use when managing Zoho Mail — compose, send, and save draft emails. Create drafts, list drafts, send emails, manage folders, and automate email workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zoho, email, productivity, drafts, communication]
    related_skills: [himalaya, google-workspace, gmail]
---

# Zoho Mail Integration

Comprehensive skill for interacting with Zoho Mail from Hermes Agent. Supports email composition, draft management, sending, and folder operations.

## Overview

Zoho Mail is a secure email hosting platform. This skill provides Hermes Agent with full control over email workflows:

- **Drafts** — create, list, update, delete, send drafts
- **Emails** — send emails, list messages, search
- **Folders** — manage custom folders
- **Auto-save** — automatically save compositions as drafts before sending

This skill is ideal for **automating email workflows**, **batch sending**, and **draft collaboration**.

## When to Use

- You're composing responses and want to save them as drafts for review
- You're automating email workflows (newsletters, notifications, bulk sends)
- You need to list and manage draft emails programmatically
- You're integrating Zoho Mail with external systems
- You want to defer sending until a draft is reviewed by a team member

**Don't use for:**
- Manual one-off emails (use the Zoho Mail UI)
- Real-time email monitoring (use Zoho Mail webhooks instead)
- Complex mail filtering (use Zoho Mail rules)

## Setup

### Configure Multiple Accounts

1. **Edit `config.yaml`** in the skill directory:
   ```bash
   nano ~/.hermes/skills/productivity/zoho-mail/config.yaml
   ```

2. **Add your accounts:**
   ```yaml
   accounts:
     adriel:
       email: phillip@adrielpartners.com
       account_id: ${ZOHO_ACCOUNT_ID_ADRIEL}
       description: "ADRIEL PARTNERS"
       default: true
     
     sitehub:
       email: team@sitehubservices.com
       account_id: ${ZOHO_ACCOUNT_ID_SITEHUB}
       description: "Site Hub Services"
       default: false
   
   oauth:
     client_id: ${ZOHO_CLIENT_ID}
     client_secret: ${ZOHO_CLIENT_SECRET}
     redirect_url: http://localhost:8080/callback
   ```

### Get Zoho OAuth Credentials

1. Go to [Zoho API Console](https://api-console.zoho.com)
2. Create a new OAuth client (Self Client or Server-based Application)
3. Copy:
   - **Client ID**
   - **Client Secret**
   - **Redirect URL** (if needed; default: `http://localhost:8080/callback`)

4. Store in `~/.hermes/.env`:
   ```bash
   ZOHO_CLIENT_ID=your_client_id
   ZOHO_CLIENT_SECRET=your_client_secret
   ZOHO_ACCOUNT_ID_ADRIEL=your_adriel_account_id
   ZOHO_ACCOUNT_ID_SITEHUB=your_sitehub_account_id
   ZOHO_REDIRECT_URL=http://localhost:8080/callback
   ```

### Get Account IDs

For each Zoho Mail account, find the Account ID:

1. Log into [Zoho Mail](https://mail.zoho.com)
2. Settings → Account Settings → look for "Account ID"
3. Or via API:
   ```bash
   curl -X GET https://mail.zoho.com/api/accounts \
     -H "Authorization: Zoho-oauthtoken YOUR_TOKEN"
   ```

### Required Credentials

| Variable | Description |
|----------|-------------|
| `ZOHO_CLIENT_ID` | OAuth Client ID (shared) |
| `ZOHO_CLIENT_SECRET` | OAuth Client Secret (shared) |
| `ZOHO_ACCOUNT_ID_ADRIEL` | Account ID for phillip@adrielpartners.com |
| `ZOHO_ACCOUNT_ID_SITEHUB` | Account ID for team@sitehubservices.com |

## Operations

### Authentication

The skill uses OAuth 2.0. First run will prompt for authorization:

```bash
hermes -s zoho-mail chat -q "List my draft emails"
# Follow the browser prompt to authorize
```

### Drafts

#### Create a Draft

```bash
# Simple draft
hermes chat -q "Create a draft email to john@example.com with subject 'Meeting Notes' and body 'Please review the attached notes'"

# The skill will:
# 1. Compose the email
# 2. Save it as a draft in Zoho Mail
# 3. Return the draft ID for future reference
```

#### List Drafts

```bash
hermes chat -q "List all my draft emails"

# Returns:
# - Draft ID
# - To address
# - Subject
# - Created date
# - Last modified date
```

#### Get Draft Details

```bash
hermes chat -q "Show me draft ID: draft_123"
```

#### Update a Draft

```bash
hermes chat -q "Update draft draft_123 to change subject to 'New Subject'"
```

#### Send a Draft

```bash
hermes chat -q "Send draft draft_123"

# Draft will be sent and moved to "Sent" folder
```

#### Delete a Draft

```bash
hermes chat -q "Delete draft draft_123"
```

### Email Operations

#### Send an Email Directly

```bash
hermes chat -q "Send email to alice@example.com with subject 'Hello' and body 'Testing'"

# This sends immediately (not as draft)
```

#### List Emails

```bash
hermes chat -q "List my recent emails"

# Returns:
# - Email ID
# - From address
# - Subject
# - Date
# - Snippet
```

#### Search Emails

```bash
hermes chat -q "Search for emails from john@example.com about budget"
```

## API Reference

### Zoho Mail API Endpoints

Base URL: `https://mail.zoho.com/api/accounts/{accountId}`

#### Drafts

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/drafts` | Create a new draft |
| GET | `/drafts` | List all drafts |
| GET | `/drafts/{draftId}` | Get draft details |
| PUT | `/drafts/{draftId}` | Update a draft |
| DELETE | `/drafts/{draftId}` | Delete a draft |
| POST | `/drafts/{draftId}/send` | Send a draft |

#### Messages

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/messages/send` | Send email directly |
| GET | `/messages` | List messages |
| GET | `/messages/{messageId}` | Get message details |
| DELETE | `/messages/{messageId}` | Delete message |

#### Folders

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/folders` | List all folders |
| POST | `/folders` | Create folder |
| DELETE | `/folders/{folderId}` | Delete folder |

## Pitfalls & Solutions

1. **"Unauthorized" on first use**
   - Run the authorization flow once: `hermes -s zoho-mail chat -q "Verify my email"`
   - Check that OAuth token is cached in `~/.hermes/auth.json`

2. **"Account ID not found"**
   - Verify `ZOHO_ACCOUNT_ID` is set correctly in `.env`
   - Make sure it matches your actual Zoho Mail account ID (not email)

3. **Draft not saving**
   - Check that `To:` address is valid
   - Subject and body must be non-empty
   - Verify API token hasn't expired (re-authorize if needed)

4. **Send draft fails**
   - Draft must have at least: To, Subject, Body
   - Some drafts may be locked if they're being edited elsewhere

5. **Rate limiting (429 Too Many Requests)**
   - Zoho Mail API has request limits
   - Add delays between operations (0.5s)
   - Batch operations where possible

6. **OAuth token expired**
   - Tokens expire after 1 hour of inactivity
   - Run any command again to re-authenticate
   - Token refresh happens automatically

## Examples

### Example 1: List Accounts

```bash
hermes chat -q "List my Zoho Mail accounts"

# Output:
# === Zoho Mail Accounts ===
#
# adriel (default)
#   Email: phillip@adrielpartners.com
#   ADRIEL PARTNERS
#
# sitehub
#   Email: team@sitehubservices.com
#   Site Hub Services
```

### Example 2: Create Draft (Default Account)

```bash
hermes chat -q "
Create a draft email:
- To: client@example.com
- Subject: Project Update
- Body: Please review the attached proposal.
"

# Creates draft in default account (adriel)
```

### Example 3: Create Draft in Specific Account

```bash
hermes chat -q "
Create a draft in sitehub account:
- To: contact@example.com
- Subject: Website Service
- Body: We can help with your website.
"
```

### Example 4: List Drafts from Specific Account

```bash
hermes chat -q "List drafts from sitehub account"

# Returns:
# === Drafts (team@sitehubservices.com) ===
# ID: draft_123
# To: ...
```

### Example 5: Send Draft from Specific Account

```bash
hermes chat -q "Send draft from sitehub account: draft_123"
```

### Example 6: Compose Draft for Team Review

```bash
hermes chat -q "
Create draft in adriel account to: team@adrielpartners.com
Subject: Q1 Marketing Plan
Body: Team,

Here's the proposed Q1 marketing plan:
- Focus on social media (Twitter, LinkedIn)
- Launch blog content series
- Partner outreach program

Please review and provide feedback by EOD Thursday.

Best,
Phillip
"

# Creates draft, you review it, then:
# Send draft from adriel account: DRAFT_ID
```

## Verification Checklist

- [ ] `ZOHO_CLIENT_ID` set in `~/.hermes/.env`
- [ ] `ZOHO_CLIENT_SECRET` set in `~/.hermes/.env`
- [ ] `ZOHO_ACCOUNT_ID` set in `~/.hermes/.env`
- [ ] OAuth token obtained (first auth flow completed)
- [ ] Token stored in `~/.hermes/auth.json`
- [ ] Test draft creation: `hermes -s zoho-mail chat -q "Create test draft to yourself"`
- [ ] Test list drafts: `hermes -s zoho-mail chat -q "List my drafts"`

## References

- [Zoho Mail API Docs](https://www.zoho.com/mail/help/api)
- [Zoho OAuth Flow](https://www.zoho.com/accounts/protocol/oauth)
- [API Console](https://api-console.zoho.com)
