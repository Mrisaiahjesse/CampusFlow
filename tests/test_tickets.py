import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    generate_ticket_id,
    get_ticket,
)


class TestPriority(unittest.TestCase):
    def test_high_urgency_with_12_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_with_2_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_with_4_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_with_1_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_boundary_low_urgency_with_10_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_boundary_medium_urgency_with_1_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")


class TestCreateTicket(unittest.TestCase):
    def test_valid_ticket_is_created_and_normalized(self):
        tickets = []
        ticket = create_ticket(tickets, "  Wi-Fi is down ", "network", "HIGH", "15")

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(tickets), 1)

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Broken laptop", "Hardware", "low", 0)

    def test_negative_decimal_and_text_affected_users_are_rejected(self):
        for bad_value in [-3, "-3", 2.5, "2.5", "many", True]:
            with self.assertRaises(ValueError):
                create_ticket([], "Broken laptop", "Hardware", "low", bad_value)

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "   ", "Network", "low", 1)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Power cut", "Electricity", "low", 1)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket([], "Power cut", "Other", "urgent", 1)

    def test_invalid_input_does_not_change_the_ticket_list(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "Wi-Fi is down", "Network", "high", 0)
        self.assertEqual(tickets, [])


class TestTicketIds(unittest.TestCase):
    def test_ids_increase_one_by_one(self):
        tickets = []
        first = create_ticket(tickets, "One", "Other", "low", 1)
        second = create_ticket(tickets, "Two", "Other", "low", 1)
        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_next_id_follows_the_highest_existing_id(self):
        tickets = [{"id": "T005"}, {"id": "T002"}]
        self.assertEqual(generate_ticket_id(tickets), "T006")


class TestGetTicket(unittest.TestCase):
    def test_finds_ticket_ignoring_case_and_spaces(self):
        tickets = []
        create_ticket(tickets, "One", "Other", "low", 1)
        self.assertEqual(get_ticket(tickets, " t001 ")["id"], "T001")

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(ValueError):
            get_ticket([], "T999")


if __name__ == "__main__":
    unittest.main()
