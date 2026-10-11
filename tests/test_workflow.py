"""Unit tests for CampusFlow ticket assignment and workflow."""

import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    reopen_ticket,
)


class TestTicketWorkflow(unittest.TestCase):
    """Test ticket assignment, status changes, and reopening."""

    def setUp(self):
        """Create a fresh ticket for each test."""
        self.tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi is not working",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

    # Assignment tests

    def test_assign_ticket_successfully(self):
        ticket = assign_ticket(self.tickets, "T001", "James")

        self.assertEqual(ticket["assigned_to"], "James")

    def test_assignment_removes_extra_spaces_from_name(self):
        ticket = assign_ticket(self.tickets, "T001", "  James  ")

        self.assertEqual(ticket["assigned_to"], "James")

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_non_string_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", None)

    def test_unknown_ticket_assignment_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "James")

    def test_assignment_rejects_non_list_ticket_collection(self):
        with self.assertRaises(TypeError):
            assign_ticket(None, "T001", "James")

    def test_assignment_rejects_non_dictionary_ticket(self):
        with self.assertRaises(TypeError):
            assign_ticket(["invalid ticket"], "T001", "James")

    def test_assignment_rejects_ticket_with_invalid_status(self):
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "James")

    def test_resolved_ticket_cannot_be_assigned(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "James")

    # Status workflow tests

    def test_assigned_ticket_can_start_work(self):
        assign_ticket(self.tickets, "T001", "James")

        ticket = update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(ticket["status"], "in_progress")

    def test_unassigned_ticket_cannot_start_work(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

    def test_ticket_can_be_resolved_after_work_starts(self):
        assign_ticket(self.tickets, "T001", "James")
        update_status(self.tickets, "T001", "in_progress")

        ticket = update_status(self.tickets, "T001", "resolved")

        self.assertEqual(ticket["status"], "resolved")

    def test_open_ticket_cannot_skip_work_in_progress(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "resolved")

    def test_invalid_status_name_is_rejected(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "pending")

    def test_unknown_ticket_status_update_is_rejected(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T999", "in_progress")

    def test_resolved_ticket_cannot_change_status_directly(self):
        assign_ticket(self.tickets, "T001", "James")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "open")

    def test_ticket_with_invalid_current_status_cannot_be_updated(self):
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

    # Reopening tests

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.tickets, "T001", "James")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        ticket = reopen_ticket(self.tickets, "T001")

        self.assertEqual(ticket["status"], "open")

    def test_unresolved_ticket_cannot_be_reopened(self):
        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T001")

    def test_unknown_ticket_cannot_be_reopened(self):
        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T999")

    def test_reopening_rejects_ticket_with_invalid_status(self):
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T001")


if __name__ == "__main__":
    unittest.main()