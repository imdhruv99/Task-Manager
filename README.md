# Task Manager

-   Three tier application deployment demo on kubernetes to understand and get grip on kubernetes.

### Local Development

-   create `.env` file at root, this will have different values for host

    ```
    ### ENV FILE FOR DOCKER COMPOSE ###

    # Database configuration
    POSTGRES_USER=taskapp
    POSTGRES_PASSWORD=taskpassword
    POSTGRES_DB=taskmanagement
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

    # Redis configuration
    REDIS_HOST=redis
    REDIS_PORT=6379

    # Backend configuration
    FLASK_APP=app.py
    FLASK_ENV=development
    FLASK_DEBUG=1
    BACKEND_PORT=5000

    # Frontend configuration
    VITE_API_URL=http://localhost:5000/api
    ```

-   Run docker compose with below command
    ```
    docker compose up -d
    ```
-   Once done follow the instruction from backend/README.md and frontend/README.md.
-   You can also run backend and frontend as container with the help of below command, pass root `.env` which you created for docker compose. since you are running application in docker make sure it's in same network as postgre and redis.

    ```
    docker run -it -d --name tm-frontend -p 80:80 --env-file .env --network task-management_app-network <your-account-name>/task-manager-frontend:1.0.0
    ```

    ```
    docker run -it -d --name tm-backend -p 5000:5000 --env-file .env --network task-management_app-network <your-account-name>/task-manager-backend:1.0.0
    ```

    OR, you can add below block of code in compose and run it again with `docker compose up -d`

    ```
      # Backend Service
        backend:
            build:
            context: ./backend
            dockerfile: Dockerfile
            container_name: task_backend
            restart: always
            ports:
            - "${BACKEND_PORT}:5000"
            environment:
            - FLASK_APP=${FLASK_APP}
            - FLASK_ENV=${FLASK_ENV}
            - FLASK_DEBUG=${FLASK_DEBUG}
            - POSTGRES_USER=${POSTGRES_USER}
            - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            - POSTGRES_DB=${POSTGRES_DB}
            - POSTGRES_HOST=${POSTGRES_HOST}
            - POSTGRES_PORT=${POSTGRES_PORT}
            - REDIS_HOST=${REDIS_HOST}
            - REDIS_PORT=${REDIS_PORT}
            depends_on:
            postgres:
                condition: service_healthy
            redis:
                condition: service_healthy
            volumes:
            - ./backend:/app

        # Frontend Service
        frontend:
            build:
            context: ./frontend
            dockerfile: Dockerfile
            container_name: task_frontend
            restart: always
            ports:
            - "3000:3000"
            environment:
            - VITE_API_URL=${VITE_API_URL}
            depends_on:
            - backend
            volumes:
            - ./frontend:/app
            - /app/node_modules
    ```
