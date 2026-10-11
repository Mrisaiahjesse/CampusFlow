import os
import tempfile
import unittest

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class TestStorage(unittest.TestCase):
    def setUp(self):
        # A temporary folder that is deleted after each test
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "tickets.json")

    def test_save_and_reload_keeps_existing_tickets(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi is down", "Network", "high", 15)
        create_ticket(tickets, "Slow laptop", "Hardware", "low", 1)

        save_tickets(tickets, self.path)
        reloaded = load_tickets(self.path)

        self.assertEqual(reloaded, tickets)

    def test_missing_file_gives_an_empty_list(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_corrupted_json_gives_a_clear_error_and_keeps_the_file(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{ this is not valid json")

        with self.assertRaises(ValueError):
            load_tickets(self.path)

        with open(self.path, "r", encoding="utf-8") as file:
            self.assertEqual(file.read(), "{ this is not valid json")

    def test_new_ticket_after_reload_does_not_duplicate_ids(self):
        tickets = []
        create_ticket(tickets, "One", "Other", "low", 1)
        create_ticket(tickets, "Two", "Other", "low", 1)
        save_tickets(tickets, self.path)

        reloaded = load_tickets(self.path)
        new_ticket = create_ticket(reloaded, "Three", "Other", "low", 1)

        ids = [ticket["id"] for ticket in reloaded]
        self.assertEqual(new_ticket["id"], "T003")
        self.assertEqual(len(ids), len(set(ids)))

    def test_empty_list_can_be_saved_and_reloaded(self):
        save_tickets([], self.path)
        self.assertEqual(load_tickets(self.path), [])


if __name__ == "__main__":
    unittest.main()
