# ClickUp Skill — Setup Complete ✅

Your custom ClickUp skill is ready to use!

## 📁 Files Created

```
~/.hermes/skills/productivity/clickup/
├── SKILL.md              # Full documentation (12KB)
├── clickup_client.py     # Python wrapper for ClickUp API v2 (8KB)
├── QUICK_START.md        # Quick reference guide with examples
├── examples.py           # 8 realistic workflow examples
└── README.md             # This file
```

## 🔑 Credentials

Your API credentials are configured. Store them securely:

```bash
# Add to ~/.hermes/.env
CLICKUP_API_KEY=pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT
CLICKUP_WORKSPACE_ID=1233538
```

**Workspace:** ADRIEL PARTNERS

**Team Members:**
- Armando Pulgar (armandopulgarb@gmail.com) [ID: 101207393]
- Noble Daniel (thenobledaniel@gmail.com) [ID: 55307323]
- Isabella Amengual (amengualisabella@gmail.com) [ID: 3017021]
- AB (digital.b3asts@gmail.com) [ID: 54035174]
- Phillip Gonzales (phillip@phillipgonzales.com) [ID: 1377633] — Owner

## 🚀 Quick Start

### 1. Test the Connection

```bash
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

Expected output: List of all team members with IDs and emails.

### 2. Use in Python

```python
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
from clickup_client import ClickUpClient

client = ClickUpClient()

# Create a task
task = client.create_task(
    list_id="901234567",  # Replace with actual list ID
    name="My Task",
    status="to_do"
)

# Assign to someone
member = client.get_member_by_username("Noble Daniel")
client.update_task(
    task_id=task["task"]["id"],
    assignees_add=[member["user"]["id"]]
)
```

### 3. Use in Hermes Sessions

Load the skill in your session:

```
/skill clickup
```

Then ask Hermes to help with ClickUp tasks:

> "Create a task in ClickUp for 'Design landing page' and assign it to Phillip Gonzales"
>
> "Upload the design.pdf file to task ABC123"
>
> "List all incomplete tasks in my main project list"

## 📚 Operations Supported

### Tasks
- `create_task()` — Create a new task
- `get_task()` — Get task details
- `update_task()` — Update name, status, assignees, priority, due date
- `list_tasks()` — Get all tasks in a list
- `delete_task()` — Delete a task

### Lists & Folders
- `create_list()` — Create a new list in a folder
- `get_lists()` — List all lists in a folder
- `delete_list()` — Delete a list
- `create_folder()` — Create a new folder in a space
- `get_folders()` — List folders in a space
- `delete_folder()` — Delete a folder

### Comments
- `add_comment()` — Add a comment to a task
- `get_comments()` — Get all comments on a task

### Attachments
- `upload_attachment()` — Upload a file to a task
- `get_task_attachments()` — Get attachments on a task

### Team & Status
- `get_team_members()` — List all team members
- `get_member_by_email()` — Find member by email
- `get_member_by_username()` — Find member by username
- `get_list_statuses()` — Get available statuses for a list
- `set_task_status()` — Change task status

## 🎯 Common Workflows

See `QUICK_START.md` for copy-paste examples:

1. **Create and assign a task**
2. **Upload file to task**
3. **List all tasks with filters**
4. **Add comment to task**
5. **Create list and folder structure**

See `examples.py` for advanced patterns:

1. Create weekly tasks
2. Assign to team
3. Bulk update status
4. Upload batch files
5. Add comments with mentions
6. Duplicate list structure (templates)
7. Get overdue tasks
8. Create project from template

## 🔍 Finding IDs

Before using the skill, you need:

- **List ID** — `curl https://api.clickup.com/api/v2/folder/{folder_id}/list -H "Authorization: pk_..."`
- **Folder ID** — `curl https://api.clickup.com/api/v2/space/{space_id}/folder -H "Authorization: pk_..."`
- **Space ID** — `curl https://api.clickup.com/api/v2/team/1233538 -H "Authorization: pk_..." | jq '.team.spaces'`
- **Task ID** — Visible in ClickUp URL or API responses

## ⚠️ Important Notes

1. **API Rate Limits** — ClickUp allows ~100 requests/minute. Add delays (0.5s) for batch operations.

2. **Status Workflow** — Not all statuses are reachable from all states. Check your list's workflow rules.

3. **Attachments** — File size limit typically 50MB (depends on your plan).

4. **Multipart Upload** — Attachments use `multipart/form-data`, not JSON.

5. **Security** — Keep your API key private. Never commit to git.

## 📖 Full Documentation

See `SKILL.md` for:
- Detailed setup instructions
- All API endpoints and parameters
- Authentication details
- Common pitfalls and solutions
- Verification checklist
- Full API reference

## 🐛 Troubleshooting

**"Unauthorized" error:**
- Check `CLICKUP_API_KEY` is in `~/.hermes/.env`
- Verify the token hasn't been revoked in ClickUp settings

**"Invalid list_id":**
- List IDs can be numeric or alphanumeric
- Get your actual list ID from the ClickUp API or UI

**File upload fails:**
- Use multipart/form-data (not JSON)
- Ensure file path exists and is readable
- Check file size is within plan limits

**Rate limit errors:**
- Slow down: add `time.sleep(0.5)` between requests
- Use pagination instead of polling

## 📞 Next Steps

1. **Test it:** Run `python clickup_client.py team` to verify setup
2. **Read docs:** Open `SKILL.md` for full reference
3. **Try examples:** See `examples.py` for real workflows
4. **Use in Hermes:** Load with `/skill clickup` or `hermes -s clickup`

Happy task managing! 🎉
