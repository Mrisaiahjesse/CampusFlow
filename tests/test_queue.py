"""Unit tests for the CampusFlow priority queue."""

import unittest

from campusflow.queue import get_priority_queue


class TestPriorityQueue(unittest.TestCase):
    """Test priority ordering, filtering, and input validation."""

    def setUp(self):
        """Create sample tickets for each test."""
        self.tickets = [
            {
                "id": "T003",
                "priority": "medium",
                "status": "open",
            },
            {
                "id": "T002",
                "priority": "critical",
                "status": "open",
            },
            {
                "id": "T001",
                "priority": "high",
                "status": "in_progress",
            },
            {
                "id": "T004",
                "priority": "low",
                "status": "open",
            },
            {
                "id": "T005",
                "priority": "high",
                "status": "resolved",
            },
        ]

    def test_critical_tickets_come_first(self):
        result = get_priority_queue(self.tickets)

        self.assertEqual(result[0]["priority"], "critical")

    def test_tickets_are_sorted_by_priority(self):
        result = get_priority_queue(self.tickets)

        priorities = [ticket["priority"] for ticket in result]

        self.assertEqual(
            priorities,
            ["critical", "high", "medium", "low"],
        )

    def test_resolved_tickets_are_excluded(self):
        result = get_priority_queue(self.tickets)

        ticket_ids = [ticket["id"] for ticket in result]

        self.assertNotIn("T005", ticket_ids)

    def test_numeric_ticket_ids_break_priority_ties(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
            {"id": "T001", "priority": "high", "status": "open"},
        ]

        result = get_priority_queue(tickets)

        ticket_ids = [ticket["id"] for ticket in result]

        self.assertEqual(ticket_ids, ["T001", "T002", "T010"])

    def test_original_list_order_is_not_modified(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        get_priority_queue(self.tickets)

        current_ids = [ticket["id"] for ticket in self.tickets]

        self.assertEqual(current_ids, original_ids)

    def test_empty_ticket_list_returns_empty_list(self):
        result = get_priority_queue([])

        self.assertEqual(result, [])

    def test_non_list_input_is_rejected(self):
        with self.assertRaises(TypeError):
            get_priority_queue(None)

    def test_non_dictionary_ticket_is_rejected(self):
        with self.assertRaises(TypeError):
            get_priority_queue(["invalid ticket"])

    def test_invalid_priority_is_rejected(self):
        tickets = [
            {"id": "T001", "priority": "urgent", "status": "open"}
        ]

        with self.assertRaises(ValueError):
            get_priority_queue(tickets)

    def test_invalid_ticket_id_is_rejected(self):
        tickets = [
            {"id": "ABC", "priority": "high", "status": "open"}
        ]

        with self.assertRaises(ValueError):
            get_priority_queue(tickets)

    def test_ticket_with_missing_status_is_rejected(self):
        tickets = [
            {
                "id": "T001",
                "priority": "critical",
            }
        ]

        with self.assertRaises(ValueError):
            get_priority_queue(tickets)

    def test_ticket_with_invalid_status_is_rejected(self):
        tickets = [
            {
                "id": "T001",
                "priority": "critical",
                "status": "pending",
            }
        ]

        with self.assertRaises(ValueError):
            get_priority_queue(tickets)


if __name__ == "__main__":
    unittest.main()