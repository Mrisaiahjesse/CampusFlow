"""Priority-based work queue for CampusFlow."""

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

VALID_STATUSES = {"open", "in_progress", "resolved"}


def get_priority_queue(tickets):
    """Return unresolved tickets sorted by priority and numeric ID.

    Resolved tickets are excluded. Remaining tickets are sorted first
    by priority and then by the numeric portion of their ticket IDs.

    The original list is not modified.

    Args:
        tickets: A list of ticket dictionaries.

    Returns:
        A new list of unresolved tickets in priority order.

    Raises:
        TypeError: If tickets is not a list or contains non-dictionaries.
        ValueError: If a ticket has an invalid status, priority, or ID.
    """
    if not isinstance(tickets, list):
        raise TypeError("Tickets must be provided as a list.")

    unresolved_tickets = []

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise TypeError("Each ticket must be a dictionary.")

        ticket_id = ticket.get("id")
        status = ticket.get("status")
        priority = ticket.get("priority")

        # Validate status before deciding whether to exclude the ticket.
        if status not in VALID_STATUSES:
            raise ValueError(
                f"Ticket {ticket_id} has an invalid status: {status}"
            )

        # Validate priority for every ticket, including resolved tickets.
        if priority not in PRIORITY_ORDER:
            raise ValueError(
                f"Ticket {ticket_id} has an invalid priority: {priority}"
            )

        # Validate the ticket ID for every ticket.
        if (
            not isinstance(ticket_id, str)
            or len(ticket_id) < 2
            or not ticket_id.startswith("T")
            or not ticket_id[1:].isdigit()
        ):
            raise ValueError(f"Invalid ticket ID: {ticket_id}")

        # Resolved tickets do not belong in the active work queue.
        if status == "resolved":
            continue

        unresolved_tickets.append(ticket)

    # Sort by priority first, then by numeric ticket ID.
    return sorted(
        unresolved_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )