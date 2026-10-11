"""Ticket reporting utilities for CampusFlow."""

STATUSES = ("open", "in_progress", "resolved")

PRIORITIES = ("critical", "high", "medium", "low")


def generate_report(tickets):
    """Generate ticket totals grouped by status and priority.

    Args:
        tickets: A list of ticket dictionaries.

    Returns:
        A dictionary containing the total number of tickets,
        counts by status, and counts by priority.

    Raises:
        TypeError: If tickets is not a list or contains
            non-dictionary entries.
        ValueError: If a ticket contains an unknown status
            or priority.
    """
    if not isinstance(tickets, list):
        raise TypeError("Tickets must be provided as a list.")

    report = {
        "total_tickets": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
    }

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise TypeError("Each ticket must be a dictionary.")

        status = ticket.get("status")
        priority = ticket.get("priority")

        if status not in STATUSES:
            raise ValueError(
                f"Ticket {ticket.get('id')} has an invalid status: {status}"
            )

        if priority not in PRIORITIES:
            raise ValueError(
                f"Ticket {ticket.get('id')} has an invalid priority: {priority}"
            )

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report