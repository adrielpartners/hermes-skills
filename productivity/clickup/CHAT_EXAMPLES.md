# ClickUp Chat API — Usage Guide

New chat messaging functionality added to the ClickUp skill!

## Quick Examples

### 1. List All Chats

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient

client = ClickUpClient()
chats = client.get_chats()

for chat in chats:
    print(f"Chat: {chat.get('name')} (ID: {chat.get('id')})")
    print(f"  Members: {len(chat.get('members', []))}")
    print()
```

### 2. Send Message to Chat

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient

client = ClickUpClient()

# Send message to a specific chat
chat_id = "901234567"  # Replace with your chat ID
response = client.send_message(
    chat_id=chat_id,
    text="🚀 Project update: Design phase complete, moving to development"
)

print(f"Message sent: {response}")
```

### 3. Find Chat by Name and Send Message

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient

client = ClickUpClient()

# Find chat by name
chat = client.get_chat_by_name("team-updates")

if chat:
    response = client.send_message(
        chat_id=chat['id'],
        text="Meeting at 2pm today - don't forget!"
    )
    print(f"✅ Message sent to {chat['name']}")
else:
    print("❌ Chat not found")
```

### 4. Get Recent Chat Messages

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient

client = ClickUpClient()

# Get last 20 messages from a chat
chat_id = "901234567"
messages = client.get_chat_messages(chat_id=chat_id, limit=20)

for msg in messages:
    user = msg.get('user', {})
    timestamp = msg.get('created_at', '')
    content = msg.get('content', '')
    print(f"{user.get('username', 'Unknown')}: {content}")
    print(f"  ({timestamp})\n")
```

### 5. Use in Hermes Chat

```
/skill clickup
> Send a message to the team-updates chat saying "Ready for standup"
```

## New Methods

### `get_chats() → List[Dict]`
Get all chats in the workspace.

**Returns:**
- List of chat objects with id, name, members, etc.

### `get_chat_by_name(chat_name: str) → Optional[Dict]`
Find a chat by its name.

**Args:**
- `chat_name` — Name of the chat

**Returns:**
- Chat object or None if not found

### `get_chat_messages(chat_id: str, limit: int = 50) → List[Dict]`
Get messages from a chat.

**Args:**
- `chat_id` — The chat ID
- `limit` — Max messages to fetch (default 50)

**Returns:**
- List of message objects with id, user, content, created_at

### `send_message(chat_id: str, text: str) → Dict`
Send a message to a chat.

**Args:**
- `chat_id` — The chat ID
- `text` — Message text (plain text or markdown)

**Returns:**
- Message object with id, user, content, created_at

## Common Chat Use Cases

### 1. Daily Standup Reminder

```python
from clickup_client import ClickUpClient
import os

os.environ.update({
    'CLICKUP_API_KEY': os.getenv('CLICKUP_API_KEY'),
    'CLICKUP_WORKSPACE_ID': os.getenv('CLICKUP_WORKSPACE_ID')
})

client = ClickUpClient()
team_chat = client.get_chat_by_name("team")

if team_chat:
    client.send_message(
        team_chat['id'],
        "📅 Daily standup in 30 minutes!\nPlease share:\n- What you completed\n- What you're working on\n- Any blockers"
    )
```

### 2. Task Status Updates

```python
from clickup_client import ClickUpClient
import os

os.environ.update({
    'CLICKUP_API_KEY': os.getenv('CLICKUP_API_KEY'),
    'CLICKUP_WORKSPACE_ID': os.getenv('CLICKUP_WORKSPACE_ID')
})

client = ClickUpClient()

# When a task is completed, announce it
task_name = "Landing page redesign"
chat = client.get_chat_by_name("announcements")

if chat:
    client.send_message(
        chat['id'],
        f"✅ {task_name} has been completed!"
    )
```

### 3. Monitor All Chats

```python
from clickup_client import ClickUpClient
import os

os.environ.update({
    'CLICKUP_API_KEY': os.getenv('CLICKUP_API_KEY'),
    'CLICKUP_WORKSPACE_ID': os.getenv('CLICKUP_WORKSPACE_ID')
})

client = ClickUpClient()
chats = client.get_chats()

print(f"Total chats: {len(chats)}\n")

for chat in chats:
    members = chat.get('members', [])
    print(f"📱 {chat.get('name', 'Unnamed')}")
    print(f"   Members: {', '.join([m.get('username', 'Unknown') for m in members])}")
    print()
```

### 4. Broadcast Message to Multiple Chats

```python
from clickup_client import ClickUpClient
import os

os.environ.update({
    'CLICKUP_API_KEY': os.getenv('CLICKUP_API_KEY'),
    'CLICKUP_WORKSPACE_ID': os.getenv('CLICKUP_WORKSPACE_ID')
})

client = ClickUpClient()
chats = client.get_chats()

# Send to all chats containing "team"
for chat in chats:
    if "team" in chat.get('name', '').lower():
        client.send_message(
            chat['id'],
            "🎉 Important announcement: System maintenance tonight at 8pm"
        )
```

## Limitations & Notes

1. **Message content** — Use plain text or markdown. Rich formatting not yet supported via API.

2. **Chat discovery** — You must find chats by name or iterate through all chats. There's no search endpoint.

3. **Rate limiting** — Same as other ClickUp endpoints (~100 req/min). Space out bulk messages.

4. **Message history** — Limited to 50 messages by default. Increase `limit` parameter to fetch more.

5. **Direct messages** — Works with both group chats and DMs. Use the DM chat ID the same way.

## Troubleshooting

**"Chat not found"**
- Verify the chat ID is correct
- Use `get_chats()` first to see available chats
- Chat names are case-sensitive when using `get_chat_by_name()`

**"Message failed to send"**
- Check the chat_id exists
- Message text cannot be empty
- Verify API key has chat access (check ClickUp permissions)

**"Getting wrong chat"**
- Multiple chats may have similar names
- Use the chat ID directly instead of name matching
- Loop through `get_chats()` to verify correct ID

## Next Steps

- Use in scheduled jobs (cron): Send daily updates automatically
- Integrate with task workflows: Alert team when tasks change status
- Build chat integrations: Sync messages with external systems
- Create chat notifications: Alert team on important events

Happy messaging! 💬
