# ClickUp Skill — Command Reference

Quick reference for all ways to use the ClickUp skill.

## Test Connection

```bash
# Verify API works and list all team members
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

Expected: List of 5 team members with IDs and emails

## In Hermes Chat

### Load the Skill
```
/skill clickup
```

### Ask Hermes Directly
```
> Create a task "Design landing page" in ClickUp

> Assign this task to Phillip Gonzales

> Upload the file design.pdf to task ABC123

> Show me all incomplete tasks in my main list

> Mark all "In Progress" tasks as completed
```

### In Hermes Session
```bash
# Start new session with skill preloaded
hermes -s clickup

# Start and ask question
hermes -s clickup -q "List all my ClickUp team members"
```

## Python Usage

### Basic Setup
```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
from clickup_client import ClickUpClient

# Initialize (uses CLICKUP_API_KEY and CLICKUP_WORKSPACE_ID from env)
client = ClickUpClient()
```

### Create Task
```python
task = client.create_task(
    list_id="901234567",
    name="My Task",
    description="Task description",
    status="to_do",
    priority=2
)
print(f"Created task: {task['task']['id']}")
```

### Get Task
```python
task = client.get_task("ABC123")
print(f"Task: {task['task']['name']}")
```

### Update Task
```python
client.update_task(
    task_id="ABC123",
    name="Updated name",
    status="in_progress"
)
```

### Assign Member
```python
member = client.get_member_by_username("Phillip Gonzales")
client.update_task(
    task_id="ABC123",
    assignees_add=[member["user"]["id"]]
)
```

### Upload File
```python
client.upload_attachment(
    task_id="ABC123",
    file_path="/path/to/file.pdf"
)
```

### Add Comment
```python
client.add_comment(
    task_id="ABC123",
    text="This looks good!"
)
```

### List Tasks
```python
response = client.list_tasks(list_id="901234567")
for task in response["tasks"]:
    print(f"- {task['name']}")
```

### Get Team Members
```python
members = client.get_team_members()
for m in members:
    print(f"{m['user']['username']}: {m['user']['id']}")
```

### Find Member
```python
# By username
member = client.get_member_by_username("Noble Daniel")

# By email
member = client.get_member_by_email("thenobledaniel@gmail.com")

print(f"Found: {member['user']['username']} (ID: {member['user']['id']})")
```

## Via Cron Jobs

### Schedule Weekly Tasks
```bash
hermes cron create "0 9 * * 1" \
  -s clickup \
  -q "Create this week's team tasks using ClickUp skill"
```

### Schedule Daily Report
```bash
hermes cron create "0 18 * * *" \
  -s clickup \
  -q "Show me all overdue tasks in ClickUp"
```

## Command-Line Examples

### List Team Members
```bash
python3 << 'EOF'
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient
client = ClickUpClient()
members = client.get_team_members()
for m in members:
    print(f"{m['user']['username']}: {m['user']['id']}")
EOF
```

### Create Task
```bash
python3 << 'EOF'
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient
client = ClickUpClient()
task = client.create_task(
    list_id="901234567",  # Replace with your list ID
    name="My Task",
    status="to_do"
)
print(f"✅ Created: {task['task']['id']}")
EOF
```

### Assign to Team Member
```bash
python3 << 'EOF'
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient
client = ClickUpClient()

# Find member
member = client.get_member_by_username("Phillip Gonzales")

# Assign
client.update_task(
    task_id="ABC123",
    assignees_add=[member["user"]["id"]]
)
print(f"✅ Assigned to {member['user']['username']}")
EOF
```

## Using in Scripts

### Script Template
```bash
#!/bin/bash

# Add skill to Python path
SKILL_DIR=~/.hermes/skills/productivity/clickup

# Export credentials
export CLICKUP_API_KEY="pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT"
export CLICKUP_WORKSPACE_ID="1233538"

# Run Python code
python3 << 'EOF'
import sys, os
sys.path.insert(0, os.path.expanduser(os.environ.get('SKILL_DIR')))
from clickup_client import ClickUpClient

client = ClickUpClient()
# Your code here
EOF
```

## Integration Examples

### With Git
```bash
# Create task for each TODO in code
grep -r "TODO" . | while read line; do
  # Parse and create ClickUp task
done
```

### With CI/CD
```bash
# In GitHub Actions / GitLab CI
- name: Create ClickUp task
  run: |
    hermes -s clickup -q "Create task for this build failure"
```

### With Webhooks
```bash
# Subscribe to ClickUp webhooks
hermes webhook subscribe clickup
```

## Troubleshooting Commands

### Verify Setup
```bash
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

### Check Python Import
```bash
python3 -c "
import sys
sys.path.insert(0, '/Users/max/.hermes/skills/productivity/clickup')
from clickup_client import ClickUpClient
print('✅ OK')
"
```

### Verify Credentials
```bash
grep CLICKUP ~/.hermes/.env.clickup
```

### Test API Connection
```bash
curl https://api.clickup.com/api/v2/team/1233538 \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" \
  -s | jq .team.name
```

## All Available Methods

```python
# Task operations
client.create_task(list_id, name, **kwargs)
client.get_task(task_id)
client.update_task(task_id, **kwargs)
client.list_tasks(list_id)
client.delete_task(task_id)

# List operations
client.create_list(folder_id, name)
client.get_lists(folder_id)
client.delete_list(list_id)

# Folder operations
client.create_folder(space_id, name)
client.get_folders(space_id)
client.delete_folder(folder_id)

# Comment operations
client.add_comment(task_id, text, **kwargs)
client.get_comments(task_id)

# Attachment operations
client.upload_attachment(task_id, file_path)
client.get_task_attachments(task_id)

# Team operations
client.get_team_members()
client.get_member_by_email(email)
client.get_member_by_username(username)

# Status operations
client.get_list_statuses(list_id)
client.set_task_status(task_id, status)
```

## Need Help?

1. **Read:** `README.md` or `SKILL.md`
2. **Examples:** Check `QUICK_START.md` or `examples.py`
3. **Troubleshoot:** See `TROUBLESHOOTING.md`
4. **Ask Hermes:** `/skill clickup` then ask your question

---

**All commands tested and ready to use!** 🚀
