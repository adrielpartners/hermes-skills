# ClickUp Skill — Complete Documentation Index

Your ClickUp skill is fully documented and ready to use. Here's where to find everything:

## 📚 Quick Navigation

| File | Purpose | Read Time |
|------|---------|-----------|
| [README.md](#readmemd) | Getting started & setup guide | 5 min |
| [QUICK_START.md](#quick_startmd) | Copy-paste examples & workflows | 5 min |
| [SKILL.md](#skillmd) | Complete API reference & documentation | 15 min |
| [HERMES_INTEGRATION.md](#hermes_integrationmd) | Using the skill in Hermes chat | 10 min |
| [TROUBLESHOOTING.md](#troubleshootingmd) | Common issues & solutions | 5 min |
| [examples.py](#examplespy) | Python code examples | 10 min |
| [clickup_client.py](#clickup_clientpy) | Python client library | Reference |

---

## README.md

**Start here!** Quick setup guide with:
- Credential setup instructions
- File overview
- Team member list
- Quick start commands
- 20 supported operations
- Next steps

**Read this first:** 5 minutes

---

## QUICK_START.md

Copy-paste examples for:
1. Creating tasks
2. Assigning to team members
3. Uploading files
4. Listing tasks
5. Adding comments
6. Creating list/folder structures
7. Finding IDs

**Use when:** You need working code examples fast

---

## SKILL.md

Complete skill documentation (12 KB):
- Full overview
- When to use / when not to use
- Complete setup instructions
- All 20+ operations with API examples
- Tasks, lists, folders, comments, attachments
- Team management
- Status management
- Common pitfalls & solutions
- Verification checklist
- API reference table

**Use when:** You need full context or working with unfamiliar APIs

---

## HERMES_INTEGRATION.md

How to use the skill inside Hermes Agent:
- Loading the skill (`/skill clickup`)
- Usage patterns & examples
- Combining with other skills
- Common commands
- Automation with cron jobs
- Session context & memory
- Advanced workflows

**Use when:** Working in Hermes chat or building automation

---

## TROUBLESHOOTING.md

Problem-solving guide with:
- API connection issues (401, 429, etc.)
- ID/reference problems
- Attachment issues
- Status & workflow issues
- Python client errors
- Hermes integration issues
- Debugging tips
- Performance optimization
- Quick reference table

**Use when:** Something doesn't work

---

## examples.py

8 realistic Python workflow examples:
1. Create weekly tasks
2. Assign tasks to team members
3. Bulk update status
4. Upload attachments in batch
5. Add comments with mentions
6. Duplicate list structures (templates)
7. Find overdue tasks
8. Create project from template

**Use when:** Building complex automations

---

## clickup_client.py

Python library (8 KB) with:
- `ClickUpClient` class
- 20+ methods for all operations
- Error handling
- Automatic credential loading
- Example CLI usage

**Use when:** Writing Python scripts or integrations

---

## Team Reference

**Your workspace:** ADRIEL PARTNERS (ID: 1233538)

**Team members:**
- Armando Pulgar (101207393) — armandopulgarb@gmail.com
- Noble Daniel (55307323) — thenobledaniel@gmail.com
- Isabella Amengual (3017021) — amengualisabella@gmail.com
- AB (54035174) — digital.b3asts@gmail.com
- Phillip Gonzales (1377633) — phillip@phillipgonzales.com [Owner]

---

## Common Scenarios

### Scenario 1: "I need to create a task in ClickUp"
→ Read: QUICK_START.md (section 1)
→ Reference: SKILL.md (Tasks section)
→ Example: examples.py (create_weekly_tasks)

### Scenario 2: "How do I use this in Hermes chat?"
→ Read: HERMES_INTEGRATION.md
→ Reference: QUICK_START.md

### Scenario 3: "Something's broken, what do I do?"
→ Read: TROUBLESHOOTING.md
→ Reference: SKILL.md (Common Pitfalls)

### Scenario 4: "I want to build automation"
→ Read: examples.py
→ Reference: HERMES_INTEGRATION.md (Cron section)
→ Library: clickup_client.py

### Scenario 5: "I want the full API reference"
→ Read: SKILL.md (complete)

---

## Using the Skill

### In Hermes Chat
```
/skill clickup

> Create a task called "Review design" and assign to Phillip
```

### In Python
```python
from clickup_client import ClickUpClient

client = ClickUpClient()
task = client.create_task(list_id="ABC123", name="My Task")
```

### Via Terminal
```bash
python ~/.hermes/skills/productivity/clickup/clickup_client.py team
```

### Automated (Cron)
```bash
hermes cron create "0 9 * * 1" -s clickup -q "Create this week's tasks"
```

---

## File Checklist

```
~/.hermes/skills/productivity/clickup/
  ✅ README.md              (5.5 KB)  — START HERE
  ✅ QUICK_START.md         (5.6 KB)  — Copy-paste examples
  ✅ SKILL.md               (12.2 KB) — Full documentation
  ✅ HERMES_INTEGRATION.md  (6.7 KB)  — Hermes usage
  ✅ TROUBLESHOOTING.md     (9.8 KB)  — Problem solving
  ✅ examples.py            (8.2 KB)  — Python examples
  ✅ clickup_client.py      (8.0 KB)  — Python library
  ✅ INDEX.md               (this file) — Documentation guide
```

**Total: 56.0 KB of documentation + code**

---

## Learning Path

**Beginner (15 min):**
1. README.md — Get oriented
2. QUICK_START.md — Try an example
3. Load skill: `/skill clickup`

**Intermediate (30 min):**
1. HERMES_INTEGRATION.md — Learn Hermes integration
2. SKILL.md (Tasks section) — Understand operations
3. TROUBLESHOOTING.md — Learn common issues

**Advanced (1 hour+):**
1. examples.py — Study 8 real workflows
2. clickup_client.py — Understand implementation
3. SKILL.md (full) — Master all operations
4. Build your own automation

---

## Quick Commands

```bash
# Test connectivity
python ~/.hermes/skills/productivity/clickup/clickup_client.py team

# View Python examples
cat ~/.hermes/skills/productivity/clickup/examples.py

# View full API docs
cat ~/.hermes/skills/productivity/clickup/SKILL.md

# Start Hermes with skill loaded
hermes -s clickup

# Load skill in session
# (in Hermes chat)
/skill clickup
```

---

## API Reference Quick Lookup

| Operation | File | Example |
|-----------|------|---------|
| Create task | SKILL.md (Tasks) | QUICK_START.md #1 |
| Get task | SKILL.md (Tasks) | examples.py |
| Update task | SKILL.md (Tasks) | QUICK_START.md #2 |
| List tasks | SKILL.md (Tasks) | examples.py |
| Delete task | SKILL.md (Tasks) | SKILL.md |
| Assign member | SKILL.md (Team) | QUICK_START.md #2 |
| Upload file | SKILL.md (Attachments) | QUICK_START.md #3 |
| Add comment | SKILL.md (Comments) | QUICK_START.md #5 |
| Get statuses | SKILL.md (Status) | examples.py |
| Set status | SKILL.md (Status) | examples.py |

---

## Next Steps

1. **First time?** → Start with README.md
2. **Need examples?** → Check QUICK_START.md
3. **Using in Hermes?** → Read HERMES_INTEGRATION.md
4. **Something broken?** → Look at TROUBLESHOOTING.md
5. **Ready to code?** → Use clickup_client.py + examples.py

---

**Your ClickUp skill is ready! 🚀**

Questions? Check the relevant documentation file above or ask Hermes:
```
/skill clickup
> How do I [your question]?
```
