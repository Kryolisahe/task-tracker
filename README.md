# Task Tracker CLI

A simple command line app to track what you need to do, what you're working on, and what's done. Written in Python 3 using only the standard library (no external packages). Tasks are stored in a `tasks.json` file in the folder you run the program from. The file is created automatically if it doesn't exist.

## Requirements

- Python 3.6 or newer

## Getting started

```bash
git clone https://github.com/Kryolisahe/task-tracker.git
cd task-tracker
python task.py add "Buy groceries"
```

On some systems (Mac/Linux) you may need `python3` instead of `python`.

## Usage

### Add a task

```bash
python task.py add "Buy groceries"
# Task added successfully (ID: 1)
```

### Update a task

```bash
python task.py update 1 "Buy groceries and cook dinner"
# Task 1 updated successfully
```

### Delete a task

```bash
python task.py delete 1
# Task 1 deleted successfully
```

### Change a task's status

```bash
python task.py mark-in-progress 1
# Task 1 marked as in-progress

python task.py mark-done 1
# Task 1 marked as done
```

### List tasks

```bash
python task.py list               # all tasks
python task.py list todo          # tasks not started
python task.py list in-progress   # tasks being worked on
python task.py list done          # completed tasks
```

Example output:

```
[1] Buy groceries and cook dinner
     status: in-progress | created: 2026-11-09T10:30:00 | updated: 2026-11-09T11:05:00
```

> **Tip:** wrap descriptions in double quotes. On Windows cmd, use double quotes (`"..."`), not single quotes.

## Commands at a glance

| Command | Description |
|---|---|
| `add <description>` | Add a new task (starts as `todo`) |
| `update <id> <description>` | Change a task's description |
| `delete <id>` | Remove a task |
| `mark-in-progress <id>` | Set status to `in-progress` |
| `mark-done <id>` | Set status to `done` |
| `list [status]` | Show all tasks, or only `todo`, `in-progress` or `done` |

## Task format

Each task in `tasks.json` has these properties:

```json
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2026-11-09T10:30:00",
  "updatedAt": "2026-11-09T10:30:00"
}
```

| Field | Meaning |
|---|---|
| `id` | Unique number for the task |
| `description` | Short text describing the task |
| `status` | `todo`, `in-progress` or `done` |
| `createdAt` | When the task was created |
| `updatedAt` | When it was last changed (updated on every edit or status change) |

## Error handling

The program prints a clear message and exits with a non-zero code when:

- the command is unknown or arguments are missing
- an ID is not a number, or no task has that ID
- a description is empty
- a status filter is not `todo`, `in-progress` or `done`
- `tasks.json` is unreadable or contains invalid JSON

## Notes and limitations

- A new task gets the ID `max(existing IDs) + 1`. If you delete the highest-numbered task, that ID can be reused.
- There is no file locking, so don't run several commands at the same moment.
