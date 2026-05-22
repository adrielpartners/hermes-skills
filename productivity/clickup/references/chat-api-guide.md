# ClickUp Chat API — Reference Guide

**Added in v1.1.0.** Four new methods for sending and receiving messages in ClickUp chats (both team channels and direct messages).

## Quick Lookup

| Method | Purpose | Returns |
|--------|---------|---------|
| `get_chats()` | List all chats in workspace | `List[Dict]` with id, name, members |
| `get_chat_by_name(name)` | Find chat by name | `Dict` (chat object) or `None` |
| `get_chat_messages(chat_id, limit=50)` | Fetch recent messages | `List[Dict]` with user, content, created_at |
| `send_message(chat_id, text)` | Send message to chat | `Dict` (message object with id, timestamp) |

## API Endpoints

```
GET  /team/{team_id}/chat                 → List all chats
GET  /chat/{chat_id}/message?limit=N      → Get messages (default limit 50)
POST /chat/{chat_id}/message              → Send message
```

## Common Patterns

### 1. Notify Team on Task Status Change

```python
from clickup_client import ClickUpClient

client = ClickUpClient()
announcements = client.get_chat_by_name("announcements")

if announcements:
    client.send_message(
        announcements['id'],
        f"✅ Task completed: 'Landing page redesign' is now live!"
    )
```

### 2. Daily Standup Reminder

Use in a cron job (every weekday 9am):

```python
from clickup_client import ClickUpClient

client = ClickUpClient()
team = client.get_chat_by_name("team")

if team:
    client.send_message(
        team['id'],
        "📅 **Daily Standup in 30 min**\nShare:\n• What you completed\n• Today's focus\n• Any blockers"
    )
```

### 3. Broadcast to Multiple Chats

```python
from clickup_client import ClickUpClient

client = ClickUpClient()
chats = client.get_chats()

message = "🎉 Release v1.2.0 is now live!"

for chat in chats:
    if "team" in chat.get('name', '').lower():
        client.send_message(chat['id'], message)
```

### 4. Retrieve Chat History

```python
from clickup_client import ClickUpClient

client = ClickUpClient()
chat_id = "901234567"

# Get last 100 messages
messages = client.get_chat_messages(chat_id, limit=100)

for msg in messages:
    user = msg.get('user', {}).get('username', 'Unknown')
    text = msg.get('content', '')
    print(f"{user}: {text}")
```

## Pitfalls

**"Chat not found" when using `get_chat_by_name()`**
- Chat names are case-sensitive
- Multiple chats may have similar names — prefer using chat ID directly if you know it
- Get the exact name with `get_chats()` first

**"Message failed to send"**
- Verify chat_id exists (not a workspace ID or other resource)
- Message text must be non-empty
- Check API key has chat permissions (rare edge case)

**Rate limiting on bulk sends**
- ClickUp API limit: ~100 requests/minute
- Add `time.sleep(0.5)` between sends if broadcasting to many chats

**Chat vs. Direct Message**
- DMs use the same API — find them with `get_chats()` and send the same way
- Both are treated as "chats" by the API

## Markdown Support

Messages support basic markdown:
- `**bold**` → bold
- `_italic_` → italic
- `- bullet` → bullets
- `` `code` `` → inline code
- Line breaks (`\n`) → new lines

Plain text also works fine.

## Integration Example: Hermes Cron Job

```bash
hermes cron create "0 9 * * 1-5" \
  -s clickup \
  -q "Send standup reminder to the team chat using ClickUp"
```

Hermes loads the skill, finds the `team` chat, and sends the message automatically each weekday at 9am.

## Next Steps

- See CHAT_EXAMPLES.md for 10+ full working examples
- See SKILL.md for complete API docs
- Test locally: `python clickup_client.py team` to list chats
