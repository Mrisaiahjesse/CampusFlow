# Allowed values for support tickets
VALID_CATEGORIES = ["Network", "Hardware", "Software", "Other"]
VALID_URGENCY_LEVELS = ["low", "medium", "high"]


def validate_category(category):
    """Validate the category and return its standardized form."""
    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    category = category.strip().lower()

    for valid_category in VALID_CATEGORIES:
        if category == valid_category.lower():
            return valid_category

    raise ValueError(
        "Invalid category. Choose Network, Hardware, Software, or Other."
    )


def validate_urgency(urgency):
    """Validate the urgency and return it in lowercase."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    urgency = urgency.strip().lower()

    if urgency in VALID_URGENCY_LEVELS:
        return urgency

    raise ValueError("Invalid urgency. Choose low, medium, or high.")


def validate_title(title):
    """Validate the title and return it without extra spaces."""
    if not isinstance(title, str):
        raise ValueError("Title must be text.")

    title = title.strip()

    if title == "":
        raise ValueError("Title must not be blank.")

    return title


def validate_affected_users(affected_users):
    """Validate affected_users and return it as a positive whole number."""
    # True and False count as numbers in Python, so reject them first
    if isinstance(affected_users, bool):
        raise ValueError("Affected users must be a positive whole number.")

    # The menu gives us text like "15", so accept digits-only text
    if isinstance(affected_users, str):
        text = affected_users.strip()
        if not text.isdigit():
            raise ValueError("Affected users must be a positive whole number.")
        affected_users = int(text)
    elif not isinstance(affected_users, int):
        raise ValueError("Affected users must be a positive whole number.")

    if affected_users <= 0:
        raise ValueError("Affected users must be a positive whole number.")

    return affected_users


def calculate_priority(urgency, affected_users):
    """Return critical, high, medium or low using the four rules in order."""
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def generate_ticket_id(tickets):
    """Return the next ticket ID, such as T001, T002, T003."""
    highest = 0
    for ticket in tickets:
        number = int(ticket["id"][1:])  # "T005" -> 5
        if number > highest:
            highest = number
    return f"T{highest + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate everything, then add a new ticket to the list and return it."""
    # Validate first, so a bad input never changes the list
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    ticket = {
        "id": generate_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def get_ticket(tickets, ticket_id):
    """Find one ticket by ID. Raises ValueError if it does not exist."""
    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be text.")

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} not found.")


def format_ticket_line(ticket):
    """One-line summary used when listing all tickets."""
    return (
        f"{ticket['id']} | {ticket['priority']:<8} | "
        f"{ticket['status']:<11} | {ticket['title']}"
    )


def format_ticket_details(ticket):
    """Multi-line details used when viewing one ticket."""
    assigned = ticket["assigned_to"] or "Unassigned"
    lines = [
        f"ID:             {ticket['id']}",
        f"Title:          {ticket['title']}",
        f"Category:       {ticket['category']}",
        f"Urgency:        {ticket['urgency']}",
        f"Affected users: {ticket['affected_users']}",
        f"Priority:       {ticket['priority']}",
        f"Status:         {ticket['status']}",
        f"Assigned to:    {assigned}",
    ]
    return "\n".join(lines)
