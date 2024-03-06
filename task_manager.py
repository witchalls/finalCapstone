# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# =====function declarations=========


def get_valid_int(included=[]):
    '''Gets user input and returns the input if it is an integer in included list.       
    '''
    while True:
        try:
            user_input = int(input())
            # Check if the user input is in included list. 
            if included != []:
                if user_input in included:
                    return user_input
                else:
                    print("Please enter a valid integer.")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def main_menu():
    '''Displays main options menu and takes the user's input 
       and then calls relevant function
    '''
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports (admin only)
    ds - Display statistics (admin only)
    e - Exit
    : ''').lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()

        elif menu == 'gr' and curr_user == 'admin':
            generate_reports()

        elif menu == 'ds' and curr_user == 'admin':
            '''If the user is an admin they can display statistics about number of users
                and tasks along with generated reports.'''
            
            # Check if there is a missing report file and run generate_reports if there is.
            if not os.path.exists("user_overview.txt") or not os.path.exists("task_overview.txt"):
                generate_reports()

            with open("user_overview.txt", "r") as file:
                report = file.read()

            with open("task_overview.txt", "r") as file:
                report += file.read()

            print(report)

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


def reg_user():
    '''Registers a new user and adds the data to users.txt'''
    user_exists = True
    while user_exists:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Username already exists.")
            continue
        else:
            user_exists = False

    while True:
        # - Request input of a new password.
        new_password = input("New Password: ")
        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break
        else:
            print("Passwords do no match")


def add_task():
    '''Gathers user input and adds the new task to the tasks.txt file
    '''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console the tasks
        that are assigned to the current users in the format presented in 
        the task pdf (i.e. includes spacing and labelling)
    '''
    task_counter = 0
    # List created for input validation, -1 added for menu option.
    valid_task_ids = [-1]
    # Loop through task_list and builds strings for tasks that match current user. 
    for i, t in enumerate(task_list, 1):
        if t['username'] == curr_user:
            valid_task_ids.append(i)
            task_counter += 1
            disp_str = '-'*50+'\n'
            disp_str += f"Task id: \t {i}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n{t['description']}\n"
            disp_str += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
            disp_str += '-'*50
            print(disp_str)

    print("Enter task id to mark as complete or edit or -1 to save and exit: ")

    if task_counter != 0:
        # Get task id from user to edit.
        selected_task = get_valid_int(included=valid_task_ids)
        if selected_task == -1:
            print("Saving changes and returning to main menu...")
            # Write task_list to tasks.txt file. 
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        'Yes' if t['completed'] else 'No'
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            main_menu()
    else:
        print("Task list is empty. Returning to main menu...")
        main_menu()

    # Set selected task as curr_task
    curr_task = task_list[selected_task - 1]

    print('''Task Menu:
c - Mark task as complete
e - Edit the task
x - Exit to my task list
    : ''')
    user_choice = input().lower()
    # Mark as complete option.
    if user_choice == 'c':
        curr_task['completed'] = True
        print("The task has been marked as complete")
    # Edit task option.
    elif user_choice == 'e':
        if curr_task['completed']:
            print("You cannot edited a task already marked as complete. Please select another task...")
            view_mine()

        print('''Edit Menu:
u - Change the user the task is assigned to (incomplete tasks only)
d - Change the due date
x - Exit to my task list
        ''')
        user_choice = input().lower()
        # Change user option.
        if user_choice == 'u':
            print(f"Which user would you like to assign task {selected_task} to?:")
            users = list(username_password.keys())
            valid_user_ids = []
            for i, user in enumerate(users, 1):
                print(f"{i}:\t {user}")
                valid_user_ids.append(i)
            selected_user = get_valid_int(included=valid_user_ids)
            curr_task['username'] = users[selected_user - 1]
        # Change date option.
        elif user_choice == 'd':
            print(f"What is the new due date of task {selected_task}?")
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(
                        task_due_date, DATETIME_STRING_FORMAT)
                    curr_task['due_date'] = due_date_time
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
        else:
            print("Invalid option")
    # Exit menu
    elif user_choice == 'x':
        print("Exiting menu...")
       
    else:
        print("Invalid option")
     

    # Return to view_mine menu.
    view_mine()


def generate_reports():
    '''Generates two files user_overview.txt and task_overview.txt
       The files contain statistics regarding the current tasks and users.
    '''
    # Build string for task_overview.txt
    completed = 0
    overdue = 0
    total_tasks = len(task_list)
    if total_tasks != 0:
        for task in task_list:
            if task['completed'] == True:
                completed += 1
            elif task['due_date'].date() < date.today():
                overdue += 1
        uncompleted = total_tasks - completed
        task_rpt = '-'*40 + '\n'
        task_rpt += "Task Overview\n"
        task_rpt += '-'*40 + '\n'
        task_rpt += f"Total tasks generated: \t\t{len(task_list)}\n"
        task_rpt += f"Total completed tasks: \t\t{completed}\n"
        task_rpt += f"Total uncompleted tasks: \t{uncompleted}\n"
        task_rpt += f"Total overdue tasks: \t\t{overdue}\n"
        task_rpt += f"Percentage incomplete: \t\t{round(uncompleted*100/total_tasks, 2)}%\n"
        task_rpt += f"Percentage overdue: \t\t{round(overdue*100/total_tasks, 2)}%\n"
        task_rpt += '-'*40
    else:
        task_rpt = "No tasks found"

    # Build string for user_overview.txt
    user_rpt = '-'*40 + '\n'
    user_rpt += "User Overview\n"
    user_rpt += '-'*40 + '\n'
    user_rpt += f"Total users: \t{len(username_password.keys())}\n"
    user_rpt += f"Total tasks: \t{total_tasks}\n"
    user_rpt += '-'*40 + '\n\n'
    user_rpt += '-'*40 + '\n'
    user_rpt += "User Statistics\n"
    user_rpt += '-'*40 + '\n\n'
    
    # Display stats for individual users.
    for user in username_password.keys():
        completed_tasks = 0
        uncompleted_tasks = 0
        total_user_tasks = 0
        overdue = 0
        for task in task_list:
            if task['username'] == user:
                total_user_tasks += 1
                if task['completed'] == False:
                    uncompleted_tasks += 1
                    if task['due_date'].date() < date.today():
                        overdue += 1
                else:
                    completed_tasks += 1

        user_rpt += f"{user}:\n"
        user_rpt += f"Total tasks assigned: \t{total_user_tasks}\n"
        if total_user_tasks != 0:
            user_rpt += f"Percentage assigned: \t{round(total_user_tasks*100/total_tasks, 2)}%\n"
            user_rpt += f"Percentage completed: \t{round(completed_tasks*100/total_user_tasks, 2)}%\n"
            user_rpt += f"Percentage overdue: \t{round(overdue*100/total_user_tasks, 2)}%\n\n"

        else:
            user_rpt += "*The user has no assigned tasks!*\n\n"

    user_rpt += '-'*40+'\n'

    # Write strings to files.
    try:
        with open('user_overview.txt', 'w') as out_file:
            out_file.write(user_rpt)
            print("User overview file created.")
    except Exception as e:
        print("There was an error writing to file!", e)

    try:
        with open('task_overview.txt', 'w') as out_file:
            out_file.write(task_rpt)
            print("Task overview file created.")
    except Exception as e:
        print("There was an error writing to file!", e)


# ======= Main Logic =======
# Create tasks.txt if it doesn't exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component.
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


# ======= Login Section =======
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account.
if not os.path.exists("user.txt"):
    print("File not found")
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data.
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

main_menu()
