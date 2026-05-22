#!/usr/bin/env python3
"""
ClickUp API utility for Hermes Agent.
Wraps common ClickUp operations with error handling and convenience methods.
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class ClickUpClient:
    """Client for interacting with ClickUp API v2."""
    
    def __init__(self, api_key: Optional[str] = None, workspace_id: Optional[str] = None):
        """
        Initialize ClickUp client.
        
        Args:
            api_key: ClickUp API key (defaults to CLICKUP_API_KEY env var)
            workspace_id: ClickUp workspace/team ID (defaults to CLICKUP_WORKSPACE_ID env var)
        """
        self.api_key = api_key or os.getenv("CLICKUP_API_KEY")
        self.workspace_id = workspace_id or os.getenv("CLICKUP_WORKSPACE_ID")
        self.base_url = "https://api.clickup.com/api/v2"
        
        if not self.api_key:
            raise ValueError("CLICKUP_API_KEY not set")
        if not self.workspace_id:
            raise ValueError("CLICKUP_WORKSPACE_ID not set")
        
        self.headers = {"Authorization": self.api_key}
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request to ClickUp API."""
        url = f"{self.base_url}{endpoint}"
        headers = {**self.headers, **kwargs.pop("headers", {})}
        
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        
        return response.json()
    
    # Task operations
    
    def create_task(
        self,
        list_id: str,
        name: str,
        description: Optional[str] = None,
        assignees: Optional[List[int]] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
    ) -> Dict:
        """Create a new task."""
        payload = {"name": name}
        if description:
            payload["description"] = description
        if assignees:
            payload["assignees"] = assignees
        if status:
            payload["status"] = status
        if priority:
            payload["priority"] = priority
        if due_date:
            payload["due_date"] = due_date
        
        return self._request("POST", f"/list/{list_id}/task", json=payload)
    
    def get_task(self, task_id: str, include_subtasks: bool = False) -> Dict:
        """Get task details."""
        params = {}
        if include_subtasks:
            params["include_subtasks"] = "true"
        
        return self._request("GET", f"/task/{task_id}", params=params)
    
    def update_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,
        assignees_add: Optional[List[int]] = None,
        assignees_remove: Optional[List[int]] = None,
    ) -> Dict:
        """Update a task."""
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if status:
            payload["status"] = status
        if priority:
            payload["priority"] = priority
        if due_date:
            payload["due_date"] = due_date
        
        if assignees_add or assignees_remove:
            payload["assignees"] = {}
            if assignees_add:
                payload["assignees"]["add"] = assignees_add
            if assignees_remove:
                payload["assignees"]["rem"] = assignees_remove
        
        return self._request("PUT", f"/task/{task_id}", json=payload)
    
    def list_tasks(self, list_id: str, page: int = 0) -> Dict:
        """List tasks in a list."""
        return self._request("GET", f"/list/{list_id}/task", params={"page": page})
    
    def delete_task(self, task_id: str) -> None:
        """Delete a task."""
        self._request("DELETE", f"/task/{task_id}")
    
    # List operations
    
    def create_list(self, folder_id: str, name: str) -> Dict:
        """Create a new list in a folder."""
        return self._request("POST", f"/folder/{folder_id}/list", json={"name": name})
    
    def get_lists(self, folder_id: str) -> Dict:
        """Get lists in a folder."""
        return self._request("GET", f"/folder/{folder_id}/list")
    
    def delete_list(self, list_id: str) -> None:
        """Delete a list."""
        self._request("DELETE", f"/list/{list_id}")
    
    # Folder operations
    
    def create_folder(self, space_id: str, name: str) -> Dict:
        """Create a new folder in a space."""
        return self._request("POST", f"/space/{space_id}/folder", json={"name": name})
    
    def get_folders(self, space_id: str) -> Dict:
        """Get folders in a space."""
        return self._request("GET", f"/space/{space_id}/folder")
    
    def delete_folder(self, folder_id: str) -> None:
        """Delete a folder."""
        self._request("DELETE", f"/folder/{folder_id}")
    
    # Comment operations
    
    def add_comment(
        self,
        task_id: str,
        text: str,
        assignee: Optional[int] = None,
    ) -> Dict:
        """Add a comment to a task."""
        payload = {"comment_text": text}
        if assignee:
            payload["assignee"] = assignee
        
        return self._request("POST", f"/task/{task_id}/comment", json=payload)
    
    def get_comments(self, task_id: str) -> Dict:
        """Get comments on a task."""
        return self._request("GET", f"/task/{task_id}/comment")
    
    # Attachment operations
    
    def upload_attachment(self, task_id: str, file_path: str) -> Dict:
        """Upload a file to a task."""
        with open(file_path, "rb") as f:
            files = {"attachment": f}
            return self._request("POST", f"/task/{task_id}/attachment", files=files)
    
    def get_task_attachments(self, task_id: str) -> List[Dict]:
        """Get attachments for a task."""
        task = self.get_task(task_id)
        return task.get("task", {}).get("attachments", [])
    
    # Team/member operations
    
    def get_team_members(self) -> List[Dict]:
        """Get all team members in workspace."""
        result = self._request("GET", f"/team/{self.workspace_id}")
        return result.get("team", {}).get("members", [])
    
    def get_member_by_email(self, email: str) -> Optional[Dict]:
        """Find team member by email."""
        members = self.get_team_members()
        for member in members:
            if member.get("user", {}).get("email") == email:
                return member
        return None
    
    def get_member_by_username(self, username: str) -> Optional[Dict]:
        """Find team member by username."""
        members = self.get_team_members()
        for member in members:
            if member.get("user", {}).get("username") == username:
                return member
        return None
    
    # Status operations
    
    def get_list_statuses(self, list_id: str) -> List[Dict]:
        """Get available statuses for a list."""
        result = self._request("GET", f"/list/{list_id}")
        return result.get("list", {}).get("statuses", [])
    
    def set_task_status(self, task_id: str, status: str) -> Dict:
        """Set task status."""
        return self.update_task(task_id, status=status)
    
    # Chat operations
    
    def get_chats(self) -> List[Dict]:
        """Get all chats in the workspace."""
        result = self._request("GET", f"/team/{self.workspace_id}/chat")
        return result.get("chats", [])
    
    def get_chat_messages(self, chat_id: str, limit: int = 50) -> List[Dict]:
        """Get messages from a chat.
        
        Args:
            chat_id: The chat ID
            limit: Max messages to fetch (default 50)
        
        Returns:
            List of messages with id, user, content, created_at
        """
        result = self._request("GET", f"/chat/{chat_id}/message", params={"limit": limit})
        return result.get("messages", [])
    
    def send_message(self, chat_id: str, text: str) -> Dict:
        """Send a message to a chat.
        
        Args:
            chat_id: The chat ID
            text: Message text (plain text or markdown)
        
        Returns:
            Message object with id, user, content, created_at
        """
        payload = {"content": text}
        return self._request("POST", f"/chat/{chat_id}/message", json=payload)
    
    def get_chat_by_name(self, chat_name: str) -> Optional[Dict]:
        """Find a chat by name.
        
        Args:
            chat_name: Name of the chat to find
        
        Returns:
            Chat object or None if not found
        """
        chats = self.get_chats()
        for chat in chats:
            if chat.get("name") == chat_name or chat.get("title") == chat_name:
                return chat
        return None


# CLI convenience function
if __name__ == "__main__":
    import sys
    
    try:
        client = ClickUpClient()
        
        # Example: List team members
        if len(sys.argv) > 1 and sys.argv[1] == "team":
            members = client.get_team_members()
            print(json.dumps(
                [
                    {
                        "id": m["user"]["id"],
                        "username": m["user"]["username"],
                        "email": m["user"]["email"],
                    }
                    for m in members
                ],
                indent=2
            ))
        else:
            print("Usage: python clickup_client.py team")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
