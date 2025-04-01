# Task Manager Backend

- Flask based REST API for Task Manager

### Tools and Technology

| Index  | Tech Name   |
|---|---|
| Programming Language  | Python  |
| Web Framework | Flask |
| Database | PostgreSQL |
| Caching | Redis |
| ORM | SQLAlchemy, Marshmallow, Flask-SQLAlchemy |

### Prerequisites

-   Create Virtual Environment
    ```
    python -m venv venv
    ```
-   Enable the virtual environment
    ```
    source venv/bin/activate # for Unix
    ```
    ```
    source venv/Scripts/activate # for windows
    ```
-   Install required libraries
    ```
    python -m requirements.txt
    ```

### Steps to run the project

-   Make sure you have postgre and redis database running, either as docker container or locally configured.
-   Create `.env` file as given below in the backend folder.

    ```
        # Database configuration
        POSTGRES_USER=taskapp
        POSTGRES_PASSWORD=taskpassword
        POSTGRES_DB=taskmanagement
        POSTGRES_HOST=localhost
        POSTGRES_PORT=5432

        # Redis configuration
        REDIS_HOST=localhost
        REDIS_PORT=6379

        # Backend configuration
        FLASK_APP=app.py
        FLASK_ENV=development
        FLASK_DEBUG=1
        BACKEND_PORT=5000
    ```

-   Once done run below command from the backend directory.

    ```
    python wsgi.py
    ```

-   Postman collection available so you can export it and execute the apis.

### Create docker image for kubernetes based deployment

-   Build the docker image
    ```
        docker build -t  <your-account-name>/task-management-backend:1.0.0 ./backend
    ```
-   Push docker image to remote repository
    ```
    docker push <your-account-name>/task-management-backend:1.0.0
    ```
