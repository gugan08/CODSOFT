import json
import os
from datetime import datetime

# --- Configuration and Data Storage ---
TODO_FILE = "my_personal_todo_list.json"
DATE_FORMAT = "%Y-%m-%d"

# --- Utility Functions ---

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as file:

            content = file.read()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"Error loading tasks: {e}. Starting with an empty list.")
        return []

def save_tasks(tasks_list):
    """Saves the current list of tasks to the JSON file."""
    try:
        with open(TODO_FILE, 'w') as file:
            json.dump(tasks_list, file, indent=4)
    except Exception as e:
        print(f"Critical Error: Could not save tasks! {e}")

def get_next_id(tasks_list):
    """Calculates the next unique ID for a new task."""
    if not tasks_list:
        return 1
    # Find the maximum existing ID and add 1
    max_id = max(task.get('id', 0) for task in tasks_list)
    return max_id + 1

# --- Core To-Do Functions ---

def add_task(tasks_list):
    """Prompts the user for a new task description and adds it to the list."""
    description = input("Enter the new task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return

    # Optional: get a due date
    due_date_input = input(f"Enter due date (optional, format: {DATE_FORMAT}): ").strip()
    due_date = ""
    if due_date_input:
        try:
            # Simple validation check
            datetime.strptime(due_date_input, DATE_FORMAT)
            due_date = due_date_input
        except ValueError:
            print(f"Invalid date format. Due date not set. Please use {DATE_FORMAT}.")

    new_task = {
        'id': get_next_id(tasks_list),
        'description': description,
        'done': False,
        'created_on': datetime.now().strftime(DATE_FORMAT),
        'due_date': due_date
    }
    tasks_list.append(new_task)
    save_tasks(tasks_list)
    print(f"Task #{new_task['id']} added successfully.")

def view_tasks(tasks_list):
    """Displays all tasks in a structured, readable format."""
    if not tasks_list:
        print("\n Your To-Do List is empty! Time to add some tasks.")
        return

    print("\n--- Current To-Do List ---")
    for task in tasks_list:
        status = "DONE" if task['done'] else "☐ PENDING"
        due = f" (Due: {task['due_date']})" if task.get('due_date') else ""
        print(f"[{task['id']}] {status} | {task['description']}{due}")
    print("------------------------------\n")

def find_task_by_id(tasks_list, task_id):
    """Helper to find a task dictionary by its unique ID."""
    try:
        task_id = int(task_id)
        return next((task for task in tasks_list if task['id'] == task_id), None)
    except ValueError:
        return None

def mark_task_done(tasks_list):
    """Changes the 'done' status of a task."""
    task_id = input("Enter the ID of the task to mark as DONE: ").strip()
    task = find_task_by_id(tasks_list, task_id)

    if task:
        task['done'] = True
        save_tasks(tasks_list)
        print(f"Task #{task['id']} marked as done.")
    else:
        print(f"Task with ID '{task_id}' not found.")

def delete_task(tasks_list):
    """Removes a task from the list using its unique ID."""
    task_id = input("Enter the ID of the task to DELETE: ").strip()
    task = find_task_by_id(tasks_list, task_id)

    if task:
        # Use list comprehension to create a new list without the deleted task
        tasks_list[:] = [t for t in tasks_list if t['id'] != task['id']]
        save_tasks(tasks_list)
        print(f"Task #{task['id']} successfully deleted.")
    else:
        print(f"Task with ID '{task_id}' not found.")

# --- Main Application Loop ---

def main_menu():
    """Displays the main menu and handles user input."""
    tasks = load_tasks()

    while True:
        print("\n===== To-Do List Manager =====")
        print("1. View Tasks")
        print("2. Add New Task")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        print("==============================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            view_tasks(tasks) # Show tasks first for convenience
            mark_task_done(tasks)
        elif choice == '4':
            view_tasks(tasks) # Show tasks first for convenience
            delete_task(tasks)
        elif choice == '5':
            print("Saving and exiting. Goodbye!")
            save_tasks(tasks) # Ensure final save on exit
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Entry point of the script
if __name__ == "__main__":
    main_menu()