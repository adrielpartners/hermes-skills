# ClickUp Skill — Setup Checklist ✅

Use this checklist to verify your ClickUp skill is properly installed and configured.

## Installation Verification

- [ ] **Skill directory exists**
  ```bash
  ls -la ~/.hermes/skills/productivity/clickup/
  ```
  Should show 9 files (including this checklist)

- [ ] **All documentation files present**
  ```bash
  ls ~/.hermes/skills/productivity/clickup/*.md
  ```
  Should list: README.md, SKILL.md, QUICK_START.md, HERMES_INTEGRATION.md, 
  TROUBLESHOOTING.md, INDEX.md, SETUP_CHECKLIST.md

- [ ] **Python files present**
  ```bash
  ls ~/.hermes/skills/productivity/clickup/*.py
  ```
  Should list: clickup_client.py, examples.py

## Credential Configuration

- [ ] **Credentials file created**
  ```bash
  test -f ~/.hermes/.env.clickup && echo "✅ Found" || echo "❌ Missing"
  ```

- [ ] **API key set correctly**
  ```bash
  grep CLICKUP_API_KEY ~/.hermes/.env.clickup
  ```
  Should show: `CLICKUP_API_KEY=pk_1377633_...`

- [ ] **Workspace ID set correctly**
  ```bash
  grep CLICKUP_WORKSPACE_ID ~/.hermes/.env.clickup
  ```
  Should show: `CLICKUP_WORKSPACE_ID=1233538`

## API Connectivity

- [ ] **Python requests library installed**
  ```bash
  python3 -c "import requests; print('✅ OK')"
  ```

- [ ] **API connection works**
  ```bash
  python ~/.hermes/skills/productivity/clickup/clickup_client.py team
  ```
  Should list all 5 team members without errors

## Python Client Verification

- [ ] **Client module imports**
  ```bash
  python3 << 'PYEOF'
  import sys
  sys.path.insert(0, '/Users/max/.hermes/skills/productivity/clickup')
  from clickup_client import ClickUpClient
  print('✅ ClickUpClient imported successfully')
  PYEOF
  ```

## Hermes Integration

- [ ] **Skill loads in Hermes**
  ```bash
  hermes skills list | grep clickup
  ```
  Should show clickup skill

- [ ] **Can load with /skill command**
  (In Hermes chat):
  ```
  /skill clickup
  ```

## Documentation Validation

- [ ] **README is readable**
  ```bash
  head -1 ~/.hermes/skills/productivity/clickup/README.md
  ```

- [ ] **SKILL.md exists**
  ```bash
  test -f ~/.hermes/skills/productivity/clickup/SKILL.md && echo "✅"
  ```

## Quick Verification One-Liner

```bash
python3 << 'EOF'
import sys, os
sys.path.insert(0, '/Users/max/.hermes/skills/productivity/clickup')
os.environ.update({
    'CLICKUP_API_KEY': 'pk_1377633_NQ0FL1EXXJ6JTPV8YM407ENMP8OFFYZT',
    'CLICKUP_WORKSPACE_ID': '1233538'
})

from clickup_client import ClickUpClient
client = ClickUpClient()
members = client.get_team_members()
print(f"✅ ClickUp Skill Ready!")
print(f"   Workspace: ADRIEL PARTNERS")
print(f"   Team members: {len(members)}")
print(f"   Operations available: 20+")
EOF
```

Expected output:
```
✅ ClickUp Skill Ready!
   Workspace: ADRIEL PARTNERS
   Team members: 5
   Operations available: 20+
```

## Next Steps

1. **Read:** Start with `README.md`
2. **Try:** Run `QUICK_START.md` example
3. **Use:** Load `/skill clickup` in Hermes
4. **Integrate:** Follow `HERMES_INTEGRATION.md`

Your ClickUp skill is ready! 🚀
