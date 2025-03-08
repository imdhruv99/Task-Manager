# Task Manager

-   Three tier application deployment demo on kubernetes to understand and get grip on kubernetes.

### Local Development

-   create `.env` file at root, this will have different values for host

    ```
    ### ENV FILE FOR DOCKER COMPOSE ###

    # Application
    APP_ENV=development
    APP_PORT=5000

    # PostgreSQL
    POSTGRES_USER=taskapp
    POSTGRES_PASSWORD=taskapp_password
    POSTGRES_DB=taskmanagement
    POSTGRES_HOST=postgres # this will be localhost in backend directory, here it's service name of docker since we want to run app as container
    POSTGRES_PORT=5432

    # Redis
    REDIS_HOST=redis # this will be localhost in backend directory, here it's service name of docker since we want to run app as container
    REDIS_PORT=6379
    REDIS_PASSWORD=redis_password

    # Frontend
    VITE_API_URL=http://localhost:5000/api
    ```

-   Run docker compose with below command
    ```
    docker compose up -d
    ```
-   Once done follow the instruction from backend/README.md and frontend/README.md.
-   You can also run backend and frontend as container with the help of below command, pass root `.env` which you created for docker compose. since you are running application in docker make sure it's in same network as postgre and redis.

    ```
    docker run -it -d --name tm-frontend -p 80:80 --env-file .env --network task-management_app-network <your-account-name>/task-management-frontend:1.0.0
    ```

    ```
    docker run -it -d --name tm-backend -p 5000:5000 --env-file .env --network task-management_app-network <your-account-name>/task-management-backend:1.0.0
    ```
