import random
from collections import deque

# Mock data for family members
family_members = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'},
    {'id': 4, 'name': 'Diana'}
]

# Mock data for tasks
tasks = [
    {'id': 1, 'description': 'Clean the house', 'status': 'Assigned', 'assignedTo': None},
    {'id': 2, 'description': 'Wash the dishes', 'status': 'Assigned', 'assignedTo': None},
    {'id': 3, 'description': 'Buy groceries', 'status': 'Assigned', 'assignedTo': None},
    {'id': 4, 'description': 'Take out the trash', 'status': 'Assigned', 'assignedTo': None},
    {'id': 5, 'description': 'Prepare dinner', 'status': 'Assigned', 'assignedTo': None},
    {'id': 6, 'description': 'Do laundry', 'status': 'Assigned', 'assignedTo': None},
    {'id': 7, 'description': 'Mow the lawn', 'status': 'Assigned', 'assignedTo': None},
    {'id': 8, 'description': 'Feed the pets', 'status': 'Assigned', 'assignedTo': None},
    {'id': 9, 'description': 'Clean the windows', 'status': 'Assigned', 'assignedTo': None},
    {'id': 10, 'description': 'Water the plants', 'status': 'Assigned', 'assignedTo': None}
]

# Initialize task queue for transfers
task_queue = deque(family_members)

# Track additional tasks for each member
additional_tasks = {member['id']: 0 for member in family_members}

def distribute_tasks(tasks, family_members):
    num_members = len(family_members)
    tasks_per_member = len(tasks) // num_members
    extra_tasks = len(tasks) % num_members

    assignments = {member['id']: [] for member in family_members}

    for i, task in enumerate(tasks):
        member_id = family_members[i % num_members]['id']
        assignments[member_id].append(task['id'])
        task['assignedTo'] = member_id
    
    # Handle extra tasks if any
    for i in range(extra_tasks):
        member_id = family_members[i]['id']
        assignments[member_id].append(tasks[len(tasks) - extra_tasks + i]['id'])
        tasks[len(tasks) - extra_tasks + i]['assignedTo'] = member_id

    return assignments

# Tasks deferral
def defer_task(task_id, member_id):
    # Mark the task as deferred
    update_task_status(task_id, 'Deferred')
    
    # Get the next member in the queue who is not the current member
    while True:
        next_member = task_queue.popleft()
        if next_member['id'] != member_id:
            task_queue.append(next_member)  # Move the member to the end of the queue
            break
        task_queue.append(next_member)  # Move the member to the end of the queue if same as deferring member

    # Assign the deferred task to the next member
    for task in tasks:
        if task['id'] == task_id:
            task['assignedTo'] = next_member['id']
            task['status'] = 'Assigned'
            break

    # Track additional tasks for the member who deferred the task
    additional_tasks[member_id] += 1
    additional_tasks[next_member['id']] -= 1

    # Rebalance tasks for the next week
    rebalance_tasks(family_members)

def update_task_status(task_id, status):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
    print(f"Updated task status for task {task_id}: {status}")

def rebalance_tasks(family_members):
    all_tasks = get_all_tasks()
    pending_tasks = [task for task in all_tasks if task['status'] == 'Assigned']
    
    num_members = len(family_members)
    tasks_per_member = len(pending_tasks) // num_members
    extra_tasks = len(pending_tasks) % num_members

    assignments = {member['id']: [] for member in family_members}

    for i, task in enumerate(pending_tasks):
        member_id = family_members[i % num_members]['id']
        assignments[member_id].append(task['id'])
        task['assignedTo'] = member_id
    
    # Handle extra tasks if any
    for i in range(extra_tasks):
        member_id = family_members[i]['id']
        assignments[member_id].append(pending_tasks[len(pending_tasks) - extra_tasks + i]['id'])
        pending_tasks[len(pending_tasks) - extra_tasks + i]['assignedTo'] = member_id

    return assignments

def get_all_tasks():
    return tasks

def get_all_family_members():
    return family_members

def get_tasks_for_member(member_id):
    return [task for task in tasks if task['assignedTo'] == member_id]

# Function to print the schedule
def print_schedule(assignments):
    for member_id, task_ids in assignments.items():
        member_name = next((member['name'] for member in family_members if member['id'] == member_id), None)
        task_descriptions = [task['description'] for task in tasks if task['id'] in task_ids]
        print(f"\nSchedule for {member_name}:")
        for task in task_descriptions:
            print(f" - {task}")

# Simulation Execution
print("Initial Task Distribution")
assignments = distribute_tasks(tasks, family_members)
print_schedule(assignments)

print("\nTasks before deferral:")
for task in tasks:
    print(task)

# Ask if there's a deferral
deferral_needed = input("\nIs there a deferral needed? (yes/no): ").strip().lower()

if deferral_needed == 'yes':
    member_name_deferring = input("Enter the name of the member who wants to defer a task: ").strip()
    member_deferring_task = next((member['id'] for member in family_members if member['name'].lower() == member_name_deferring.lower()), None)
    
    if member_deferring_task is not None:
        member_tasks = get_tasks_for_member(member_deferring_task)
        print(f"\n{member_name_deferring}'s tasks:")
        for task in member_tasks:
            print(f"Task ID: {task['id']}, Description: {task['description']}")

        task_to_defer = int(input("Enter the Task ID to defer: ").strip())
        
        if task_to_defer in [task['id'] for task in member_tasks]:
            print(f"\nDeferring Task {task_to_defer} for Member {member_name_deferring}")
            defer_task(task_to_defer, member_deferring_task)
        else:
            print("Invalid Task ID.")
    else:
        print("Invalid member name.")
else:
    print("No deferral needed.")

print("\nTasks after deferral and rebalancing:")
for task in tasks:
    print(task)

print("\nUpdated Schedule after Deferral:")
assignments = distribute_tasks([task for task in tasks if task['status'] == 'Assigned'], family_members)
print_schedule(assignments)
