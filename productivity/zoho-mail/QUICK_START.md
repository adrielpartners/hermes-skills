# Zoho Mail Skill — Quick Start

## Setup (5 minutes)

1. **Get OAuth credentials:**
   - Go to [Zoho API Console](https://api-console.zoho.com)
   - Create OAuth client (Self Client)
   - Copy Client ID and Client Secret

2. **Add to `.env`:**
   ```bash
   echo 'ZOHO_CLIENT_ID=your_id' >> ~/.hermes/.env
   echo 'ZOHO_CLIENT_SECRET=your_secret' >> ~/.hermes/.env
   echo 'ZOHO_ACCOUNT_ID=your_account_id' >> ~/.hermes/.env
   ```

3. **Authorize:**
   ```bash
   hermes -s zoho-mail chat -q "verify my email"
   # Follow browser prompt
   ```

## Common Tasks

### Create and Save Draft

```bash
hermes chat -q "
Create a draft email:
- To: client@example.com
- Subject: Project Update
- Body: Please review the attached proposal and let me know your thoughts.
"
```

### List All Drafts

```bash
hermes chat -q "List my draft emails"
```

### Send a Draft

```bash
# After listing drafts, copy the draft ID
hermes chat -q "Send draft DRAFT_ID_HERE"
```

### Send Email Directly

```bash
hermes chat -q "
Send email to contact@example.com
Subject: Quick Question
Body: Do you have availability for a call this week?
"
```

## Examples

### Example 1: Compose Draft for Team Review

```bash
hermes chat -q "
Create draft to: team@company.com
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
```

Then later:
```bash
hermes chat -q "Send draft DRAFT_ID"
```

### Example 2: Batch Create Drafts for Review

```bash
hermes chat -q "
Create multiple draft emails:

1. To: alice@company.com
   Subject: Project Alpha - Status Update
   Body: Alice, can you provide a status on Project Alpha? We need metrics by Friday.

2. To: bob@company.com
   Subject: Resource Request
   Body: Bob, we need additional design resources for Q2. Can we schedule a meeting?

3. To: charlie@company.com
   Subject: Contract Review
   Body: Charlie, please review the attached vendor contract.
"
```

Then review all drafts:
```bash
hermes chat -q "List my drafts"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unauthorized" | Run authorization: `hermes -s zoho-mail chat -q "verify"` |
| "Account ID not found" | Check ZOHO_ACCOUNT_ID in ~/.hermes/.env |
| Draft not saving | Verify To, Subject, and Body are non-empty |
| Token expired | Re-authorize (happens automatically) |

## Next Steps

- Push to GitHub: `update-skill-github zoho-mail productivity`
- Share with team: Have them add tap and install skill
- Integrate with ClickUp: Use drafts to compose task comments
- Automate workflows: Use with cron jobs for scheduled emails
