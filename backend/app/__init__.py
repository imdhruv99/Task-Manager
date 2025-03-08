import logging
import structlog
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, upgrade

from config import get_config
from app.extensions import db, migrate, redis_client
from app.utils.database import check_and_create_database


def setup_logging():
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )

def create_app():
    """Application factory pattern."""
    # Configure logging
    setup_logging()

    # Create and configure the app
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)

    # Initialize extensions
    register_extensions(app)

    # Configure CORS
    CORS(app)

    # Check and create database if it doesn't exist
    check_and_create_database(app)

    # Auto-apply migrations in development
    if app.config.get('AUTO_MIGRATE', False):
        with app.app_context():
            try:
                upgrade()
            except Exception as e:
                raise

    # Register API blueprints
    register_blueprints(app)

    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)

    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.api.v1 import api_bp

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return None
