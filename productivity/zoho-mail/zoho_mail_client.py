"""
Zoho Mail API Client for Hermes Agent

Handles OAuth authentication, draft management, and email operations.
Supports multiple Zoho Mail accounts.
"""

import os
import json
import yaml
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
from pathlib import Path


class ZohoMailClient:
    """Client for Zoho Mail API v2 with multi-account support"""

    BASE_URL = "https://mail.zoho.com/api"
    OAUTH_URL = "https://accounts.zoho.com/oauth/v2"
    
    def __init__(self, account: Optional[str] = None):
        """
        Initialize client for a specific account.
        
        Args:
            account: Account name (e.g., 'adriel', 'sitehub'). 
                    If None, uses default account from config.
        """
        self.config_file = Path(__file__).parent / "config.yaml"
        self.config = self._load_config()
        
        # Determine which account to use
        if account is None:
            account = self._get_default_account()
        
        self.account_name = account
        self.account_config = self.config.get("accounts", {}).get(account)
        
        if not self.account_config:
            raise ValueError(
                f"Account '{account}' not found. Available: {list(self.config.get('accounts', {}).keys())}"
            )
        
        # Get OAuth credentials
        oauth_config = self.config.get("oauth", {})
        self.client_id = os.getenv(
            "ZOHO_CLIENT_ID", 
            oauth_config.get("client_id", "").replace("${ZOHO_CLIENT_ID}", "")
        )
        self.client_secret = os.getenv(
            "ZOHO_CLIENT_SECRET",
            oauth_config.get("client_secret", "").replace("${ZOHO_CLIENT_SECRET}", "")
        )
        self.redirect_url = os.getenv(
            "ZOHO_REDIRECT_URL",
            oauth_config.get("redirect_url", "http://localhost:8080/callback")
        )
        
        # Get account-specific details
        self.email = self.account_config.get("email")
        self.account_id = self._resolve_env_var(self.account_config.get("account_id"))
        
        if not all([self.client_id, self.client_secret, self.account_id, self.email]):
            raise ValueError(
                f"Missing credentials for account '{account}'. "
                f"Check config.yaml and .env for ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, "
                f"and ZOHO_ACCOUNT_ID_{account.upper()}"
            )
        
        self.token = None
        self.token_expiry = None
        self._load_token()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load config.yaml"""
        if not self.config_file.exists():
            return {"accounts": {}, "oauth": {}}
        
        with open(self.config_file, "r") as f:
            config = yaml.safe_load(f) or {}
        
        # Resolve environment variables in config
        config = self._resolve_config_vars(config)
        return config
    
    def _resolve_config_vars(self, config: Dict) -> Dict:
        """Resolve ${VAR} placeholders in config"""
        import re
        
        def resolve_value(val):
            if isinstance(val, str):
                return re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), m.group(0)), val)
            elif isinstance(val, dict):
                return {k: resolve_value(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [resolve_value(v) for v in val]
            return val
        
        return resolve_value(config)
    
    def _resolve_env_var(self, value: str) -> Optional[str]:
        """Resolve a single environment variable reference"""
        if not value:
            return None
        
        import re
        match = re.match(r'\$\{([^}]+)\}', value)
        if match:
            return os.getenv(match.group(1))
        return value
    
    def _get_default_account(self) -> str:
        """Get default account name from config"""
        for name, config in self.config.get("accounts", {}).items():
            if config.get("default"):
                return name
        
        # If no default, return first account
        accounts = list(self.config.get("accounts", {}).keys())
        if accounts:
            return accounts[0]
        
        raise ValueError("No accounts configured in config.yaml")
    
    @staticmethod
    def list_accounts() -> List[Dict[str, str]]:
        """List all configured accounts"""
        config_file = Path(__file__).parent / "config.yaml"
        if not config_file.exists():
            return []
        
        with open(config_file, "r") as f:
            config = yaml.safe_load(f) or {}
        
        accounts_list = []
        for name, account_config in config.get("accounts", {}).items():
            accounts_list.append({
                "name": name,
                "email": account_config.get("email"),
                "description": account_config.get("description", ""),
                "default": account_config.get("default", False)
            })
        
        return accounts_list
    
    def _load_token(self) -> None:
        """Load OAuth token from ~/.hermes/auth.json"""
        auth_file = os.path.expanduser("~/.hermes/auth.json")
        if not os.path.exists(auth_file):
            return
        
        try:
            with open(auth_file, "r") as f:
                data = json.load(f)
                # Store tokens per account: zoho_mail.<account_name>
                account_key = f"zoho_mail_{self.account_name}"
                if account_key in data:
                    self.token = data[account_key].get("access_token")
                    expiry = data[account_key].get("expires_at")
                    if expiry:
                        self.token_expiry = datetime.fromisoformat(expiry)
        except (json.JSONDecodeError, IOError):
            pass
    
    def _save_token(self, token: str, expires_in: int) -> None:
        """Save OAuth token to ~/.hermes/auth.json"""
        auth_file = os.path.expanduser("~/.hermes/auth.json")
        os.makedirs(os.path.dirname(auth_file), exist_ok=True)
        
        data = {}
        if os.path.exists(auth_file):
            with open(auth_file, "r") as f:
                data = json.load(f)
        
        self.token = token
        self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
        
        # Store per account: zoho_mail_adriel, zoho_mail_sitehub, etc.
        account_key = f"zoho_mail_{self.account_name}"
        data[account_key] = {
            "access_token": token,
            "expires_at": self.token_expiry.isoformat(),
            "account": self.email
        }
        
        with open(auth_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def get_auth_url(self) -> str:
        """Generate OAuth authorization URL"""
        params = {
            "scope": "ZohoMail.accounts.ALL,ZohoMail.messages.ALL,ZohoMail.drafts.ALL",
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_url,
            "access_type": "offline"
        }
        return f"{self.OAUTH_URL}/auth?{urlencode(params)}"
    
    def authorize_with_code(self, auth_code: str) -> bool:
        """Exchange auth code for access token"""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_url,
            "code": auth_code
        }
        
        response = requests.post(f"{self.OAUTH_URL}/token", data=data)
        if response.status_code == 200:
            token_data = response.json()
            self._save_token(token_data["access_token"], token_data.get("expires_in", 3600))
            return True
        return False
    
    def _is_token_expired(self) -> bool:
        """Check if token is expired or about to expire"""
        if not self.token_expiry:
            return True
        return datetime.now() >= (self.token_expiry - timedelta(minutes=5))
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization"""
        if self._is_token_expired():
            raise RuntimeError(
                "OAuth token expired. Re-authorize: hermes -s zoho-mail chat -q 'verify'"
            )
        return {
            "Authorization": f"Zoho-oauthtoken {self.token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make API request"""
        url = f"{self.BASE_URL}/accounts/{self.account_id}{endpoint}"
        headers = self._get_headers()
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        if response.status_code == 401:
            raise RuntimeError("Unauthorized. Re-authorize: hermes -s zoho-mail chat -q 'verify'")
        
        response.raise_for_status()
        return response.json()
    
    # Draft Operations
    
    def create_draft(self, to: str, subject: str, body: str, 
                    cc: Optional[str] = None, bcc: Optional[str] = None,
                    attachments: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a draft email"""
        payload = {
            "fromAddress": self.get_account_email(),
            "toAddress": to,
            "subject": subject,
            "textBody": body,
            "ccAddress": cc or "",
            "bccAddress": bcc or ""
        }
        
        response = self._request("POST", "/drafts", json=payload)
        return response.get("data", response)
    
    def get_drafts(self, page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        """List all draft emails"""
        params = {
            "pageIndex": page,
            "limit": limit
        }
        
        response = self._request("GET", "/drafts", params=params)
        return response.get("data", [])
    
    def get_draft(self, draft_id: str) -> Dict[str, Any]:
        """Get details of a specific draft"""
        response = self._request("GET", f"/drafts/{draft_id}")
        return response.get("data", response)
    
    def update_draft(self, draft_id: str, **kwargs) -> Dict[str, Any]:
        """Update a draft email"""
        payload = {}
        
        if "to" in kwargs:
            payload["toAddress"] = kwargs["to"]
        if "subject" in kwargs:
            payload["subject"] = kwargs["subject"]
        if "body" in kwargs:
            payload["textBody"] = kwargs["body"]
        if "cc" in kwargs:
            payload["ccAddress"] = kwargs["cc"]
        if "bcc" in kwargs:
            payload["bccAddress"] = kwargs["bcc"]
        
        response = self._request("PUT", f"/drafts/{draft_id}", json=payload)
        return response.get("data", response)
    
    def send_draft(self, draft_id: str) -> Dict[str, Any]:
        """Send a draft email"""
        response = self._request("POST", f"/drafts/{draft_id}/send")
        return response.get("data", response)
    
    def delete_draft(self, draft_id: str) -> bool:
        """Delete a draft email"""
        self._request("DELETE", f"/drafts/{draft_id}")
        return True
    
    # Message Operations
    
    def send_email(self, to: str, subject: str, body: str,
                  cc: Optional[str] = None, bcc: Optional[str] = None) -> Dict[str, Any]:
        """Send email directly (not as draft)"""
        payload = {
            "fromAddress": self.get_account_email(),
            "toAddress": to,
            "subject": subject,
            "textBody": body,
            "ccAddress": cc or "",
            "bccAddress": bcc or ""
        }
        
        response = self._request("POST", "/messages/send", json=payload)
        return response.get("data", response)
    
    def get_messages(self, folder: str = "inbox", page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        """List messages from a folder"""
        params = {
            "folderId": self._get_folder_id(folder),
            "pageIndex": page,
            "limit": limit
        }
        
        response = self._request("GET", "/messages", params=params)
        return response.get("data", [])
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get message details"""
        response = self._request("GET", f"/messages/{message_id}")
        return response.get("data", response)
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        self._request("DELETE", f"/messages/{message_id}")
        return True
    
    def search_messages(self, query: str, page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        """Search messages"""
        params = {
            "searchKey": query,
            "pageIndex": page,
            "limit": limit
        }
        
        response = self._request("GET", "/messages/search", params=params)
        return response.get("data", [])
    
    # Folder Operations
    
    def get_folders(self) -> List[Dict[str, Any]]:
        """List all folders"""
        response = self._request("GET", "/folders")
        return response.get("data", [])
    
    def _get_folder_id(self, folder_name: str) -> str:
        """Get folder ID by name"""
        folders = self.get_folders()
        for folder in folders:
            if folder.get("displayName", "").lower() == folder_name.lower():
                return folder.get("folderId")
        
        # Return common folder IDs if not found
        folder_map = {
            "inbox": "INBOX",
            "sent": "SENT",
            "drafts": "DRAFTS",
            "trash": "TRASH",
            "spam": "SPAM"
        }
        return folder_map.get(folder_name.lower(), "INBOX")
    
    def create_folder(self, folder_name: str) -> Dict[str, Any]:
        """Create a custom folder"""
        payload = {"displayName": folder_name}
        response = self._request("POST", "/folders", json=payload)
        return response.get("data", response)
    
    def delete_folder(self, folder_id: str) -> bool:
        """Delete a folder"""
        self._request("DELETE", f"/folders/{folder_id}")
        return True
    
    # Account Operations
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        response = self._request("GET", "")
        return response.get("data", response)
    
    def get_account_email(self) -> str:
        """Get primary email address for account"""
        info = self.get_account_info()
        return info.get("emailAddress", "")


# Convenience functions for Hermes integration

def create_draft(to: str, subject: str, body: str, cc: str = "", bcc: str = "", account: str = None) -> str:
    """Create a draft and return draft ID"""
    client = ZohoMailClient(account)
    result = client.create_draft(to, subject, body, cc or None, bcc or None)
    draft_id = result.get("draftId") or result.get("id")
    return f"Draft created in {client.account_config.get('description', client.account_name)}\n\nID: {draft_id}\nTo: {to}\nSubject: {subject}"


def list_drafts(account: str = None) -> str:
    """List all drafts"""
    client = ZohoMailClient(account)
    drafts = client.get_drafts()
    
    if not drafts:
        return f"No drafts found in {client.account_config.get('description', client.account_name)}."
    
    output = f"=== Drafts ({client.email}) ===\n"
    for draft in drafts:
        output += f"\nID: {draft.get('draftId')}\n"
        output += f"To: {draft.get('toAddress')}\n"
        output += f"Subject: {draft.get('subject')}\n"
        output += f"Created: {draft.get('createdDate')}\n"
    
    return output


def send_draft(draft_id: str, account: str = None) -> str:
    """Send a draft"""
    client = ZohoMailClient(account)
    result = client.send_draft(draft_id)
    return f"Draft {draft_id} sent from {client.email}"


def delete_draft(draft_id: str, account: str = None) -> str:
    """Delete a draft"""
    client = ZohoMailClient(account)
    client.delete_draft(draft_id)
    return f"Draft {draft_id} deleted from {client.email}"


def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "", account: str = None) -> str:
    """Send email directly"""
    client = ZohoMailClient(account)
    result = client.send_email(to, subject, body, cc or None, bcc or None)
    return f"Email sent from {client.email} to {to}\nSubject: {subject}"


def list_accounts() -> str:
    """List all configured accounts"""
    accounts = ZohoMailClient.list_accounts()
    
    if not accounts:
        return "No accounts configured."
    
    output = "=== Zoho Mail Accounts ===\n"
    for account in accounts:
        marker = " (default)" if account["default"] else ""
        output += f"\n{account['name']}{marker}\n"
        output += f"  Email: {account['email']}\n"
        output += f"  {account['description']}\n"
    
    return output
