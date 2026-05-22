# ClickUp Skill Quick Reference

## Setup

```bash
# 1. Set your credentials in ~/.hermes/.env
echo "CLICKUP_API_KEY=pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" >> ~/.hermes/.env
echo "CLICKUP_WORKSPACE_ID=1233538" >> ~/.hermes/.env

# 2. Test the connection
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

## Common Workflows

### 1. Create a Task

```python
from hermes_tools import terminal
import json

# Get the skill first
result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Create task
task = client.create_task(
    list_id="901234567",  # Replace with your list ID
    name="Review design mockups",
    description="Check Figma designs and provide feedback",
    status="to_do",
    priority=2,  # 1=urgent, 2=high, 3=normal, 4=low
)

print(json.dumps(task, indent=2))
EOF
""")

print(result["output"])
```

### 2. Assign Task to Team Member

```python
from hermes_tools import terminal
import json

result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Find team member by username
member = client.get_member_by_username("Noble Daniel")
if member:
    user_id = member["user"]["id"]
    
    # Assign to task
    task = client.update_task(
        task_id="ABC123XYZ",  # Replace with your task ID
        assignees_add=[user_id]
    )
    print(f"Assigned to {member['user']['username']}")
else:
    print("Member not found")
EOF
""")

print(result["output"])
```

### 3. Upload File to Task

```python
from hermes_tools import terminal

result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Upload a file
result = client.upload_attachment(
    task_id="ABC123XYZ",  # Replace with your task ID
    file_path="/path/to/your/file.pdf"
)

print(f"File uploaded: {result}")
EOF
""")

print(result["output"])
```

### 4. List All Tasks in a List

```python
from hermes_tools import terminal
import json

result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Get all tasks
tasks_response = client.list_tasks(list_id="901234567")  # Replace with your list ID
tasks = tasks_response.get("tasks", [])

for task in tasks:
    status = task.get("status", {}).get("status", "unknown")
    assignees = [a["username"] for a in task.get("assignees", [])]
    print(f"- {task['name']} [{status}] → {', '.join(assignees) or 'Unassigned'}")
EOF
""")

print(result["output"])
```

### 5. Add Comment to Task

```python
from hermes_tools import terminal

result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Add comment
comment = client.add_comment(
    task_id="ABC123XYZ",  # Replace with your task ID
    text="Design looks good! Ready for implementation."
)

print(f"Comment added: {comment}")
EOF
""")

print(result["output"])
```

### 6. Create List and Folder Structure

```python
from hermes_tools import terminal
import json

result = terminal("""
python3 << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

from clickup_client import ClickUpClient

client = ClickUpClient()

# Create folder (replace space_id with your space ID)
folder = client.create_folder(space_id="1234567", name="Product Launch Q2 2025")
folder_id = folder["folder"]["id"]
print(f"Created folder: {folder_id}")

# Create list in folder
new_list = client.create_list(folder_id=folder_id, name="Marketing Tasks")
list_id = new_list["list"]["id"]
print(f"Created list: {list_id}")

# Create first task
task = client.create_task(
    list_id=list_id,
    name="Create landing page copy",
    status="to_do"
)
print(f"Created task: {task['task']['id']}")
EOF
""")

print(result["output"])
```

## Finding IDs

You need workspace, space, folder, and list IDs for various operations.

### Get Team Members (with IDs)

```bash
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

Output:
```json
[
  {
    "id": 1377633,
    "username": "Phillip Gonzales",
    "email": "phillip@phillipgonzales.com"
  },
  ...
]
```

### Get Space ID

The workspace (team) ID is `1233538` (you provided this). To find spaces:

```bash
curl https://api.clickup.com/api/v2/team/1233538 \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" | jq '.team.spaces'
```

### Get Folder ID

```bash
curl https://api.clickup.com/api/v2/space/{space_id}/folder \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" | jq '.folders[] | {id, name}'
```

### Get List ID

```bash
curl https://api.clickup.com/api/v2/folder/{folder_id}/list \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" | jq '.lists[] | {id, name}'
```

## API Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | N/A |
| 400 | Bad request | Check payload format and required fields |
| 401 | Unauthorized | Verify API key in `.env` |
| 404 | Not found | Check ID (list, task, folder) is correct |
| 429 | Rate limited | Wait a minute, then retry |
| 500 | Server error | Try again later |

## More Examples

See `SKILL.md` in the same directory for full documentation and additional examples.
