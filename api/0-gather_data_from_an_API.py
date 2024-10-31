#!/usr/bin/python3
"""Prints the TODO list progress for a given employee ID."""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """Fetches the TODO list progress for a given employee ID."""

    # Define the API endpoint
    url = f'https://jsonplaceholder.typicode.com/users/{employee_id}'

    try:
        # Send a GET request to the API
        response = requests.get(url + '/todos')
        response.raise_for_status()  # Raise an error for bad responses
        todos = response.json()  # Parse the JSON response

        # Extract completed and total tasks
        completed_tasks = [task for task in todos if task.get('completed')]
        total_tasks = len(todos)
        number_of_done_tasks = len(completed_tasks)

        # Get employee name from the user API
        user_response = requests.get(url)
        user_response.raise_for_status()
        user_info = user_response.json()
        employee_name = user_info.get('name')

        # Output the results
        print(
            f'Employee {employee_name} is done with tasks'
            f'({number_of_done_tasks}/{total_tasks}):'
        )

        for task in completed_tasks:
            print(f'\t{task.get("title")}')

    except requests.RequestException as e:
        print(f'Error fetching data: {e}')


if __name__ == "__main__":
    # Check if an employee ID is provided
    if len(sys.argv) != 2:
        print("Usage: python3 todo_progress.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer for employee ID.")
        sys.exit(1)

    get_employee_todo_progress(employee_id)
