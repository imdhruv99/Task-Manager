import logging
from flask import request, jsonify
from models import db, Task
from schemas.task import task_schema, tasks_schema
from services.task_service import get_tasks, get_task, create_task, update_task, delete_task
from services.cache_service import cache_get, cache_set, cache_delete
from api import api_blueprint
from utils.error_handler import APIError

logger = logging.getLogger(__name__)

@api_blueprint.route('/tasks', methods=['GET'])
def list_tasks():
    """Get all tasks."""
    try:
        # Try to get tasks from cache
        cached_tasks = cache_get('all_tasks')
        if cached_tasks:
            logger.info("Retrieved tasks from cache")
            return jsonify(cached_tasks)

        # Get tasks from database
        tasks = get_tasks()
        result = tasks_schema.dump(tasks)

        # Cache tasks
        cache_set('all_tasks', result)

        logger.info(f"Retrieved {len(tasks)} tasks")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise APIError("Failed to retrieve tasks", 500)

@api_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    """Get a single task by ID."""
    try:
        # Try to get task from cache
        cached_task = cache_get(f'task_{task_id}')
        if cached_task:
            logger.info(f"Retrieved task {task_id} from cache")
            return jsonify(cached_task)

        # Get task from database
        task = get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise APIError("Task not found", 404)

        result = task_schema.dump(task)

        # Cache task
        cache_set(f'task_{task_id}', result)

        logger.info(f"Retrieved task {task_id}")
        return jsonify(result)
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        raise APIError("Failed to retrieve task", 500)

@api_blueprint.route('/tasks', methods=['POST'])
def add_task():
    """Create a new task."""
    try:
        # Validate request data
        json_data = request.get_json()
        if not json_data:
            raise APIError("No input data provided", 400)

        # Validate task data
        errors = task_schema.validate(json_data)
        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise APIError(f"Invalid task data: {errors}", 400)

        # Create task
        task = create_task(json_data)
        result = task_schema.dump(task)

        # Invalidate cache
        cache_delete('all_tasks')

        logger.info(f"Created task {task.id}")
        return jsonify(result), 201
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise APIError("Failed to create task", 500)

@api_blueprint.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def modify_task(task_id):
    """Update an existing task."""
    try:
        # Validate request data
        json_data = request.get_json()
        if not json_data:
            raise APIError("No input data provided", 400)

        # Get task from database
        task = get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise APIError("Task not found", 404)

        # Update task
        updated_task = update_task(task, json_data)
        result = task_schema.dump(updated_task)

        # Invalidate cache
        cache_delete('all_tasks')
        cache_delete(f'task_{task_id}')

        logger.info(f"Updated task {task_id}")
        return jsonify(result)
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        raise APIError("Failed to update task", 500)

@api_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    """Delete a task."""
    try:
        # Get task from database
        task = get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise APIError("Task not found", 404)

        # Delete task
        delete_task(task)

        # Invalidate cache
        cache_delete('all_tasks')
        cache_delete(f'task_{task_id}')

        logger.info(f"Deleted task {task_id}")
        return jsonify({'message': 'Task deleted'}), 200
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise APIError("Failed to delete task", 500)
