# ClickUp Skill — Troubleshooting Guide

Common issues and solutions when using the ClickUp skill with Hermes Agent.

## API Connection Issues

### Error: "Unauthorized" or "401"

**Symptoms:**
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: https://api.clickup.com/api/v2/...
```

**Solutions:**
1. Check credentials are set:
   ```bash
   echo $CLICKUP_API_KEY
   echo $CLICKUP_WORKSPACE_ID
   ```

2. Verify file `~/.hermes/.env` contains:
   ```
   CLICKUP_API_KEY=pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT
   CLICKUP_WORKSPACE_ID=1233538
   ```

3. Regenerate token in ClickUp (may have expired):
   - Go to app.clickup.com
   - User menu → Settings → API → Regenerate token
   - Update `.env` with new token

4. Check token hasn't been revoked:
   - Settings → API → Verify your token is listed
   - If not, generate a new one

### Error: "Connection refused" or "Failed to connect"

**Symptoms:**
```
requests.exceptions.ConnectionError: Failed to establish a new connection
```

**Solutions:**
1. Check internet connection: `ping api.clickup.com`
2. Check firewall isn't blocking ClickUp API
3. Try using a VPN if ClickUp API is geo-blocked
4. Wait a moment — the API may be temporarily down

### Error: "HTTP 429 — Too Many Requests"

**Symptoms:**
```
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests
```

**Cause:** Rate limit exceeded (ClickUp limits ~100 requests/minute)

**Solutions:**
1. Add delay between requests:
   ```python
   import time
   for task in tasks:
       client.create_task(...)
       time.sleep(0.5)  # Wait 500ms between requests
   ```

2. Use pagination for large lists instead of polling
3. Wait 1-2 minutes before retrying
4. Batch operations when possible

## ID/Reference Issues

### Error: "Invalid list_id" or "404 Not Found"

**Symptoms:**
```
"error": "Invalid list_id"
```

**Solutions:**
1. Verify you have the correct list ID:
   ```bash
   curl https://api.clickup.com/api/v2/folder/{folder_id}/list \
     -H "Authorization: pk_..."
   ```

2. List IDs can be numeric or alphanumeric — verify format matches
3. Task IDs and list IDs are different — don't mix them
4. IDs from ClickUp UI URL are usually correct

### Error: "Task not found"

**Solutions:**
1. Check task exists:
   ```python
   client.get_task("ABC123")  # Will error if not found
   ```

2. Verify task ID from:
   - ClickUp URL: `app.clickup.com/t/{task_id}`
   - API response from `create_task` or `list_tasks`
   - ClickUp UI (right-click task → Copy link)

3. Task may have been deleted — check in ClickUp UI

### Error: "Member not found" when assigning

**Symptoms:**
```
client.update_task(..., assignees_add=[99999999])  # Invalid user ID
```

**Solutions:**
1. Get correct user ID:
   ```python
   members = client.get_team_members()
   for m in members:
       print(f"{m['user']['username']}: {m['user']['id']}")
   ```

2. Or use convenience methods:
   ```python
   member = client.get_member_by_username("Phillip Gonzales")
   user_id = member["user"]["id"]
   ```

3. Verify member is in your workspace (not a guest with limited access)

## Attachment Issues

### Error: "File upload failed" or "400 Bad Request"

**Symptoms:**
```
requests.exceptions.HTTPError: 400 Client Error: Bad Request
```

**Solutions:**
1. Verify file exists and is readable:
   ```python
   import os
   assert os.path.isfile("/path/to/file.pdf")
   ```

2. Use absolute path:
   ```python
   import os
   filepath = os.path.abspath("design.pdf")
   client.upload_attachment(task_id, filepath)
   ```

3. Check file size is within limit (typically 50MB)
4. Use multipart/form-data (handled by `upload_attachment()`)

### Attachment not appearing in task

**Solutions:**
1. Verify upload succeeded (check response)
2. Refresh ClickUp UI (F5)
3. Check you uploaded to correct task ID
4. Verify you have permission to upload files

## Status & Workflow Issues

### Error: "Invalid status" or "400 Bad Request" when setting status

**Symptoms:**
```
client.set_task_status(task_id, "custom_status")  # Doesn't work
```

**Solutions:**
1. Get valid statuses for the list:
   ```python
   statuses = client.get_list_statuses(list_id)
   for s in statuses:
       print(f"  - {s['status']}")
   ```

2. Use only statuses defined in that list's workflow
3. Not all statuses are reachable from all states (workflow rules)
4. Check ClickUp UI for list's status configuration

### Task status doesn't change

**Symptoms:**
- Status API call succeeds but status in ClickUp unchanged

**Solutions:**
1. Verify status is transitionally valid (workflow rules)
2. Check task permissions (may be locked or archived)
3. Refresh ClickUp UI to see changes
4. Check if task is on a different list than expected

## Comment Issues

### Error: "Invalid comment text" or "400 Bad Request"

**Solutions:**
1. Ensure comment text is not empty:
   ```python
   assert len(comment_text) > 0
   ```

2. Use plain text (HTML tags are optional):
   ```python
   # Both work:
   client.add_comment(task_id, "Simple comment")
   client.add_comment(task_id, "<b>Bold</b> and <i>italic</i>")
   ```

3. Very long comments may fail — try breaking into smaller comments

### Comment not appearing

**Solutions:**
1. Check comment was added (verify response success)
2. Refresh ClickUp UI
3. If assigning via comment, verify assignee ID is valid

## Python Client Issues

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solutions:**
1. Install requests:
   ```bash
   pip install requests
   ```

2. Or use Hermes to install:
   ```
   /skill clickup
   > Can you install the requests library?
   ```

3. Check Python path:
   ```bash
   python3 -c "import requests"
   ```

### Error: "clickup_client.py not found"

**Solutions:**
1. Verify skill was installed:
   ```bash
   ls ~/.hermes/skills/productivity/clickup/
   ```

2. If missing, recreate skill:
   ```
   /skill clickup
   > Reinstall the ClickUp skill
   ```

3. Verify Python path:
   ```bash
   export PYTHONPATH="$PYTHONPATH:$HOME/.hermes/skills/productivity/clickup"
   ```

### Error: "CLICKUP_API_KEY not set"

**Solutions:**
1. Ensure `.env` file exists:
   ```bash
   cat ~/.hermes/.env | grep CLICKUP
   ```

2. Add if missing:
   ```bash
   echo "CLICKUP_API_KEY=pk_..." >> ~/.hermes/.env
   echo "CLICKUP_WORKSPACE_ID=1233538" >> ~/.hermes/.env
   ```

3. Restart Hermes session for changes to take effect

## Hermes Integration Issues

### Error: "/skill clickup" not recognized

**Solutions:**
1. Skill may not be loaded — verify it exists:
   ```bash
   hermes skills list | grep clickup
   ```

2. If not in list, reinstall:
   ```
   hermes skills install ~/.hermes/skills/productivity/clickup/SKILL.md --name clickup
   ```

3. Reload skills:
   ```
   /reload-skills
   ```

### Skill works in Python but not in Hermes chat

**Solutions:**
1. Load the skill explicitly:
   ```
   /skill clickup
   ```

2. Check toolsets are enabled:
   ```
   /toolsets
   ```
   Ensure `terminal` and `file` toolsets are enabled

3. New session might be needed:
   ```
   /new
   /skill clickup
   ```

### Long operations timeout

**Symptoms:**
- Creating many tasks → "timeout" error

**Solutions:**
1. Add delays between requests (see Rate Limiting section)
2. Increase Hermes timeout:
   ```
   /model [settings]
   max_turns: 200
   ```

3. Break into smaller batches:
   ```
   > Create first 5 tasks: [...]
   > Create next 5 tasks: [...]
   ```

## Debugging

### Enable verbose output

```bash
# In Python
import logging
logging.basicConfig(level=logging.DEBUG)

# In Hermes
/verbose
```

### Test API directly

```bash
# Get all tasks
curl https://api.clickup.com/api/v2/list/901234567/task \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" | jq .

# Create task
curl https://api.clickup.com/api/v2/list/901234567/task \
  -X POST \
  -H "Authorization: pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test task"}'
```

### Verify credentials work

```bash
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

Should show all team members.

### Print full error

```python
import traceback

try:
    client = ClickUpClient()
    task = client.create_task(...)
except Exception as e:
    traceback.print_exc()
    print(f"Error details: {e}")
```

## Performance Tips

1. **Batch operations:** Create 10 tasks at once (with delays) rather than asking 10 times
2. **Cache results:** Store team member IDs instead of querying every time
3. **Use pagination:** For large lists, use the API's page parameter
4. **Parallel workflows:** Use Hermes delegation for independent operations

## Still Having Issues?

1. **Check full documentation:** `SKILL.md` has complete API reference
2. **Review examples:** `examples.py` shows common patterns
3. **Test API directly:** Use curl to isolate ClickUp vs. Hermes issues
4. **Check ClickUp status:** Verify ClickUp isn't down
5. **Ask Hermes for help:**
   ```
   /skill clickup
   > I'm getting [error]. Help me debug.
   ```

## Quick Reference

| Issue | Check | Fix |
|-------|-------|-----|
| 401 Unauthorized | API key valid? | Regenerate token in ClickUp Settings |
| 404 Not Found | ID correct? | Get ID from ClickUp API or UI |
| 429 Too Many Requests | Rate limit hit? | Add delays between requests |
| Invalid status | Valid for workflow? | Get valid statuses: `get_list_statuses()` |
| File upload fails | File exists? Readable? | Use absolute path, check permissions |
| Comment not appearing | Posted successfully? | Refresh UI, check comment text not empty |
| ModuleNotFoundError | requests installed? | `pip install requests` |
| Skill not loading | Skill exists? | `hermes skills list` |
