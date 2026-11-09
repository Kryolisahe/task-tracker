import json
import os
import sys
from datetime import datetime

tasks_file="tasks.json"
statuses=("todo","in-progress","completed")

def now():
    return datetime.now().isoformat(timespec="seconds")

def save_tasks(tasks):
    tmp=tasks_file+".tmp"
    try:
        with open(tmp,"w",encoding="utf-8") as f:
            json.dump(tasks,f,indent=2,ensure_ascii=False)
        os.replace(tmp,tasks_file)
    except OSError as e:
        sys.exit(f"Unable to write {tasks_file}: {e}")
        
def load_tasks():
    #create file if it dosent exist
    if not os.path.exists(tasks_file):
        save_tasks([])
        return []
    try:
        with open(tasks_file,"r",encoding="utf-8") as f:
            content=f.read().strip()
            tasks=json.loads(content) if content else []
    except json.JSONDecodeError:
        sys.exit(f"{tasks_file} contains invalid json. fix or delete and retry")
    except OSError as e:
        sys.exit(f"could not read {tasks_file}: {e}")
    if not isinstance(tasks,list):
        sys.exit(f"{tasks_file} must contain a JSON list of tasks.")
    return tasks

def parse_id(value):
    """Convert a command-line argument to a positive integer ID."""
    try:
        task_id = int(value)
    except ValueError:
        sys.exit(f"Error: '{value}' is not a valid task ID (must be a number).")
    if task_id < 1:
        sys.exit("Error: task ID must be a positive number.")
    return task_id


def find_task(tasks, task_id):
    for task in tasks:
        if task.get("id") == task_id:
            return task
    sys.exit(f"Error: no task found with ID {task_id}.")


def clean_description(parts):
    """Join the arguments into one description and leave empty text."""
    description = " ".join(parts).strip()
    if not description:
        sys.exit("description cannot be empty.")
    return description

def cmd_add(args):
    if not args:
        sys.exit('Usage: task-cli add "<description>"')
    description = clean_description(args)
    tasks = load_tasks()
    new_id = max((t.get("id", 0) for t in tasks), default=0) + 1
    timestamp = now()
    tasks.append({
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp,
    })
    save_tasks(tasks)
    print(f"Task added perfectly (ID: {new_id})")
 
    
def cmd_list(args):
    if len(args) > 1:
        sys.exit("Usage: task-cli list [todo|in-progress|done]")
    status_filter = args[0] if args else None
    if status_filter and status_filter not in statuses:
        sys.exit(f"unknown status '{status_filter}'. Choose from: {', '.join(statuses)}.")

    tasks = load_tasks()
    if status_filter:
        tasks = [t for t in tasks if t.get("status") == status_filter]

    if not tasks:
        print("No tasks found" if not status_filter else f"No '{status_filter}' tasks found.")
        return

    for t in tasks:
        print(f"[{t['id']}] {t['description']}")
        print(f"     status: {t['status']} | created: {t['createdAt']} | updated: {t['updatedAt']}")

def cmd_update(args):
    if len(args) < 2:
        sys.exit('Usage: task-cli update <id> "<new description>"')
    task_id = parse_id(args[0])
    description = clean_description(args[1:])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    task["description"] = description
    task["updatedAt"] = now()
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully")

def cmd_delete(args):
    if len(args) != 1:
        sys.exit("Usage: task-cli delete <id>")
    task_id = parse_id(args[0])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully")


def cmd_mark_in_progress(args):
    if len(args) != 1:
        sys.exit("Usage: task-cli mark-in-progress <id>")
    task_id = parse_id(args[0])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    task["status"] = "in-progress"
    task["updatedAt"] = now()
    save_tasks(tasks)
    print(f"Task {task_id} marked as in-progress")


def cmd_mark_done(args):
    if len(args) != 1:
        sys.exit("Usage: task-cli mark-done <id>")
    task_id = parse_id(args[0])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    task["status"] = "done"
    task["updatedAt"] = now()
    save_tasks(tasks)
    print(f"Task {task_id} marked as done")


COMMANDS = {
    "add": cmd_add,
    "update": cmd_update,
    "delete": cmd_delete,
    "mark-in-progress": cmd_mark_in_progress,
    "mark-done": cmd_mark_done,
    
    "list": cmd_list,
    
}


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: task-cli <command> [arguments]")
    command, args = sys.argv[1], sys.argv[2:]
    handler = COMMANDS.get(command)
    if handler is None:
        sys.exit(f"Error: unknown command '{command}'.")
    handler(args)
