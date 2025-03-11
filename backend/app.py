from flask import Flask
from flask_cors import CORS
from models import db
from api import api_blueprint
from utils.logging import configure_logging
from utils.error_handler import configure_error_handlers
from config import config

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configure logging
    configure_logging(app)

    # Initialize extensions
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api/v1/')

    # Configure error handlers
    configure_error_handlers(app)

    return app
