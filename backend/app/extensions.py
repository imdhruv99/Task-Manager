from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

# SQLAlchemy for ORM
db = SQLAlchemy()

# Flask-Migrate for database migrations
migrate = Migrate()

# Redis client for caching
class RedisClient:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        self.client = redis.from_url(app.config['REDIS_URL'])

redis_client = RedisClient()
