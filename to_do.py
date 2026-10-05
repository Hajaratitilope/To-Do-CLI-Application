import json
from datetime import date, datetime
import os

# =========================
# Configuration
# =========================

PRIORITY_LEVELS = ["high", "medium", "low"]

FILTER_CHOICES = [
    "category",
    "priority",
    "status",
    "due date",
    "completed date"
]

DATE_FILTERS = ["due date", "completed date"]

FIELD_CHOICES = ["1", "2", "3", "4"]

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if not value:
            print("This field cannot be empty.")
        else:
            return value
        
def get_valid_date(prompt):
    while True:
        value = input(prompt).strip()
        
        try:
            converted_value = datetime.strptime(value, "%Y-%m-%d").date().isoformat()
            break
        
        except ValueError:
                    print("❌ Invalid format. Please use exactly YYYY-MM-DD (e.g., 2026-09-29).")
                    
    return converted_value

def get_task():
    task_desc = get_non_empty_input("What task do you want to handle? ")
            
    category = get_non_empty_input("What category does this task belong to? ")
            
    while True:
        priority = input("Enter a priority level of High, Medium or Low: ").strip().lower()
        
        if not priority:
            print("This field cannot be empty.")
        elif priority not in PRIORITY_LEVELS:
            print("Priority level has to be High, Medium or Low")
        else:
            break
    
    due_date = get_valid_date("Enter a date for which this task is due (YYYY-MM-DD): ")
    
    task = {
        "task description": task_desc,
        "category": category,
        "priority": priority,
        "due date": due_date,
        "completed date": None,
        "status": "pending"
    }
    
    return task

def save_task(task):
    with open("tasks.json", "w") as file:
        json.dump(task, file, indent=4)

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
        
    return []

def add_task():
    tasks = load_tasks()
    
    new_task = get_task()
    
    tasks.append(new_task)
    
    save_task(tasks)

def view_tasks(tasks):
    
    for number, task in enumerate(tasks, start = 1):
        print(f"Task {number}")
        print(f"Description: {task["task description"]}")
        print(f"Category: {task["category"]}")
        print(f"Priority: {task["priority"]}")
        print(f"Due Date: {task["due date"]}")
        print(f"Completed Date: {task["completed date"]}")
        print(f"Status: {task["status"]}")
        print()
        
def complete_task():
    tasks = load_tasks()
    
    if not tasks:
        print("There are no tasks to complete.")
        return
        
    view_tasks(tasks)
        
    while True:
        try:
            task_number = int(input("Enter the task number of the task you want completed: "))
            
            if task_number <= 0 or task_number > len(tasks):
                print(f"Task number has to be between 1 and {len(tasks)}")
                continue
    
            completed_task = tasks[task_number -1]
    
            completed_task["status"] = "completed"

            completed_task["completed date"] = date.today().isoformat()
    
            save_task(tasks)
    
            print(f"{completed_task["task description"].title()} has been marked completed")
            
            break
            
        except ValueError:
            print("Enter a number: ")

def view_completed_task():
    tasks = load_tasks()
    
    num_completed_tasks = 0
    
    for task in tasks:
        if task["status"] == "completed":
            num_completed_tasks += 1
            
    if num_completed_tasks == 0:
        print("There are no completed tasks.")
        return
    
    a = "=" * len("Congratulations! The following tasks have been completed")
    print(f"{a}\nCongratulations! The following tasks have been completed\n{a}")
    
    for index, task in enumerate(tasks, start=1):
                
        if task["status"] == "completed":
            print(f"Task {index}: {task["task description"]}")
            
def view_pending_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("There are no tasks recorded.")
        return
    
    pending_tasks = []
    for task in tasks:
        if task["status"] == "pending":
            pending_tasks.append(task)
            
    if pending_tasks:
        view_tasks(pending_tasks)
    else:
        print("There are no pending tasks.")
            
def delete_task():
    tasks = load_tasks()
    
    if not tasks:
        print("There are no tasks recorded for deletion.")
        return None, None
    
    view_tasks(tasks)
        
    while True:
        try:
            task_number = int(input("Provide the task number of the task you are about to delete: "))
            
            if task_number <= 0 or task_number > len(tasks):
                print(f"Task number has to be between 1 and {len(tasks)}")
                continue
                
            task_index = task_number -1    
            deleted_task = tasks.pop(task_index)
    
            save_task(tasks)
    
            print(f"You have just deleted Task {task_number} and it is {deleted_task["status"]}")
            print(f"Description: {deleted_task["task description"]}")
            print(f"Category: {deleted_task["category"]}")
            print(f"Priority: {deleted_task["priority"]}")
            print(f"Due Date: {deleted_task["due date"]}")
            print(f"Completed Date: {deleted_task["completed date"]}")
            print(f"status: {deleted_task["status"]}")
            
            break
        
        except ValueError:
            print("Enter a number")
            
    return deleted_task, task_index

def return_deleted_task(task_index, deleted_task):
    tasks = load_tasks()
    
    tasks.insert(task_index, deleted_task)
    
    save_task(tasks)
    
    print("You have successfully undone the deleted task.")

def edit_task():
    tasks = load_tasks()

    if not tasks:
        print("There are no tasks to be edited.")
        return

    view_tasks(tasks)

    while True:
        try:
            choice = int(input("Which task do you want to edit? "))

            if choice <= 0 or choice > len(tasks):
                print(f"Task number should be between 1 and {len(tasks)}.")
                continue

            editable_task = tasks[choice - 1]

            print(
                f"You are about to edit "
                f"'{editable_task['task description'].title()}'"
            )

            print("1. Task Description")
            print("2. Category")
            print("3. Priority")
            print("4. Due Date")

            while True:
                field_choice = input(
                    "What would you like to edit in this task? "
                ).strip()

                if field_choice not in FIELD_CHOICES:
                    print("Please pick an option (number) from the menu displayed.")
                    continue

                if field_choice == "1":
                    editable_task["task description"] = get_non_empty_input(
                        "Please edit the task description: "
                    )

                elif field_choice == "2":
                    editable_task["category"] = get_non_empty_input(
                        "Please edit the category of this task: "
                    )

                elif field_choice == "3":
                    while True:
                        priority = input(
                            "Enter a new priority level of high, medium or low: "
                        ).strip().lower()

                        if not priority:
                            print("This field cannot be empty.")
                        elif priority not in PRIORITY_LEVELS:
                            print("Priority level has to be high, medium or low.")
                        else:
                            editable_task["priority"] = priority
                            break

                elif field_choice == "4":
                    editable_task["due date"] = get_valid_date(
                        "Please edit the 'Due Date' field in this format (YYYY-MM-DD): "
                    )

                break

        except ValueError:
            print("Please enter the task number you want to edit.")
            continue

        save_task(tasks)
        print("Task successfully updated.")
        break
    
def filter_():
    tasks = load_tasks()

    print("================")
    print("Filter Tasks")
    print("================")
    print("Category")
    print("Priority")
    print("Due Date")
    print("Completed Date")
    print("Status")

    if not tasks:
        print("There are no tasks to filter.")
        return

    choice = get_non_empty_input(
        "What do you want to filter by? "
    ).lower()

    if choice not in FILTER_CHOICES:
        print("Invalid filter option.")
        return

    if choice in DATE_FILTERS:
        keyword_choice = get_valid_date(
            "Enter date to search (YYYY-MM-DD): "
        )
    else:
        keyword_choice = get_non_empty_input(
            "Enter keyword to search: "
        ).lower()

    filtered_tasks = []

    for task in tasks:
        if task[choice] is not None and task[choice].lower() == keyword_choice:
            filtered_tasks.append(task)

    if filtered_tasks:
        view_tasks(filtered_tasks)
    else:
        print("No matching tasks found.")
        
deleted_task = None

while True:
    print()
    print("Task Organizer")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Complete Task")
    print("4. View Completed Tasks")
    print("5. View Pending Tasks")
    print("6. Edit Task")
    print("7. Delete Task")
    print("8. Filter Tasks")
    print("9. Undo a deleted task")
    print("10. Exit")
    
    choice = input("What would you like to do with the task organizer today? ")
    print()
    
    if choice == "1":
        add_task()
    elif choice == "2":
        tasks = load_tasks()
        view_tasks(tasks)
    elif choice == "3":
        complete_task()
    elif choice == "4":
        view_completed_task()
    elif choice == "5":
        view_pending_tasks()
    elif choice == "6":
        edit_task()
    elif choice == "7":
        deleted_task, task_index = delete_task()
    elif choice == "8":
        filter_()
    elif choice == "9":
        if deleted_task is None:
            print("Nothing to undo.")
        else:
            return_deleted_task(task_index, deleted_task)
            deleted_task = None
    elif choice == "10":
        break