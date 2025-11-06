import csv
import os
import re  # Used for basic email and phone number format validation

# --- Configuration and Data Storage ---
CONTACTS_FILE = "my_personal_contacts.csv"
CONTACT_FIELDS = ['name', 'phone', 'email', 'address']


# --- Utility Functions ---

def load_contacts():
    """Loads contacts from the CSV file into a list of dictionaries."""
    contacts_list = []
    if not os.path.exists(CONTACTS_FILE):
        return contacts_list
    try:
        with open(CONTACTS_FILE, mode='r', newline='', encoding='utf-8') as file:
            # Use DictReader to automatically read rows into dictionaries
            reader = csv.DictReader(file, fieldnames=CONTACT_FIELDS)

            # Skip the header row if it exists (but ensure we don't skip actual data)
            # Simple check: if the first item matches field names, skip it.
            first_row = next(reader, None)
            if first_row and first_row['name'] != 'name':
                contacts_list.append(first_row)

            # Add the rest of the rows
            for row in reader:
                contacts_list.append(row)

    except Exception as e:
        print(f"Error loading contacts: {e}. Starting with an empty list.")
    return contacts_list


def save_contacts(contacts_list):
    """Saves the current list of contacts to the CSV file, including a header."""
    try:
        with open(CONTACTS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CONTACT_FIELDS)

            # Manually write the header row for clarity
            writer.writeheader()

            # Write all contacts
            writer.writerows(contacts_list)
        print("Contacts saved successfully to file.")
    except Exception as e:
        print(f"Critical Error: Could not save contacts! {e}")


# --- Input Validation Helpers ---

def get_validated_input(prompt, validation_type='text'):
    """Prompts user and applies simple regex validation for email/phone."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty.")
            continue

        if validation_type == 'email':
            # Simple email regex check
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                print("Invalid email format. Please re-enter.")
                continue

        elif validation_type == 'phone':
            # Simple phone regex check (digits, spaces, dashes, parentheses)
            if not re.match(r"^[0-9()\s-]+$", value):
                print("Invalid phone format. Use only numbers and common delimiters.")
                continue

        return value


# --- Core Contact Book Functions ---

def add_contact(contacts_list):
    """Prompts the user for all details and adds a new contact."""
    print("\n--- Adding New Contact ---")

    new_contact = {}
    new_contact['name'] = get_validated_input("Enter Name: ")
    new_contact['phone'] = get_validated_input("Enter Phone Number: ", 'phone')
    new_contact['email'] = get_validated_input("Enter Email: ", 'email')
    new_contact['address'] = input("Enter Address (optional): ").strip()

    contacts_list.append(new_contact)
    save_contacts(contacts_list)
    print(f"Contact '{new_contact['name']}' added successfully.")


def view_contact_list(contacts_list):
    """Displays a list of all saved contacts (Name and Phone only)."""
    if not contacts_list:
        print("\nYour Contact Book is empty!")
        return

    print("\n--- 👥 Saved Contact List ---")
    # Using enumerate gives us a clean 1-based index for the user
    for i, contact in enumerate(contacts_list, 1):
        print(f"[{i:02d}] Name: {contact['name']:<20} | Phone: {contact['phone']}")
    print("----------------------------------\n")


def search_contact(contacts_list):
    """Allows searching by name or phone number and prints matching details."""
    if not contacts_list:
        print("The contact book is empty, nothing to search.")
        return

    term = input("Enter Name or Phone Number to search: ").strip().lower()

    # Filter the list based on the search term
    found_contacts = [
        c for c in contacts_list
        if term in c['name'].lower() or term in c['phone'].replace(' ', '').replace('-', '')
    ]

    if not found_contacts:
        print(f"No contacts found matching '{term}'.")
        return

    print(f"\n--- {len(found_contacts)} Contact(s) Found ---")
    for contact in found_contacts:
        print(f"\nName:    {contact['name']}")
        print(f"Phone:   {contact['phone']}")
        print(f"Email:   {contact['email'] if contact['email'] else 'N/A'}")
        print(f"Address: {contact['address'] if contact['address'] else 'N/A'}")
    print("------------------------------------------\n")


def update_contact(contacts_list):
    """Allows the user to select a contact and update any of its fields."""
    view_contact_list(contacts_list)
    if not contacts_list:
        return

    try:
        # Prompt for 1-based index
        index_str = input("Enter the number (index) of the contact to update: ").strip()
        contact_index = int(index_str) - 1

        if not (0 <= contact_index < len(contacts_list)):
            print("Invalid contact number.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    contact_to_update = contacts_list[contact_index]
    print(f"\n--- Updating Contact: {contact_to_update['name']} ---")

    for field in CONTACT_FIELDS:
        current_value = contact_to_update[field]
        new_value = input(f"Enter new {field} (Current: '{current_value}'). Press Enter to keep: ").strip()

        if new_value:
            # Re-apply validation if a new value is entered
            validation_type = 'phone' if field == 'phone' else ('email' if field == 'email' else 'text')
            try:
                # Use the validator logic for validation before updating
                validated_new_value = get_validated_input(f"Confirm new {field}: ", validation_type)
                contact_to_update[field] = validated_new_value
            except Exception:  # Handle the case where the user entered an empty line after the first input
                contact_to_update[field] = new_value

    save_contacts(contacts_list)
    print(f"Contact '{contact_to_update['name']}' updated successfully.")


def delete_contact(contacts_list):
    """Allows the user to select a contact and delete it."""
    view_contact_list(contacts_list)
    if not contacts_list:
        return

    try:
        index_str = input("Enter the number (index) of the contact to DELETE: ").strip()
        contact_index = int(index_str) - 1

        if not (0 <= contact_index < len(contacts_list)):
            print("Invalid contact number.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    deleted_contact = contacts_list.pop(contact_index)
    save_contacts(contacts_list)
    print(f"Contact '{deleted_contact['name']}' successfully deleted.")


# --- Main Application Loop ---

def main_menu():
    """Displays the main menu and handles user input."""

    # Load contacts once at the start of the application
    contacts = load_contacts()

    while True:
        print("\n=====Personal Contact Manager =====")
        print("1. View Contact List (Quick)")
        print("2. Add New Contact")
        print("3. Search Contact (Details)")
        print("4. Update Contact Details")
        print("5. Delete Contact")
        print("6. Exit")
        print("=======================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            view_contact_list(contacts)
        elif choice == '2':
            add_contact(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            update_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            print("Exiting Contact Manager. Goodbye!")
            save_contacts(contacts)  # Final save before exit
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Entry point of the script
if __name__ == "__main__":
    main_menu()