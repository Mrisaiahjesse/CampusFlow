import json
import os

# Always find the data folder next to main.py, wherever you run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATH = os.path.join(BASE_DIR, "data", "tickets.json")


def load_tickets(path=DEFAULT_PATH):
    """Load tickets from a JSON file. A missing file means a fresh start."""
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(
            f"The file {path} is not valid JSON. "
            "Fix or delete it, then try again."
        )

    if not isinstance(data, list):
        raise ValueError(f"The file {path} must contain a list of tickets.")

    return data


def save_tickets(tickets, path=DEFAULT_PATH):
    """Save tickets to a JSON file."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Write to a temporary file first, then swap it in.
    # If the program crashes while writing, the old file stays safe.
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)
    os.replace(temp_path, path)
