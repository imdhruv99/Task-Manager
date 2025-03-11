import os
from app import create_app

# Get environment
env = os.environ.get('FLASK_ENV', 'default')

# Create app
app = create_app(env)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
