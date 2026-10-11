# cat > README.md << 'EOF'
# CampusFlow

CampusFlow is a command-line helpdesk app for Learn2Earn campus staff. Support requests (Wi-Fi outages, faulty laptops, broken development environments) often get lost when they are reported informally. CampusFlow records each problem as a ticket, calculates its priority, assigns it to a staff member, and tracks it until it is resolved.

## Team

| Fellow | Role | What they built |
|---|---|---|
| <Your name> | Engineer A | Ticket creation, input validation, priority engine, JSON storage, main menu, and their tests |
| <Partner's name> | Engineer B | Assignment, status workflow, work queue, reports, and their tests |

## Setup

- Python 3.8 or newer
- No extra packages are needed. The project uses only the standard library.

```bash
git clone https://github.com/Mrisaiahjesse/CampusFlow.git
cd CampusFlow
```

## Run the app

```bash
python3 main.py
```

## Menu options

| Option | What it does |
|---|---|
| 1 | Create a ticket |
| 2 | List all tickets |
| 3 | View one ticket |
| 4 | Assign a ticket to a staff member |
| 5 | Change a ticket's status |
| 6 | Show the work queue |
| 7 | Show the report |
| 0 | Exit |

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The tests cover:

- Priority rules and their boundaries
- Rejecting invalid input (blank title, bad category, bad urgency, zero or negative affected users)
- Unique ticket IDs, including after a reload
- Saving and loading JSON, a missing file, and a corrupted file
- Assignment, status changes, the work queue order, and the report

## Ticket rules

### Fields

Each ticket has: `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.

- **Category:** Network, Hardware, Software, or Other
- **Urgency:** low, medium, or high
- **Affected users:** a positive whole number
- **IDs** are generated automatically: T001, T002, T003, and so on.

### Priority

The first rule that matches is used.

| Rule | Condition | Priority |
|---|---|---|
| 1 | high urgency AND 10 or more affected users | critical |
| 2 | high urgency OR 10 or more affected users | high |
| 3 | medium urgency OR 3 or more affected users | medium |
| 4 | everything else | low |

### Status

Tickets move through: open → in_progress → resolved.

- An unassigned ticket cannot move to in_progress.
- A resolved ticket can only be changed after it is reopened (set back to open).

### Work queue

The queue shows open, unresolved tickets in the order critical, high, medium, low. Tickets with the same priority are ordered by the lower ticket number first.

## Where tickets are saved

Tickets are saved automatically to `data/tickets.json`. This file is created the first time a ticket is saved and is not committed to Git.

To start fresh, close the app and delete `data/tickets.json`.

If the file is damaged, the app shows an error and does not overwrite it.

## Known limitations

- The app is text-only, with no graphical or web interface.
- Only one person can use the data file at a time.
- Tickets cannot be edited or deleted after creation, only assigned and moved through statuses.
- <Add any other honest gaps you find while testing.>

## Pull requests

- Engineer A's PR: <paste link>
- Engineer B's PR: <paste link>
EOF