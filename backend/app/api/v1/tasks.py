import structlog
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.extensions import db, redis_client
from app.models import Task
from app.schemas import TaskSchema

# Create logger
logger = structlog.get_logger(__name__)

# Create blueprint
tasks_bp = Blueprint('tasks', __name__)

# Schemas
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Cache settings
CACHE_EXPIRATION = 300  # 5 minutes

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    try:
        # Try to get from cache first
        cached_tasks = redis_client.client.get('all_tasks')

        if cached_tasks:
            logger.info("Tasks retrieved from cache")
            return jsonify(eval(cached_tasks))

        # If not in cache, get from database
        tasks = Task.query.all()
        result = tasks_schema.dump(tasks)

        # Store in cache
        redis_client.client.setex('all_tasks', CACHE_EXPIRATION, str(result))

        logger.info("Tasks retrieved from database", count=len(tasks))
        return jsonify(result)

    except Exception as e:
        logger.error("Error fetching tasks", error=str(e))
        return jsonify({"error": "Failed to fetch tasks"}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID."""
    try:
        # Try to get from cache first
        cached_task = redis_client.client.get(f'task_{task_id}')

        if cached_task:
            logger.info("Task retrieved from cache", task_id=task_id)
            return jsonify(eval(cached_task))

        # If not in cache, get from database
        task = Task.query.get(task_id)

        if not task:
            logger.error("Task not found", task_id=task_id)
            return jsonify({"error": "Task not found"}), 404

        result = task_schema.dump(task)

        # Store in cache
        redis_client.client.setex(f'task_{task_id}', CACHE_EXPIRATION, str(result))

        logger.info("Task retrieved from database", task_id=task_id)
        return jsonify(result)

    except Exception as e:
        logger.error("Error fetching task", task_id=task_id, error=str(e))
        return jsonify({"error": "Failed to fetch task"}), 500

@tasks_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        # Parse request data
        json_data = request.get_json()

        if not json_data:
            logger.error("No input data provided")
            return jsonify({"error": "No input data provided"}), 400

        # Validate data
        data = task_schema.load(json_data)

        # Create new task
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date')
        )

        # Save to database
        db.session.add(task)
        db.session.commit()

        # Invalidate caches
        redis_client.client.delete('all_tasks')

        result = task_schema.dump(task)

        logger.info("Task created", task_id=task.id)
        return jsonify(result), 201

    except ValidationError as e:
        logger.error("Validation error", errors=e.messages)
        return jsonify({"error": "Validation error", "messages": e.messages}), 400

    except Exception as e:
        db.session.rollback()
        logger.error("Error creating task", error=str(e))
        return jsonify({"error": "Failed to create task"}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    try:
        # Parse request data
        json_data = request.get_json()

        if not json_data:
            logger.error("No input data provided")
            return jsonify({"error": "No input data provided"}), 400

        # Get task
        task = Task.query.get(task_id)

        if not task:
            logger.error("Task not found", task_id=task_id)
            return jsonify({"error": "Task not found"}), 404

        # Validate data
        data = task_schema.load(json_data)

        # Update task
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        task.due_date = data.get('due_date', task.due_date)

        # Save to database
        db.session.commit()

        # Invalidate caches
        redis_client.client.delete('all_tasks')
        redis_client.client.delete(f'task_{task_id}')

        result = task_schema.dump(task)

        logger.info("Task updated", task_id=task_id)
        return jsonify(result)

    except ValidationError as e:
        logger.error("Validation error", errors=e.messages)
        return jsonify({"error": "Validation error", "messages": e.messages}), 400

    except Exception as e:
        db.session.rollback()
        logger.error("Error updating task", task_id=task_id, error=str(e))
        return jsonify({"error": "Failed to update task"}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        # Get task
        task = Task.query.get(task_id)

        if not task:
            logger.error("Task not found", task_id=task_id)
            return jsonify({"error": "Task not found"}), 404

        # Delete from database
        db.session.delete(task)
        db.session.commit()

        # Invalidate caches
        redis_client.client.delete('all_tasks')
        redis_client.client.delete(f'task_{task_id}')

        logger.info("Task deleted", task_id=task_id)
        return jsonify({"message": "Task deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error("Error deleting task", task_id=task_id, error=str(e))
        return jsonify({"error": "Failed to delete task"}), 500
