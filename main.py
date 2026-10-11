from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import (
    create_ticket,
    format_ticket_details,
    format_ticket_line,
    get_ticket,
)


def show_menu():
    print("\n=== CampusFlow Helpdesk ===")
    print("1. Create ticket")
    print("2. List all tickets")
    print("3. View one ticket")
    print("4. Assign ticket")
    print("5. Change ticket status")
    print("6. Show work queue")
    print("7. Show report")
    print("0. Exit")


def handle_create(tickets):
    title = input("Title: ")
    category = input("Category (Network, Hardware, Software, Other): ")
    urgency = input("Urgency (low, medium, high): ")
    affected_users = input("Affected users: ")

    try:
        ticket = create_ticket(tickets, title, category, urgency, affected_users)
    except ValueError as error:
        print(f"Error: {error}")
        return

    save_tickets(tickets)
    print(f"Ticket {ticket['id']} created with priority {ticket['priority']}.")


def handle_list(tickets):
    if not tickets:
        print("No tickets yet.")
        return

    for ticket in tickets:
        print(format_ticket_line(ticket))


def handle_view(tickets):
    ticket_id = input("Ticket ID (for example T001): ")

    try:
        ticket = get_ticket(tickets, ticket_id)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(format_ticket_details(ticket))


def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Error: {error}")
        return  # Stop, so we never overwrite a damaged file

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_create(tickets)
        elif choice == "2":
            handle_list(tickets)
        elif choice == "3":
            handle_view(tickets)
        elif choice == "4":
            # ENGINEER B: call your assign function here, then save_tickets(tickets)
            print("Not built yet (Engineer B).")
        elif choice == "5":
            # ENGINEER B: call your status-change function here, then save_tickets(tickets)
            print("Not built yet (Engineer B).")
        elif choice == "6":
            # ENGINEER B: show the work queue here
            print("Not built yet (Engineer B).")
        elif choice == "7":
            # ENGINEER B: show the report here
            print("Not built yet (Engineer B).")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
