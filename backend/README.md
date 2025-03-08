# Task Manager Backend

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
    # Application
    APP_ENV=development
    APP_PORT=5000

    # PostgreSQL
    POSTGRES_USER=taskapp
    POSTGRES_PASSWORD=taskapp_password
    POSTGRES_DB=taskmanagement
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    # Redis
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_PASSWORD=redis_password
    ```

-   Once done run below command from the backend directory
    ```
    python run.py
    ```

### Create docker image for kubernetes based deployment

-   Build the docker image
    ```
        docker build -t  <your-account-name>/task-management-backend:1.0.0 ./backend
    ```
-   Push docker image to remote repository
    ```
    docker push <your-account-name>/task-management-backend:1.0.0
    ```
