#!/usr/bin/env python3
"""
ClickUp Skill Examples — Common patterns and workflows.

These examples show how to use the ClickUp skill for real-world scenarios.
"""

import os
import sys
from datetime import datetime, timedelta

# Add skill to path
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/clickup"))
from clickup_client import ClickUpClient


def example_1_create_weekly_tasks():
    """Example 1: Create a set of weekly tasks for a project."""
    client = ClickUpClient()
    
    # You'll need to get your list_id first
    list_id = "YOUR_LIST_ID"  # Replace with actual list ID
    
    weekly_tasks = [
        {"name": "Client standup", "priority": 3},
        {"name": "Feature review", "priority": 2},
        {"name": "Documentation update", "priority": 4},
        {"name": "Code review", "priority": 2},
    ]
    
    print("Creating weekly tasks...")
    for task_data in weekly_tasks:
        task = client.create_task(
            list_id=list_id,
            name=task_data["name"],
            priority=task_data["priority"],
            status="to_do",
            due_date=int((datetime.now() + timedelta(days=7)).timestamp() * 1000),
        )
        print(f"  ✓ Created: {task['task']['name']}")


def example_2_assign_to_team():
    """Example 2: Assign tasks to different team members."""
    client = ClickUpClient()
    
    # Get team members
    members = client.get_team_members()
    member_map = {
        m["user"]["username"]: m["user"]["id"]
        for m in members
    }
    
    assignments = [
        ("ABC123", "Phillip Gonzales"),  # (task_id, username)
        ("ABC124", "Noble Daniel"),
        ("ABC125", "Isabella Amengual"),
    ]
    
    print("Assigning tasks to team members...")
    for task_id, username in assignments:
        if username in member_map:
            client.update_task(
                task_id=task_id,
                assignees_add=[member_map[username]]
            )
            print(f"  ✓ Assigned {task_id} to {username}")
        else:
            print(f"  ✗ {username} not found")


def example_3_bulk_update_status():
    """Example 3: Mark multiple tasks as completed."""
    client = ClickUpClient()
    
    list_id = "YOUR_LIST_ID"  # Replace with actual list ID
    
    # Get all tasks
    response = client.list_tasks(list_id=list_id)
    tasks = response.get("tasks", [])
    
    # Filter for tasks that are "in_progress"
    in_progress_tasks = [
        t for t in tasks
        if t.get("status", {}).get("status") == "in_progress"
    ]
    
    print(f"Found {len(in_progress_tasks)} in-progress tasks. Marking as completed...")
    for task in in_progress_tasks:
        client.set_task_status(task["id"], "completed")
        print(f"  ✓ {task['name']} → completed")


def example_4_add_attachments_from_directory():
    """Example 4: Upload all files from a directory to a task."""
    client = ClickUpClient()
    
    task_id = "ABC123"
    directory = "/path/to/files"  # Replace with actual path
    
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return
    
    print(f"Uploading files from {directory}...")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            client.upload_attachment(task_id=task_id, file_path=filepath)
            print(f"  ✓ Uploaded: {filename}")


def example_5_comment_with_mentions():
    """Example 5: Add a comment mentioning a team member."""
    client = ClickUpClient()
    
    task_id = "ABC123"
    
    # Find a team member
    member = client.get_member_by_username("Phillip Gonzales")
    if member:
        client.add_comment(
            task_id=task_id,
            text=f"This is ready for review! @{member['user']['username']}",
            assignee=member["user"]["id"]
        )
        print(f"✓ Comment added and assigned to {member['user']['username']}")


def example_6_duplicate_list_structure():
    """Example 6: Create a duplicate list with same tasks (template)."""
    client = ClickUpClient()
    
    source_list_id = "SOURCE_LIST_ID"
    target_folder_id = "TARGET_FOLDER_ID"
    new_list_name = "Q2 2025 Plan"
    
    # Get all tasks from source list
    source_response = client.list_tasks(list_id=source_list_id)
    source_tasks = source_response.get("tasks", [])
    
    # Create new list
    new_list = client.create_list(
        folder_id=target_folder_id,
        name=new_list_name
    )
    new_list_id = new_list["list"]["id"]
    print(f"Created list: {new_list_name} (ID: {new_list_id})")
    
    # Create tasks in new list
    for task in source_tasks:
        client.create_task(
            list_id=new_list_id,
            name=task["name"],
            description=task.get("description", ""),
            status="to_do"
        )
        print(f"  ✓ Created: {task['name']}")


def example_7_get_overdue_tasks():
    """Example 7: Find all overdue tasks in a list."""
    client = ClickUpClient()
    
    list_id = "YOUR_LIST_ID"  # Replace with actual list ID
    now = datetime.now().timestamp() * 1000  # Convert to milliseconds
    
    response = client.list_tasks(list_id=list_id)
    tasks = response.get("tasks", [])
    
    overdue = [
        t for t in tasks
        if t.get("due_date") and int(t.get("due_date", 0)) < now
        and t.get("status", {}).get("status") != "completed"
    ]
    
    if overdue:
        print(f"Found {len(overdue)} overdue tasks:")
        for task in overdue:
            due_date = datetime.fromtimestamp(int(task["due_date"]) / 1000)
            assignee = (
                task["assignees"][0]["username"]
                if task.get("assignees")
                else "Unassigned"
            )
            print(f"  - {task['name']} (due: {due_date.strftime('%Y-%m-%d')}) → {assignee}")
    else:
        print("No overdue tasks found!")


def example_8_create_from_template():
    """Example 8: Create a new project from a template."""
    client = ClickUpClient()
    
    space_id = "YOUR_SPACE_ID"  # Replace with actual space ID
    
    template = {
        "project_name": "New Client Onboarding",
        "folder_name": "Q1 2025",
        "lists": [
            {
                "name": "Discovery",
                "tasks": [
                    "Schedule kickoff call",
                    "Gather requirements",
                    "Define scope",
                ]
            },
            {
                "name": "Design",
                "tasks": [
                    "Create wireframes",
                    "Design mockups",
                    "Get approval",
                ]
            },
            {
                "name": "Development",
                "tasks": [
                    "Backend API",
                    "Frontend implementation",
                    "Testing",
                ]
            }
        ]
    }
    
    # Create folder
    folder = client.create_folder(
        space_id=space_id,
        name=template["folder_name"]
    )
    folder_id = folder["folder"]["id"]
    print(f"Created folder: {template['folder_name']}")
    
    # Create lists and tasks
    for list_config in template["lists"]:
        new_list = client.create_list(
            folder_id=folder_id,
            name=list_config["name"]
        )
        list_id = new_list["list"]["id"]
        print(f"  ✓ Created list: {list_config['name']}")
        
        for task_name in list_config["tasks"]:
            client.create_task(
                list_id=list_id,
                name=task_name,
                status="to_do"
            )
            print(f"    ✓ Created task: {task_name}")


if __name__ == "__main__":
    print("ClickUp Skill Examples")
    print("=" * 50)
    print("\nAvailable examples:")
    print("  1. Create weekly tasks")
    print("  2. Assign tasks to team members")
    print("  3. Bulk update task status")
    print("  4. Upload files from directory")
    print("  5. Add comments with mentions")
    print("  6. Duplicate list structure")
    print("  7. Get overdue tasks")
    print("  8. Create project from template")
    print("\nTo run: python examples.py [number]")
    print("\nNote: Update list_id, task_id, and other IDs with actual values!")
