"""Ticket assignment and status workflow for CampusFlow."""

from typing import Any


VALID_STATUSES = {"open", "in_progress", "resolved"}

ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


def _find_ticket(
    tickets: list[dict[str, Any]],
    ticket_id: str,
) -> dict[str, Any]:
    """Find a ticket by ID.

    Args:
        tickets: The collection of ticket dictionaries.
        ticket_id: The ID of the ticket to find.

    Returns:
        The matching ticket dictionary.

    Raises:
        TypeError: If the collection is not a list or contains
            a non-dictionary item.
        ValueError: If the requested ticket does not exist.
    """
    if not isinstance(tickets, list):
        raise TypeError("Tickets must be provided as a list.")

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise TypeError("Each ticket must be a dictionary.")

        if ticket.get("id") == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} not found.")


def assign_ticket(
    tickets: list[dict[str, Any]],
    ticket_id: str,
    staff_name: str,
) -> dict[str, Any]:
    """Assign an unresolved ticket to a staff member."""
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must be a non-empty string.")

    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")

    if current_status not in VALID_STATUSES:
        raise ValueError(
            f"Ticket has an invalid current status: {current_status}"
        )

    if current_status == "resolved":
        raise ValueError("Reopen a resolved ticket before modifying it.")

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_status(
    tickets: list[dict[str, Any]],
    ticket_id: str,
    new_status: str,
) -> dict[str, Any]:
    """Update a ticket's status when the transition is permitted."""
    if not isinstance(new_status, str) or new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")

    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")

    if current_status not in VALID_STATUSES:
        raise ValueError(
            f"Ticket has an invalid current status: {current_status}"
        )

    if current_status == "resolved":
        raise ValueError(
            "Resolved tickets must be reopened before changing status."
        )

    if (
        current_status == "open"
        and new_status == "in_progress"
        and not ticket.get("assigned_to")
    ):
        raise ValueError("A ticket must be assigned before work can begin.")

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )

    ticket["status"] = new_status

    return ticket


def reopen_ticket(
    tickets: list[dict[str, Any]],
    ticket_id: str,
) -> dict[str, Any]:
    """Reopen a resolved ticket and preserve its existing assignment."""
    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")

    if current_status not in VALID_STATUSES:
        raise ValueError(
            f"Ticket has an invalid current status: {current_status}"
        )

    if current_status != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"

    return ticket