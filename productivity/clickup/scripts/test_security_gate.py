#!/usr/bin/env python3
"""
ClickUp API Terminal Security Gate Test

Verifies that the ClickUp API can be called from the terminal without
security gate blockage. Run this after updating ~/.hermes/config.yaml
with the approved_api_domains whitelist.

Usage:
  python3 ~/.hermes/skills/productivity/clickup/scripts/test_security_gate.py

Exit codes:
  0 = API call succeeded (security gate removed or config properly whitelisted)
  1 = API call blocked (config needs update)
  2 = Network error (connectivity issue)
  3 = API error (credentials issue)
"""

import sys
import os

sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))

def test_api_call():
    """Test if ClickUpClient can make API calls from terminal."""
    print("=" * 60)
    print("ClickUp API Security Gate Test")
    print("=" * 60)
    
    # Check credentials
    api_key = os.getenv('CLICKUP_API_KEY')
    workspace_id = os.getenv('CLICKUP_WORKSPACE_ID')
    
    if not api_key or not workspace_id:
        print("\n❌ Credentials not set:")
        print(f"   CLICKUP_API_KEY: {'✓' if api_key else '✗'}")
        print(f"   CLICKUP_WORKSPACE_ID: {'✓' if workspace_id else '✗'}")
        print("\nSet them in ~/.hermes/.env or pass as env vars:")
        print("  export CLICKUP_API_KEY='pk_...'")
        print("  export CLICKUP_WORKSPACE_ID='1233538'")
        return 3
    
    print("\n✓ Credentials loaded")
    
    try:
        from clickup_client import ClickUpClient
        print("✓ ClickUpClient imported")
        
        client = ClickUpClient()
        print("✓ ClickUpClient initialized")
        
        # Try to get chats
        print("\nCalling API: get_chats()...")
        chats = client.get_chats()
        
        print(f"✓ API call succeeded!")
        print(f"✓ Found {len(chats)} chat(s)\n")
        
        print("=" * 60)
        print("✅ Security gate is NOT blocking Python API calls")
        print("=" * 60)
        print("\nYour ClickUp skill is ready to use from terminal!")
        print("Try: hermes -s clickup -q 'Show me my ClickUp chats'")
        
        return 0
        
    except Exception as e:
        error_str = str(e)
        
        if "BLOCKED" in error_str or "User denied" in error_str:
            print(f"\n❌ API call blocked by security gate:")
            print(f"   {error_str}")
            print("\nSolution: Update ~/.hermes/config.yaml")
            print("See: references/terminal-api-security.md")
            print("\nQuick fix:")
            print("  1. Edit ~/.hermes/config.yaml")
            print("  2. Find: security:")
            print("  3. Add:")
            print("       approved_api_domains:")
            print("         - api.clickup.com")
            print("         - '*.clickup.com'")
            print("  4. Restart Hermes")
            return 1
            
        elif "Unauthorized" in error_str or "401" in error_str:
            print(f"\n❌ API authentication failed:")
            print(f"   {error_str}")
            print("\nYour credentials may be invalid or revoked.")
            print("Check in ClickUp: Settings → API → Verify token")
            return 3
            
        elif "Connection" in error_str or "Network" in error_str:
            print(f"\n❌ Network error:")
            print(f"   {error_str}")
            print("\nCheck your internet connection.")
            return 2
            
        else:
            print(f"\n❌ Unexpected error:")
            print(f"   {error_str}")
            import traceback
            traceback.print_exc()
            return 3

if __name__ == "__main__":
    exit_code = test_api_call()
    sys.exit(exit_code)
