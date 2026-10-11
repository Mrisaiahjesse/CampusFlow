from campusflow.storage import load_tickets, save_tickets
from campusflow.queue import get_priority_queue
from campusflow.reports import generate_report
from campusflow.workflow import assign_ticket, reopen_ticket, update_status
from campusflow.tickets import create_ticket, format_ticket_details, format_ticket_line, get_ticket


def show_menu():
    print("""
=== CampusFlow Helpdesk ===
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Change ticket status
6. Show work queue
7. Show report
0. Exit
""")


def handle_create(tickets):
    title = input("Title: ")
    category = input("Category (Network, Hardware, Software, Other): ")
    urgency = input("Urgency (low, medium, high): ")
    affected_users = input("Affected users: ")

    try:
        ticket = create_ticket(tickets, title, category, urgency, affected_users)
        save_tickets(tickets)
        print(f"Ticket {ticket['id']} created with priority {ticket['priority']}.")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def handle_list(tickets):
    if not tickets:
        print("No tickets yet.")
        return

    print("\n=== All Tickets ===")
    for ticket in tickets:
        print(format_ticket_line(ticket))


def handle_view(tickets):
    ticket_id = input("Ticket ID (e.g. T001): ").strip().upper()

    try:
        print(format_ticket_details(get_ticket(tickets, ticket_id)))
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def handle_assign(tickets):
    ticket_id = input("Ticket ID to assign: ").strip().upper()
    staff_name = input("Staff member's name: ")

    try:
        ticket = assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets)
        print(f"Ticket {ticket['id']} assigned to {ticket['assigned_to']}.")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def handle_status(tickets):
    ticket_id = input("Ticket ID: ").strip().upper()
    print("1. Start work\n2. Resolve ticket\n3. Reopen resolved ticket")

    actions = {"1": "in_progress", "2": "resolved", "3": "reopen"}
    action = input("Choose an action: ").strip()
    new_status = actions.get(action)

    if not new_status:
        print("Invalid action. Choose 1, 2, or 3.")
        return

    try:
        ticket = (
            reopen_ticket(tickets, ticket_id)
            if new_status == "reopen"
            else update_status(tickets, ticket_id, new_status)
        )
        save_tickets(tickets)
        print(f"Ticket {ticket['id']} status is now {ticket['status']}.")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def handle_queue(tickets):
    try:
        queue = get_priority_queue(tickets)
        if not queue:
            print("No unresolved tickets in the work queue.")
            return

        print("\n=== Priority Work Queue ===")
        for ticket in queue:
            print(format_ticket_line(ticket))
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def handle_report(tickets):
    try:
        report = generate_report(tickets)
        print(f"\n=== CampusFlow Report ===\nTotal tickets: {report['total_tickets']}")

        print("\nTickets by status:")
        for status, count in report["by_status"].items():
            print(f"  {status.replace('_', ' ').title()}: {count}")

        print("\nTickets by priority:")
        for priority, count in report["by_priority"].items():
            print(f"  {priority.title()}: {count}")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def main():
    try:
        tickets = load_tickets()
    except (ValueError, TypeError) as error:
        print(f"Error loading tickets: {error}")
        return

    handlers = {
        "1": handle_create,
        "2": handle_list,
        "3": handle_view,
        "4": handle_assign,
        "5": handle_status,
        "6": handle_queue,
        "7": handle_report,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break
        elif choice in handlers:
            handlers[choice](tickets)
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()