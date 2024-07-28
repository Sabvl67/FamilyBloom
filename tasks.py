from flask import Blueprint, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import deque

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')
db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Assigned')
    assigned_to = db.Column(db.Integer, nullable=True)

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
    # Add more tasks as needed
]

# Initialize task queue for transfers
task_queue = deque(family_members)

# Track additional tasks for each member
additional_tasks = {member['id']: 0 for member in family_members}

@tasks_bp.route('/')
def tasks_index():
    return render_template('tasks.html')

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@tasks_bp.route('/api/tasks/assign', methods=['POST'])
def assign_tasks():
    assignments = distribute_tasks(tasks, family_members)
    print("Assignments:", assignments)  # Print result to console
    return jsonify(assignments)

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

    print("Task Assignments:")
    for member_id, task_ids in assignments.items():
        print(f"Member {member_id}: {task_ids}")

    return assignments

# Tasks deferral
@tasks_bp.route('/api/tasks/defer', methods=['POST'])
def defer_task():
    data = request.get_json()
    task_id = data['task_id']
    member_id = data['member_id']

    update_task_status(task_id, 'Deferred')
    next_member = task_queue.popleft()
    while next_member['id'] == member_id:
        task_queue.append(next_member)
        next_member = task_queue.popleft()
    task_queue.append(next_member)

    for task in tasks:
        if task['id'] == task_id:
            task['assignedTo'] = next_member['id']
            task['status'] = 'Assigned'
            break

    print(f"Task {task_id} reassigned to Member {next_member['id']}")


    additional_tasks[member_id] += 1
    additional_tasks[next_member['id']] -= 1

    assignments = rebalance_tasks(family_members)
    print("Rebalanced Task Assignments:")
    for member_id, task_ids in assignments.items():
        print(f"Member {member_id}: {task_ids}")

    db.session.commit()
    return jsonify({'message': 'Task deferred'}), 200

def update_task_status(task_id, status):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status

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

    for i in range(extra_tasks):
        member_id = family_members[i]['id']
        assignments[member_id].append(pending_tasks[len(pending_tasks) - extra_tasks + i]['id'])
        pending_tasks[len(pending_tasks) - extra_tasks + i]['assignedTo'] = member_id

    return assignments

def get_all_tasks():
    return tasks

def get_all_family_members():
    return family_members


# def main():
#     print("Initial Tasks:")
#     print(tasks)
#     print("\nInitial Family Members:")
#     print(family_members)

#     # Assign tasks
#     print("\nAssigning tasks...")
#     distribute_tasks(tasks, family_members)

#     # Simulate deferring a task
#     task_id_to_defer = 1
#     member_id_to_defer = 1
#     print(f"\nDeferring Task {task_id_to_defer} from Member {member_id_to_defer}...")
#     data = {'task_id': task_id_to_defer, 'member_id': member_id_to_defer}
#     defer_task()  # You should simulate the request.get_json() here if you use it directly

# if __name__ == "__main__":
#     main()