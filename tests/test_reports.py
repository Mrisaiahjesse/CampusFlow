"""Unit tests for CampusFlow ticket reports."""

import unittest

from campusflow.reports import generate_report


class TestGenerateReport(unittest.TestCase):
    """Test ticket totals and report validation."""

    def setUp(self):
        """Create sample tickets for testing."""
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "high",
            },
            {
                "id": "T003",
                "status": "resolved",
                "priority": "medium",
            },
            {
                "id": "T004",
                "status": "open",
                "priority": "low",
            },
        ]

    def test_total_ticket_count(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["total_tickets"], 4)

    def test_counts_tickets_by_status(self):
        report = generate_report(self.tickets)

        self.assertEqual(
            report["by_status"],
            {
                "open": 2,
                "in_progress": 1,
                "resolved": 1,
            },
        )

    def test_counts_tickets_by_priority(self):
        report = generate_report(self.tickets)

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 1,
                "medium": 1,
                "low": 1,
            },
        )

    def test_empty_list_returns_zero_counts(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )
        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_non_list_input_is_rejected(self):
        with self.assertRaises(TypeError):
            generate_report(None)

    def test_non_dictionary_ticket_is_rejected(self):
        with self.assertRaises(TypeError):
            generate_report(["invalid ticket"])

    def test_invalid_status_is_rejected(self):
        tickets = [
            {
                "id": "T001",
                "status": "pending",
                "priority": "high",
            }
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)

    def test_invalid_priority_is_rejected(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "urgent",
            }
        ]

        with self.assertRaises(ValueError):
            generate_report(tickets)


if __name__ == "__main__":
    unittest.main()