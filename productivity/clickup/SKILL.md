---
name: clickup
description: "Use when managing ClickUp tasks, lists, folders, attachments, team assignments, and direct chat messaging. Create tasks, organize workflows, collaborate with team chat, upload files, and automate ClickUp operations."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [clickup, productivity, task-management, collaboration, api]
    related_skills: [linear, airtable, notion, google-workspace]
---

# ClickUp Integration

Comprehensive skill for interacting with ClickUp from Hermes Agent. Supports tasks, lists, folders, comments, attachments, team member assignments, status management, and chat messaging.

## Overview

ClickUp is a powerful work management platform. This skill provides Hermes Agent with full CRUD operations across the most common ClickUp workflows:

- **Tasks** — create, read, update, delete, list, search
- **Lists & Folders** — organize hierarchies, move tasks between spaces
- **Comments** — add rich-text comments to tasks
- **Attachments** — upload files and download task attachments
- **Team Management** — assign/unassign team members, set priorities and statuses
- **Status Workflow** — query custom statuses, transition tasks through workflows
- **Chat & Messaging** — send messages to chats, fetch chat history, coordinate with team

All operations use the official ClickUp API v2 and require a valid API token.

## When to Use

- You're building workflows that sync ClickUp with external systems (CI/CD, webhooks, data pipelines)
- You need to automate task creation, bulk updates, or deadline management
- You're organizing large projects and want scripted list/folder creation
- You need to extract ClickUp data for reporting or analysis
- You're assigning work and want to batch-process team assignments
- You're uploading files or archival attachments to tasks programmatically

**Don't use for:**
- Manual, one-off task edits (use the ClickUp UI instead)
- Real-time polling with high frequency (use ClickUp webhooks + Hermes gateway integration instead)
- Task comments in high-volume channels (use the ClickUp UI for discussion threads)

## Setup

### API Credentials

1. **Get your API key:**
   - Go to [app.clickup.com](https://app.clickup.com)
   - User menu → Settings → API → Copy API Token
   - Never share or commit this token

2. **Store in `.env`:**
   ```bash
   CLICKUP_API_KEY=pk_1234...
   CLICKUP_WORKSPACE_ID=9876543
   ```

3. **Find your Workspace ID:**
   - In ClickUp UI: look at the team dropdown menu
   - Or via API:
   ```bash
   curl https://api.clickup.com/api/v2/team \
     -H "Authorization: pk_your_token"
   ```

### Required Credentials

| Variable | Description |
|----------|-------------|
| `CLICKUP_API_KEY` | Your ClickUp API personal token |
| `CLICKUP_WORKSPACE_ID` | Your workspace/team ID (e.g. 1233538) |

## Operations

### Authentication

All operations use the `Authorization` header with your API key. Hermes automatically loads credentials from environment variables or `~/.hermes/.env`.

### Tasks

#### Create a Task

```python
# Minimal
curl https://api.clickup.com/api/v2/list/{list_id}/task \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Build checkout flow"}'

# With metadata
curl https://api.clickup.com/api/v2/list/{list_id}/task \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Build checkout flow",
    "description": "Implement payment gateway",
    "assignees": [1234567],
    "status": "in_progress",
    "priority": 2,
    "due_date": 1735689600000
  }'
```

**Response:** `{ "id": "task_id", "task_id": "ABC123", "name": "...", ... }`

#### Get Task

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -H "Authorization: pk_your_key"
```

#### Update Task

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -X PUT \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated title",
    "status": "completed",
    "priority": 1,
    "assignees": {
      "add": [1234567],
      "rem": []
    }
  }'
```

#### List Tasks in a List

```bash
curl https://api.clickup.com/api/v2/list/{list_id}/task \
  -H "Authorization: pk_your_key"
```

#### Delete Task

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -X DELETE \
  -H "Authorization: pk_your_key"
```

### Lists

#### Get Lists in a Folder

```bash
curl https://api.clickup.com/api/v2/folder/{folder_id}/list \
  -H "Authorization: pk_your_key"
```

#### Create a List

```bash
curl https://api.clickup.com/api/v2/folder/{folder_id}/list \
  -X POST \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Marketing Q1 2025"}'
```

#### Delete a List

```bash
curl https://api.clickup.com/api/v2/list/{list_id} \
  -X DELETE \
  -H "Authorization: pk_your_key"
```

### Folders

#### Get Folders in a Space

```bash
curl https://api.clickup.com/api/v2/space/{space_id}/folder \
  -H "Authorization: pk_your_key"
```

#### Create a Folder

```bash
curl https://api.clickup.com/api/v2/space/{space_id}/folder \
  -X POST \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Product Development"}'
```

#### Delete a Folder

```bash
curl https://api.clickup.com/api/v2/folder/{folder_id} \
  -X DELETE \
  -H "Authorization: pk_your_key"
```

### Comments

#### Add Comment to Task

```bash
curl https://api.clickup.com/api/v2/task/{task_id}/comment \
  -X POST \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "comment_text": "This is the final design review. Approved!",
    "assignee": 1234567
  }'
```

#### Get Task Comments

```bash
curl https://api.clickup.com/api/v2/task/{task_id}/comment \
  -H "Authorization: pk_your_key"
```

### Attachments

#### Upload File to Task

```bash
# Multipart form upload
curl https://api.clickup.com/api/v2/task/{task_id}/attachment \
  -X POST \
  -H "Authorization: pk_your_key" \
  -F "attachment=@/path/to/file.pdf"
```

#### Get Task Attachments

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -H "Authorization: pk_your_key" \
  | jq '.task.attachments'
```

#### Download Attachment

Attachments have a `url` field. Simply fetch:

```bash
curl https://attachments.clickup.com/...
```

### Team Member Assignment

#### Assign Member to Task

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -X PUT \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"assignees": {"add": [1234567]}}'
```

#### Unassign Member

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -X PUT \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"assignees": {"rem": [1234567]}}'
```

#### Get Team Members

```bash
curl https://api.clickup.com/api/v2/team/{team_id} \
  -H "Authorization: pk_your_key" \
  | jq '.team.members[] | {id: .user.id, username: .user.username, email: .user.email}'
```

### Status Management

#### Set Task Status

Statuses are list-specific. First query the list to see available statuses:

```bash
curl https://api.clickup.com/api/v2/list/{list_id} \
  -H "Authorization: pk_your_key" \
  | jq '.list.statuses'
```

Then set:

```bash
curl https://api.clickup.com/api/v2/task/{task_id} \
  -X PUT \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

Common statuses: `to_do`, `in_progress`, `in_review`, `completed`

### Chat

#### Get All Chats in Workspace

```bash
curl https://api.clickup.com/api/v2/team/{team_id}/chat \
  -H "Authorization: pk_your_key"
```

Returns list of all chats (both direct messages and channels).

#### Get Chat Messages

```bash
curl https://api.clickup.com/api/v2/chat/{chat_id}/message \
  -H "Authorization: pk_your_key" \
  --data-urlencode "limit=50"
```

Fetches up to 50 most recent messages from a chat.

#### Send Message to Chat

```bash
curl https://api.clickup.com/api/v2/chat/{chat_id}/message \
  -X POST \
  -H "Authorization: pk_your_key" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is my message"}'
```

Sends a plain text or markdown message to a chat or direct message.

**Response:** `{ "chat_message_id": "...", "user": {...}, "content": "...", "created_at": 1234567890 }`

## Chat & Messaging (v1.1.0+ — DEPRECATED / NOT SUPPORTED)\n\n⚠️ **DO NOT USE.** Chat API methods are **non-functional.** The ClickUp API v2 does not expose public chat endpoints.\n\n❌ Methods below will fail (listed for reference only):\n- `get_chats()` — Returns 404\n- `get_chat_by_name(name)` — Returns 404\n- `get_chat_messages(chat_id, limit=50)` — Returns 404\n- `send_message(chat_id, text)` — Returns 404\n\n**Verified:** All `/chat` and `/message` endpoints return 404 Not Found regardless of API key validity or subscription tier. See **`references/chat-api-limitation.md`** for:\n- Root cause analysis\n- Verification steps\n- **Workarounds:** Use task comments (`add_comment()`), email, or gateway messaging (Telegram, Slack, Discord)\n\n**Recommendation:** For team communication, use:\n1. **Task comments** — Reliable, tied to work context\n2. **Email notifications** — Via Google Workspace skill\n3. **Gateway messaging** — Telegram, Slack, Discord integration

## Pitfalls & Solutions

1. **"Unauthorized" on first use**
   - Verify API key is in `.env` with exact key name: `CLICKUP_API_KEY`
   - Regenerate the token in ClickUp if you suspect it's expired or rotated
   - Check that the token has not been revoked (Settings → API)

2. **"Invalid list_id" or "Invalid task_id"**
   - IDs in ClickUp can be either numeric or custom alphanumeric strings
   - When copying from the UI, make sure you're using the ID from the URL or API response, not the task number (e.g., `ABC-123`)
   - List IDs and task IDs are different — don't mix them

3. **Attachments upload fails**
   - Ensure the file path exists and is readable
   - Use multipart/form-data, not JSON
   - File size limits: ClickUp typically allows up to 50MB per file (check your plan)

4. **Batch operations hit rate limits**
   - ClickUp API rate limit: ~100 requests/minute for most endpoints
   - When creating many tasks, add a small delay (e.g., 0.5s) between requests
   - Use cursor-based pagination for large lists instead of polling

5. **Comments don't appear or are rejected**
   - Comment text must be non-empty
   - Rich text formatting uses HTML tags — plain text is fine
   - If assigning someone in the comment, their user ID must be valid

6. **Status transitions fail silently**
   - Not all statuses are reachable from all states (depends on list workflow rules)
   - Check the list's configured status workflow in ClickUp UI
   - Some statuses may be read-only or hidden

7. **Assignee operations don't take effect**
   - Verify the user ID is correct — use the `/api/v2/team/{team_id}` endpoint to list members
   - Guest users may have limited assignment permissions
   - Check the task type — some custom fields may override assignees

8. **Chat API returns 404 (get_chats, send_message, etc.) — KNOWN ISSUE**
   - ⚠️ **This is not a configuration problem.** The ClickUp API v2 does not expose public chat endpoints.
   - Chat API methods in this skill **will not work** regardless of subscription or permissions.
   - **Workaround:** Use task comments (`add_comment()`) which work reliably, or use email/gateway messaging.
   - See **`references/chat-api-limitation.md`** for full details, verification, and alternatives.

## Verification Checklist

- [ ] `CLICKUP_API_KEY` set in `~/.hermes/.env`
- [ ] `CLICKUP_WORKSPACE_ID` set in `~/.hermes/.env`
- [ ] API token works: `curl https://api.clickup.com/api/v2/team/{TEAM_ID} -H "Authorization: pk_your_key"` returns 200
- [ ] Task IDs resolve: test with a known task ID from your workspace
- [ ] List IDs and folder IDs are available: query space/folder hierarchy first
- [ ] Team member IDs are correct: use team endpoint to cross-reference
- [ ] File attachments readable: ensure paths are absolute or relative to cwd
- [ ] **Terminal security gate cleared:** Run `python3 ~/.hermes/skills/productivity/clickup/scripts/test_security_gate.py` (see `references/terminal-api-security.md` if blocked)

## Usage Examples

### Example 1: Create and Assign a Task

```python
import requests
import os
from datetime import datetime, timedelta

CLICKUP_KEY = os.getenv("CLICKUP_API_KEY")
WORKSPACE_ID = os.getenv("CLICKUP_WORKSPACE_ID")

# Create task
list_id = "901234567"  # Get from ClickUp UI
task_data = {
    "name": "Design landing page",
    "description": "Create mockups in Figma and present to client",
    "assignees": [1234567],  # Phillip's user ID
    "priority": 2,
    "due_date": int((datetime.now() + timedelta(days=7)).timestamp() * 1000),
    "status": "to_do"
}

response = requests.post(
    f"https://api.clickup.com/api/v2/list/{list_id}/task",
    json=task_data,
    headers={"Authorization": CLICKUP_KEY}
)

task = response.json()["task"]
print(f"Created task {task['id']}: {task['name']}")
```

### Example 2: Upload File to Task

```python
import requests
import os

CLICKUP_KEY = os.getenv("CLICKUP_API_KEY")
task_id = "ABC123XYZ"

with open("/path/to/design.pdf", "rb") as f:
    files = {"attachment": f}
    response = requests.post(
        f"https://api.clickup.com/api/v2/task/{task_id}/attachment",
        files=files,
        headers={"Authorization": CLICKUP_KEY}
    )

print(f"Attachment uploaded: {response.json()}")
```

### Example 3: List All Tasks and Filter by Status

```python
import requests
import os

CLICKUP_KEY = os.getenv("CLICKUP_API_KEY")
list_id = "901234567"

response = requests.get(
    f"https://api.clickup.com/api/v2/list/{list_id}/task",
    headers={"Authorization": CLICKUP_KEY}
)

tasks = response.json()["tasks"]
in_progress = [t for t in tasks if t.get("status", {}).get("status") == "in_progress"]

for task in in_progress:
    print(f"- {task['name']} (assigned to: {', '.join([a['username'] for a in task.get('assignees', [])])})")
```

## API Reference

Full ClickUp API v2 documentation: [https://clickup.com/api](https://clickup.com/api)

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/team/{team_id}` | Get team/workspace members |
| GET | `/space/{space_id}/folder` | List folders in space |
| POST | `/space/{space_id}/folder` | Create folder |
| GET | `/folder/{folder_id}/list` | List lists in folder |
| POST | `/folder/{folder_id}/list` | Create list |
| GET | `/list/{list_id}/task` | List tasks in list |
| POST | `/list/{list_id}/task` | Create task |
| GET | `/task/{task_id}` | Get task details |
| PUT | `/task/{task_id}` | Update task |
| DELETE | `/task/{task_id}` | Delete task |
|| POST | `/task/{task_id}/comment` | Add comment |
|| GET | `/task/{task_id}/comment` | Get comments |
|| POST | `/task/{task_id}/attachment` | Upload file |
|| GET | `/team/{team_id}/chat` | List all chats |
|| GET | `/chat/{chat_id}/message` | Get chat messages |
|| POST | `/chat/{chat_id}/message` | Send message to chat |

