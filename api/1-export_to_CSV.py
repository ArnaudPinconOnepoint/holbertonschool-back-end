#!/usr/bin/python3
"""Record the TODO list for a given employee ID in CSV"""

import csv
import requests
import sys


def save_employee_todo_progress(employee_id):
    """Record the TODO list for a given employee ID in CSV"""

    # Define the API endpoint
    url = f'https://jsonplaceholder.typicode.com/users/{employee_id}'

    try:
        # Send a GET request to the API
        response = requests.get(url + '/todos')
        response.raise_for_status()  # Raise an error for bad responses
        todos = response.json()  # Parse the JSON response

        # Get employee name from the user API
        user_response = requests.get(url)
        user_response.raise_for_status()
        user_info = user_response.json()
        employee_name = user_info.get('name')

        filename = "USER_ID.csv"

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            field = [
                "USER_ID", "USERNAME",
                "TASK_COMPLETED_STATUS", "TASK_TITLE"]
            # writer.writerow(field)
            for task in todos:
                writer.writerow(
                    [employee_id, employee_name,
                     task.get('completed'), task.get('title')])

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

    save_employee_todo_progress(employee_id)
