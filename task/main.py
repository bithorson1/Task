import sqlite3
from datetime import datetime

# Database setup
def initialize_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    deadline TEXT,
                    status TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Task class
class Task:
    def __init__(self, id, description, deadline, status):
        self.id = id
        self.description = description
        self.deadline = deadline
        self.status = status

    def __str__(self):
        return f"ID: {self.id}, Description: {self.description}, Deadline: {self.deadline}, Status: {self.status}"

# CRUD Operations
def add_task(description, deadline, status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (description, deadline, status) VALUES (?, ?, ?)',
               (description, deadline, status))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = [Task(*row) for row in c.fetchall()]
    conn.close()
    return tasks

def get_pending_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE status = "pending"')
    tasks = [Task(*row) for row in c.fetchall()]
    conn.close()
    return tasks

def get_completed_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE status = "completed"')
    tasks = [Task(*row) for row in c.fetchall()]
    conn.close()
    return tasks

def update_task(task_id, description=None, deadline=None, status=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if description:
        c.execute('UPDATE tasks SET description = ? WHERE id = ?', (description, task_id))
    if deadline:
        c.execute('UPDATE tasks SET deadline = ? WHERE id = ?', (deadline, task_id))
    if status:
        c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# User Interface
def display_menu():
    print("\nTask Management Application")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. View pending tasks")
    print("4. View completed tasks")
    print("5. Update a task")
    print("6. Delete a task")
    print("7. Exit")

def main():
    initialize_db()
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD, optional): ")
            status = input("Enter status (pending/completed): ")
            add_task(description, deadline or None, status)
            print("Task added successfully!")

        elif choice == '2':
            tasks = get_all_tasks()
            for task in tasks:
                print(task)

        elif choice == '3':
            tasks = get_pending_tasks()
            for task in tasks:
                print(task)

        elif choice == '4':
            tasks = get_completed_tasks()
            for task in tasks:
                print(task)

        elif choice == '5':
            task_id = int(input("Enter task ID to update: "))
            description = input("Enter new description (leave blank to skip): ")
            deadline = input("Enter new deadline (YYYY-MM-DD, leave blank to skip): ")
            status = input("Enter new status (pending/completed, leave blank to skip): ")
            update_task(task_id, description or None, deadline or None, status or None)
            print("Task updated successfully!")

        elif choice == '6':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
            print("Task deleted successfully!")

        elif choice == '7':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()