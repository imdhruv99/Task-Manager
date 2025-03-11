import logging
from datetime import datetime
from models import db, Task

logger = logging.getLogger(__name__)

def get_tasks():
    """Get all tasks."""
    return Task.query.order_by(Task.created_at.desc()).all()

def get_task(task_id):
    """Get a task by ID."""
    return Task.query.get(task_id)

def create_task(task_data):
    """Create a new task."""
    try:
        task = Task(
            title=task_data.get('title'),
            description=task_data.get('description'),
            status=task_data.get('status', 'todo'),
            priority=task_data.get('priority', 'medium'),
            due_date=task_data.get('due_date')
        )
        db.session.add(task)
        db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating task: {str(e)}")
        raise

def update_task(task, task_data):
    """Update an existing task."""
    try:
        # Update task attributes
        if 'title' in task_data:
            task.title = task_data['title']
        if 'description' in task_data:
            task.description = task_data['description']
        if 'status' in task_data:
            task.status = task_data['status']
        if 'priority' in task_data:
            task.priority = task_data['priority']
        if 'due_date' in task_data:
            task.due_date = task_data['due_date']

        # Update timestamp
        task.updated_at = datetime.utcnow()

        db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task: {str(e)}")
        raise

def delete_task(task):
    """Delete a task."""
    try:
        db.session.delete(task)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        raise
