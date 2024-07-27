import random

family_members = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'},
    {'id': 4, 'name': 'Diana'}
]

tasks = [
    {'id': 1, 'description': 'Clean the house', 'status': 'Assigned', 'assignedTo': None},
    {'id': 2, 'description': 'Wash the dishes', 'status': 'Assigned', 'assignedTo': None},
    {'id': 3, 'description': 'Buy groceries', 'status': 'Assigned', 'assignedTo': None},
    {'id': 4, 'description': 'Take out the trash', 'status': 'Assigned', 'assignedTo': None},
    {'id': 5, 'description': 'Prepare dinner', 'status': 'Assigned', 'assignedTo': None},
    {'id': 6, 'description': 'Do laundry', 'status': 'Assigned', 'assignedTo': None},
    {'id': 7, 'description': 'Mow the lawn', 'status': 'Assigned', 'assignedTo': None},
    {'id': 8, 'description': 'Feed the pets', 'status': 'Assigned', 'assignedTo': None},
]


def distribute_tasks(tasks, family_members):
    num_members = len(family_members)
    tasks_per_member = len(tasks) // num_members
    extra_tasks = len(tasks) % num_members

    assignments = {member['id']: [] for member in family_members}

    for i, task in enumerate(tasks):
        member_id = family_members[i % num_members]['id']
        assignments[member_id].append(task['id'])
    
    # Handle extra tasks if any
    for i in range(extra_tasks):
        member_id = family_members[i]['id']
        assignments[member_id].append(tasks[len(tasks) - extra_tasks + i]['id'])

    # Update task assignments in the database
    for member_id, task_ids in assignments.items():
        update_task_assignment(member_id, task_ids)

#Tasks deferral
def defer_task(task_id, member_id):
    # Mark the task as deferred
    update_task_status(task_id, 'Deferred')
    
    # Get the list of tasks and members
    tasks = get_tasks_for_member(member_id)
    family_members = get_all_family_members()
    
    # Rebalance tasks
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
    
    # Handle extra tasks if any
    for i in range(extra_tasks):
        member_id = family_members[i]['id']
        assignments[member_id].append(pending_tasks[len(pending_tasks) - extra_tasks + i]['id'])

    # Update task assignments in the database
    for member_id, task_ids in assignments.items():
        update_task_assignment(member_id, task_ids)

def execute_query(query, params):
    print(f"Executing query: {query} with params {params}")
    # This function should handle executing the SQL query
    # and commit changes to the database.
    # pass

def update_task_assignment(member_id, task_ids):
    # This function updates the assignments in the database.
    # Assumes task_ids is a list of task IDs to be assigned.
    for task in tasks:
        if task['id'] in task_ids:
            task['assignedTo'] = member_id
    print(f"Updated task assignments for member {member_id}: {task_ids}")

def get_all_tasks():
    return tasks
    # This function should return all tasks from the database
    # Assumed to return a list of task dictionaries
    # pass

def get_all_family_members():
    return family_members
    # This function should return all family members from the database
    # Assumed to return a list of member dictionaries
    # pass

def get_tasks_for_member(member_id):
    return [task for task in tasks if task['assignedTo'] == member_id]
    # This function should return all tasks assigned to a specific member
    # pass

# Simulation Execution
print("Initial Task Distribution")
assignments = distribute_tasks(tasks, family_members)

print("\nTasks before deferral:")
for task in tasks:
    print(task)

# Simulate deferring a task
task_to_defer = random.choice([task['id'] for task in tasks if task['status'] == 'Assigned'])
member_deferring_task = random.choice(family_members)['id']

print(f"\nDeferring Task {task_to_defer} for Member {member_deferring_task}")
defer_task(task_to_defer, member_deferring_task)

print("\nTasks after deferral and rebalancing:")
for task in tasks:
    print(task)