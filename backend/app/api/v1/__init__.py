from flask import Blueprint
from app.api.v1.tasks import tasks_bp

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Register endpoints
api_bp.register_blueprint(tasks_bp, url_prefix='/tasks')

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}
