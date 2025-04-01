# Task Manager

- The objective of this project is to design, develop, and deploy a full-stack Task Management Application that simulates a real-world microservice architecture. The application will be structured to reflect the complexities and interactions commonly found in modern microservice environments. The deployment process will be aligned with best practices to ensure that the system can be efficiently scaled, maintained, and managed in production environments.

### Development Process and Methodology Followed

- I began by setting up PostgreSQL and Redis using a Docker Compose-based configuration. Both databases utilize volumes to persist data, ensuring that the containers remain stateless and do not store data internally.

- I then proceeded with backend development, building a well-structured application using Python and Flask, integrated with Redis and PostgreSQL. I tested all the APIs using Postman. While the focus of the project was not on security implementation, the backend follows several industry-standard best practices to ensure maintainability and scalability.

- Once the backend was fully functional, I transitioned to frontend development, creating an application that consumes the backend APIs to manage tasks (create, read, update, and delete). I opted not to implement state management solutions like Redux to keep the frontend simple and avoid unnecessary complexity. For styling, I used Tailwind CSS, and instead of a Babel-based compiler, I utilized Vite for faster development. The frontend also follows many industry best practices to ensure clean and efficient code.

- Once the application was ready, I proceeded with dockerizing it using a multi-stage build along with Alpine images to minimize the size of the Docker images. To adhere to security best practices, I eliminated root access where necessary and created dedicated user and group for the application.

- Moving on to Kubernetes, I created all the manifests following the same best practices and security standards. There are additional implementations planned for the Kubernetes side, such as monitoring, logging, network policies, and other security measures.

- After testing everything on Kubernetes, I converted the Kubernetes manifests into a Helm chart to enable single-command deployment and streamlined component management.

### Database Setup and Startup

-   create `.env` file at root, this will have different values for host

    ```bash
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

    # Add below environment in case of Docker Compose based application deployment
    # Backend configuration
    FLASK_APP=app.py
    FLASK_ENV=development
    FLASK_DEBUG=1
    BACKEND_PORT=5000

    # Frontend configuration
    VITE_API_URL=http://localhost:5000/api
    ```

-   Run docker compose with below command
    ```bash
    docker compose up -d
    ```

### Docker Compose based Application Deployment

-  Append below blocks `docker-compose.yaml`.

    ```yaml
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

- Execute below command and wait for image creation and container creation
    ```bash
    docker-compose up -d backend frontend
    ```
    This command will start only the backend and frontend services, leaving the existing postgres and redis containers running as they were.
