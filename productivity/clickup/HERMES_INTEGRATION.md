# Using ClickUp Skill with Hermes Agent

This guide shows how to use the ClickUp skill directly in Hermes chat sessions and automation.

## Load the Skill

### In Interactive Chat

```
/skill clickup
```

Or start a new session with it preloaded:

```bash
hermes -s clickup
```

### In Hermes Commands

```bash
# In chat
/skill clickup

# Or from terminal
hermes chat -s clickup
```

## Usage Patterns

### Pattern 1: Simple Queries

Ask Hermes directly:

> "What are all the team members in my ClickUp workspace?"

Hermes will use the skill's `get_team_members()` method and return:

```
- Armando Pulgar (armandopulgarb@gmail.com) [ID: 101207393]
- Noble Daniel (thenobledaniel@gmail.com) [ID: 55307323]
- Isabella Amengual (amengualisabella@gmail.com) [ID: 3017021]
- AB (digital.b3asts@gmail.com) [ID: 54035174]
- Phillip Gonzales (phillip@phillipgonzales.com) [ID: 1377633]
```

### Pattern 2: Create Task with Assignment

> "Create a task called 'Review Q1 roadmap' in my main list and assign it to Noble Daniel with high priority and due date next Friday"

Hermes will:
1. Use `get_member_by_username("Noble Daniel")` to find their ID
2. Calculate next Friday's due date
3. Call `create_task()` with all parameters
4. Return the created task ID

### Pattern 3: Bulk Operations

> "Get all incomplete tasks in list ABC123, then mark the ones assigned to me as completed"

Hermes will:
1. Call `list_tasks()`
2. Filter by your user ID
3. Call `update_task()` for each to set status to "completed"

### Pattern 4: File Upload

> "Upload the file /path/to/design.pdf to task XYZ789"

Hermes will:
1. Verify the file exists
2. Call `upload_attachment()`
3. Confirm successful upload

### Pattern 5: Workflow Automation

> "For all tasks in the 'In Review' status, add a comment saying 'Ready for testing!' and move them to 'In Progress'"

Hermes will:
1. List tasks in the list
2. Filter by status "In Review"
3. Add comment to each
4. Update status to "In Progress"

## Advanced: Combining with Other Skills

Use ClickUp skill with other Hermes capabilities:

### With Terminal Skills

```
Let me create a ClickUp task for each failing test in my CI pipeline.
[Hermes analyzes test output, creates tasks, assigns to developers]
```

### With Memory

```
/skill clickup

Remember: my main project list ID is ABC123, my folder is XYZ789, 
and I usually assign urgent tasks to Phillip Gonzales.

Now whenever I mention "my list", use ABC123.
When I say "urgent work", assign to Phillip (ID: 1377633).
```

### With Delegation

Spawn a subagent to handle ClickUp work while you do other tasks:

```python
delegate_task(
    goal="Create weekly team tasks in ClickUp for Q2 planning",
    context="List ID: ABC123. Create 7 tasks: one for each team member's weekly standup. Assign each to their respective member.",
    toolsets=["terminal"]  # The subagent will have access to ClickUp client via terminal
)
```

## Common Commands

### Get Your IDs

```
/skill clickup

What's my workspace ID and how do I find my list IDs?
```

Hermes responds with:
```
Workspace ID: 1233538

To find list IDs:
1. ClickUp UI: Copy from URL (the number in the address bar)
2. API: curl https://api.clickup.com/api/v2/folder/{folder_id}/list \
         -H "Authorization: pk_..."
```

### Check Team Status

```
Show me all tasks assigned to Isabella Amengual that are in 'In Progress' status.
```

Hermes will:
1. Find Isabella's user ID (3017021)
2. List tasks in your main list
3. Filter by assignee and status
4. Display them in a table

### Bulk Create from Template

```
I have a template of 5 tasks for client onboarding. Create them in a new list called 'ACME Corp Setup'.

The tasks are:
- Kickoff call
- Requirements gathering
- Design phase
- Development
- QA and launch
```

Hermes will:
1. Create the list
2. Create all 5 tasks with their names
3. Return the new list ID for future reference

### Report Generation

```
Give me a summary of my project:
- Total tasks in list ABC123
- How many are overdue
- Breakdown by status
- Who has the most assigned tasks
```

Hermes will query the list and return a formatted report.

## Troubleshooting in Chat

### "Authorization failed"

```
/skill clickup

Why can't I connect to ClickUp?
```

Check:
- `CLICKUP_API_KEY` in `~/.hermes/.env`
- API key hasn't been revoked
- Workspace ID is correct

### "Invalid list ID"

```
/skill clickup

I keep getting "invalid list ID" errors. How do I find the correct ID?
```

Hermes will explain where to find it and offer to help you look it up.

### Python Error

```
I'm getting an import error when using the ClickUp skill.
```

Hermes will check dependencies and suggest fixes.

## Automation with Cron

Schedule recurring ClickUp tasks:

```bash
hermes cron create "0 9 * * 1"  # Every Monday at 9 AM
Prompt: "Create this week's team tasks and assign them using the ClickUp skill"
Skills: clickup
```

## Session Context

The skill persists across turns in a session, so you can:

1. Load the skill once: `/skill clickup`
2. Ask multiple questions without reloading
3. Hermes remembers previous task IDs and context
4. Build complex workflows across multiple messages

## Tips & Tricks

### Tip 1: Save Your IDs

When you find your list/folder IDs, ask Hermes to remember them:

```
Remember: my main project list is ABC123 and my designs folder is XYZ789.
```

Hermes stores this in session memory.

### Tip 2: Create Aliases

```
When I say "my main list", always use list ID ABC123.
When I say "urgent", set priority to 2 and assign to Phillip (1377633).
```

### Tip 3: Batch Operations

Instead of asking for one task at a time:

```
Create these 5 tasks in my list:
1. Feature spec - high priority - due Friday - assign to Phillip
2. UI mockups - high priority - due Friday - assign to Isabella
...
```

Hermes will create all in one go.

### Tip 4: Combine with File Tools

```
Read the file design-feedback.md, then create a ClickUp task for each TODO item.
```

Hermes can parse files and create tasks in batch.

## Full Example Workflow

```
> /skill clickup

> Create a new project folder called "Q2 2025 Launch"
Created folder XYZ789

> Create a list called "Product" in that folder
Created list ABC123

> Create these tasks:
> - Technical architecture (high priority, assign to Phillip)
> - Design system (high priority, assign to Isabella)
> - Frontend components (normal priority, assign to Noble)
[3 tasks created]

> Upload the design-system-spec.pdf to the 'Design system' task
File uploaded successfully

> Add a comment on the architecture task: "Review PostgreSQL schema from the database-design.md file"
Comment added

> List all tasks in the Product list
[Shows all 3 tasks with statuses and assignees]
```

## See Also

- `SKILL.md` — Full API reference
- `QUICK_START.md` — Copy-paste examples
- `examples.py` — Advanced Python patterns
- `clickup_client.py` — Python client source
