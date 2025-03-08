import os
from app import create_app

app = create_app()

if __name__ == '__main__':

    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('APP_ENV', 'development').lower() == 'development'

    app.run(host=host, port=port, debug=debug)
