#!/usr/bin/python3
"""Record the TODO list for a given list of employee IDs in a JSON file"""

import json
import requests
import sys


def save_employees_todo_progress(employee_ids):
    """Record the TODO list for a given list of employee IDs in JSON"""

    # Define the API endpoint
    user_url = 'https://jsonplaceholder.typicode.com/users/'
    todos_url = 'https://jsonplaceholder.typicode.com/todos'

    try:
        # Send a GET request to fetch all TODOs
        response = requests.get(todos_url)
        response.raise_for_status()  # Raise an error for bad responses
        todos = response.json()  # Parse the JSON response

        # Initialize a dictionary
        data = {}

        # Process each employee ID provided
        for employee_id in employee_ids:
            # Get employee name from the user API
            user_response = requests.get(user_url + str(employee_id))
            user_response.raise_for_status()
            user_info = user_response.json()
            employee_name = user_info.get('name')

            # Filter todos for the specific employee ID
            user_todos = [task for task in todos
                          if task.get('userId') == employee_id]

            data[employee_id] = [
                {
                    "task": task.get('title'),
                    "completed": task.get('completed'),
                    "username": employee_name
                }
                for task in user_todos
            ]

        # Write the collected data to a JSON file
        with open("todo_all_employees.json", "w") as file:
            json.dump(data, file)

    except requests.RequestException as e:
        print(f'Error fetching data: {e}')


if __name__ == "__main__":
    # Check if employee IDs are provided
    if len(sys.argv) < 2:
        print("Give a list of integer")
        sys.exit(1)

    try:
        # Convert the list of IDs from command-line arguments to integers
        employee_ids = [int(id_str) for id_str in sys.argv[1:]]
        # employee_ids = [1, 2 ,3 ,4, 5, 6, 7, 8, 9, 10]
    except ValueError:
        print("Please provide a list of valid integer employee IDs.")
        sys.exit(1)

    save_employees_todo_progress(employee_ids)
