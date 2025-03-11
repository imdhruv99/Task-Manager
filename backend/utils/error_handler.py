import logging
from flask import jsonify

logger = logging.getLogger(__name__)

class APIError(Exception):
    """API Error Exception."""

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def configure_error_handlers(app):
    """Configure error handlers for the application."""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle API errors."""
        response = {
            'error': error.message
        }
        return jsonify(response), error.status_code

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle bad request errors."""
        response = {
            'error': 'Bad request'
        }
        return jsonify(response), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle not found errors."""
        response = {
            'error': 'Resource not found'
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle method not allowed errors."""
        response = {
            'error': 'Method not allowed'
        }
        return jsonify(response), 405

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Handle internal server errors."""
        logger.error(f"Internal server error: {str(error)}")
        response = {
            'error': 'Internal server error'
        }
        return jsonify(response), 500
