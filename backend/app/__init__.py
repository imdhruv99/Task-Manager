import os
import logging
import structlog
from flask import Flask
from flask_cors import CORS
from alembic.config import Config
from alembic import command
from flask_migrate import Migrate, upgrade

from config import get_config
from app.extensions import db, migrate, redis_client
from app.utils.database import check_and_create_database

logger = structlog.get_logger(__name__)

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

    # Migration handling
    with app.app_context():
        # Ensure models are imported
        from app.models.task import Task

        # Initialize migrations only once
        migrations_dir = os.path.join(app.root_path, '..', 'migrations')
        env_py_path = os.path.join(migrations_dir, 'env.py')

        # Create migrations folder if needed
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir, exist_ok=True)

        # Initialize migrations only if env.py doesn't exist
        if not os.path.exists(env_py_path):
            try:
                from flask_migrate import init
                logger.info("Initializing migrations directory")
                init(directory=migrations_dir)
            except Exception as e:
                if "already exists" not in str(e):
                    logger.error("Migrations init failed", error=str(e))
                    raise

        # Generate initial migration if needed
        versions_dir = os.path.join(migrations_dir, 'versions')
        if not os.path.exists(versions_dir) or not os.listdir(versions_dir):
            try:
                from flask_migrate import migrate
                logger.info("Generating initial migration")
                migrate(directory=migrations_dir, message='Initial migration')
            except Exception as e:
                logger.error("Migration generation failed", error=str(e))
                raise

        # Apply migrations
        if app.config.get('AUTO_MIGRATE', False):
            try:
                from flask_migrate import upgrade
                logger.info("Applying database migrations")
                upgrade(directory=migrations_dir)
            except Exception as e:
                logger.error("Migration upgrade failed", error=str(e))
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
