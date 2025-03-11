import logging
import sys
import structlog
from flask import request, g
import time
import os
from datetime import datetime

def configure_logging(app):
    """Configure logging for the application."""

    # Ensure log directory exists
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Get the current date in ISO format for the log file name (e.g., 2025-03-11)
    log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
    log_file = os.path.join(log_dir, log_filename)

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Configure file handler for logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to the root logger
    logging.getLogger().addHandler(file_handler)

    # Configure structlog
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

    # Request logging
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if request.path.startswith('/api'):
            now = time.time()
            duration = round(now - g.start, 2)
            log = structlog.get_logger()
            log.info(
                "request_handled",
                method=request.method,
                path=request.path,
                status=response.status_code,
                duration=duration,
                ip=request.remote_addr,
                agent=request.user_agent.string
            )
        return response
