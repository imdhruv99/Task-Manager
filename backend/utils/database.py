import logging
from sqlalchemy import inspect
from models import db

logger = logging.getLogger(__name__)

def check_db_exists(app, db_name):
    """Check if database exists."""
    try:
        engine = db.get_engine(app)
        conn = engine.connect()
        conn.close()
        logger.info(f"Database '{db_name}' exists")
        return True
    except Exception as e:
        logger.error(f"Database '{db_name}' does not exist: {str(e)}")
        return False

def check_table_exists(model):
    """Check if table exists."""
    try:
        inspector = inspect(db.engine)
        table_name = model.__tablename__
        if table_name in inspector.get_table_names():
            logger.info(f"Table '{table_name}' exists")
            return True
        logger.warning(f"Table '{table_name}' does not exist")
        return False
    except Exception as e:
        logger.error(f"Error checking table: {str(e)}")
        return False

def init_database(app):
    """Initialize database."""
    try:
        with app.app_context():
            # Create database tables
            db.create_all()
            logger.info("Database tables created")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False
