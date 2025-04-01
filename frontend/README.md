# Task Manager Fronend

- React + Vite based GUI for Task Manager

### Tools and Technology

| Index  | Tech Name   |
|---|---|
| Programming Language  | JavaScript  |
| Web Framework | React |
| Build Tool | Vite |
| API Integration | Axios |
| CSS | Tailwind |

### How to run Project

- Install the dependencies.
    ```bash
    npm install
    ```

- Create `.env` file.
    ```bash
    VITE_API_URL=http://localhost:5000/api/v1
    ```

- Run the application
    ```bash
    npm run build
    ```


### Create Docker Image

-   Build the docker image
    ```bash
    docker build -t  <your-account-name>/task-management-frontend:1.0.0 ./frontend
    ```
-   Push docker image to remote repository
    ```bash
    docker push <your-account-name>/task-management-frontend:1.0.0
    ```
