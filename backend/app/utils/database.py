import os
import psycopg2
import structlog

logger = structlog.get_logger(__name__)

def check_and_create_database(app):
    """
    Check if the database exists and create it if it doesn't.
    """
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST')
    db_port = os.getenv('POSTGRES_PORT')

    # Connect to PostgreSQL server
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            logger.info(f"Database {db_name} does not exist. Creating...")
            # Create database
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Database {db_name} created successfully")
        else:
            logger.info(f"Database {db_name} already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error checking/creating database: {str(e)}")
        raise
