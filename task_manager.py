import json
from pathlib import Path
from datetime import datetime
import rich
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os

"""
This module provides a simple task manager application.

The main function initializes a TaskManager instance, which is responsible for managing tasks.

"""

#Get the current date and time
current_time = datetime.now()

console = Console()

DATA_FILE = Path('tasks.json')




#Clears the console
def clear_console():
    
    """
    Clears the console.

    This function uses the os.system call to execute the
    correct command to clear the console, depending on the
    operating system.

    On Windows, the command is 'cls'.
    On other systems, the command is 'clear'.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def load_tasks():
    
    """
    Loads tasks from the JSON file.

    If the file does not exist, an empty JSON file is created.
    If the file is corrupted or unreadable, an empty list is returned.

    Returns:
        list: A list of tasks loaded from the JSON file.
    """
    if not DATA_FILE.exists():
        # Create an empty JSON file if it doesn't exist
        DATA_FILE.write_text(json.dumps([], indent=2))
        console.print('No JSON file detected, creating file...')
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If the file is corrupted or unreadable, skip loading
        return []
def save_tasks(tasks):
    # If tasks are already dicts, don't use __dict__
    """
    Saves the tasks to the JSON file.

    If the tasks are already dicts, they are saved directly to the JSON file.
    If the tasks are Task objects, their dictionaries are extracted using the __dict__ method.

    """
    DATA_FILE.write_text(json.dumps(tasks, indent=2))



class Task:
    def __init__(self, title, description, status='Incomplete', created=None, number=None):
        
        
        """
        Initializes a Task object.

        """
        self.title = title
        self.description = description
        self.status = status
        self.created = created or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.number = number 
    def mark_complete(self):
        self.status = 'Complete'
        
        
        
class TaskManager:
    def __init__(self):
        """
        Initializes the TaskManager.

        Loads tasks from the JSON file, creates a list of Task objects,
        fixes missing numbers, and saves the tasks back to the JSON file.

        """
        loaded_tasks = load_tasks()
        self.tasks = [Task(**task) for task in loaded_tasks]
        # Fix missing numbers
        next_number = 1
        for task in self.tasks:
            if not isinstance(task.number, int) or task.number is None:
                task.number = next_number
            next_number = max(next_number, task.number + 1)
        save_tasks([task.__dict__ for task in self.tasks])
        self.next_number = next_number - 1
        
        

    def add_task(self, title, description):
        
        """
        Adds a new task to the task list.
        
        """
        self.next_number += 1
        task = Task(title, description, status='Incomplete', number=self.next_number)
        self.tasks.append(task)
        save_tasks([task.__dict__ for task in self.tasks])
        console.print(f'Task "{title}" added successfully!', style='bold green')
                    
    def mark_task_complete(self, title):
        """
        Marks a task as complete in the task manager.
      
        Prints:
            - A success message if the task is marked as complete successfully.
            - An error message if no task with the provided title is found.
        """
        for task in self.tasks:
            if task.title == title:
                task.mark_complete()
                console.print(f'Task "{title}" marked as complete!', current_time, style='bold green')
                return
        console.print(f'No task with title "{title}" found.', style='bold red')

    def view_tasks(self):
        if not self.tasks:
            console.print('No tasks found. Please enter a task to view.', style='bold red')
        else:
            table = Table(title='Task List')
            table.add_column('No.', style='bold')
            table.add_column('Title', style='magenta')
            table.add_column('Description', style='cyan')
            table.add_column('Status')
            table.add_column('Date Created', style='yellow')
            for task in self.tasks:
                status_display = f"[green]{task.status}[/green]" if task.status == "Complete" else f"[red]{task.status}[/red]"
                table.add_row(str(task.number), task.title, task.description, status_display, task.created)
            console.print(table)

    def delete_task(self, title):
        """
        Deletes a task from the task manager.
       
        Prints:
            - A success message if the task is deleted successfully.
            - An error message if no task with the provided title is found.
        """
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                console.print(f'Task "{title}" deleted successfully!', style='bold green')
                return
        console.print(f'No task with title "{title}" found.', style ='bold red')

    def clear_task(self):
        """
        Clears all tasks from the task list.
     
        """
        self.tasks.clear()
        console.print('Task list cleared!', style='bold green')
        

    def update_task(self, title, new_title=None, new_description=None):
        """
        Updates the title and/or description of a task in the task manager.
        Args:
            title (str): The title of the task to be updated.
            new_title (str, optional): The new title for the task. If not provided, the current title will be kept.
            new_description (str, optional): The new description for the task. If not provided, the current description will be kept.
        Returns:
            None
        Prints:
            - A success message if the task is updated successfully.
            - An error message if no task with the provided title is found.
        """
        for task in self.tasks:
            if task.title == title:
                new_title = input('Enter new title or (leave blank to keep current title):')
                new_description = input('Enter new description or (leave blank to keep current description):')
                if new_title:
                    task.title = new_title
                if new_description:
                    task.description = new_description
                console.print(f'Task "{title}" updated successfully!', style='bold green')
                return
        console.print(f'No task with title "{title}" found.', style='bold red')
        
        
# Main Menu
def display_menu():
    """
    Displays the main menu of the Task Manager application.

    The main menu displays all available options to the user, including
    adding a new task, viewing tasks, marking a task as complete, updating
    a task, deleting a task, clearing all tasks, and exiting the application.

    The main menu is displayed in a Rich Table format, with columns for the
    option number, action, and description.
    """
    console.print(
        Panel(
            Align.center('[bold cyan]Task Manager[/bold cyan]'),
            title='[gold]Main Menu[/gold]',
            border_style='bright_magenta',
            expand=True,
            subtitle='Choose an option:',
        )
    )
    
    
    menu_items = [
        ('1', 'Add Task', 'Add a new task to the task list.'),
        ('2', 'View Tasks', 'View all tasks in the task list.'),
        ('3', 'Mark Task as Complete', 'Mark a specific task as complete.'),
        ('4', 'Update Task', 'Update the title or description of a task.'),
        ('5', 'Delete Task', 'Delete a specific task from the task list.'),
        ('6', 'Clear All Tasks', 'Clear all tasks from the task list.'),
        ('7', 'Exit', 'Exit the application.')
    ]  
    
    table = Table(title='Menu Items')
    table.add_column('Option', style='cyan')
    table.add_column('Action', style='red')
    table.add_column('Description', style='green')
    
    for key, action, description in menu_items:
        table.add_row(f'[{key}]', action, description)
        
    console.print(table)

def main():
    '''
    Main function of Task Manager.

    This function is the entry point of the Task Manager application.
    It initializes a TaskManager object and enters a loop where it displays
    the main menu, waits for user input, and performs the corresponding action.

    The loop continues until the user chooses to exit the application.

    '''
    task_manager = TaskManager()
    try:
        while True:
            clear_console()  # Clear at the start of each loop
            display_menu()
            console.print(f'To copy and item please use (Shift+Ctrl+C)', style = 'white')
            console.print(f'(Ctrl + C) exits the program!', style = 'red')
            choice = input('Enter your choice (1-7):')
            
            if choice == '1':
                title = input('Enter task title:')
                description = input('Enter task description:')
                task_manager.add_task(title,description)
                save_tasks([task.__dict__ for task in task_manager.tasks])
            elif choice == '2':
                task_manager.view_tasks()
            elif choice == '3':
                title = input('Enter the title of the task to complete:')
                task_manager.mark_task_complete(title)
                save_tasks([task.__dict__ for task in task_manager.tasks])
            elif choice == '4':
                title = input('Enter the title of the task to update:')
                task_manager.update_task(title)
                save_tasks([task.__dict__ for task in task_manager.tasks])
            elif choice == '5':
                title = input('Enter the title of the task to delete:')
                task_manager.delete_task(title)
                save_tasks([task.__dict__ for task in task_manager.tasks])
            elif choice == '6':
                task_manager.clear_task()
                save_tasks([task.__dict__ for task in task_manager.tasks])
            elif choice == '7':
                save_tasks([task.__dict__ for task in task_manager.tasks])
                console.print('Exiting Task Manager.' , style='bold blue')
                input('Press Enter to exit...')
                clear_console()  # Clear at the end before exit
                break
            else:
                console.print('Invalid choice. Please input a number between 1-7.', style='bold red')
            
            input('Press Enter to continue...')  # Pause before clearing
    except KeyboardInterrupt:
        save_tasks([task.__dict__ for task in task_manager.tasks])
        console.print('\nExiting Task Manager (Ctrl+C detected). Goodbye!', style='bold blue')


if __name__ == '__main__':
    main()
