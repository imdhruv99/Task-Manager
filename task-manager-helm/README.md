# Deploying with Helm Chart

This documentation covers the end-to-end setup and management of the **Task Manager** project using Helm. The project is composed of several components like **Backend (Flask)**, **Frontend (React + Vite)**, **Redis**, **PostgreSQL**, and **NGINX Ingress Controller**. Helm is used for deploying and managing these components in a Kubernetes cluster.


## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Kubernetes Cluster**: Ensure that you have a running Kubernetes cluster.
  - You can use a local Kubernetes environment like [Minikube](https://minikube.sigs.k8s.io/docs/) or [Docker Desktop](https://www.docker.com/products/docker-desktop) for testing.

- **Helm 3.x**: Helm is used to deploy and manage Kubernetes resources.
  - Install Helm from [here](https://helm.sh/docs/intro/install/).

- **kubectl**: Ensure you have access to `kubectl` and that it is connected to your Kubernetes cluster.
  - Install kubectl from [here](https://kubernetes.io/docs/tasks/tools/).


## Helm Chart Overview

This Helm chart is responsible for deploying the following components of the **Task Manager** application:

1. **Backend (Flask)**: A Flask based REST API.
2. **Frontend (Vite)**: A React and Vite based frontend application.
3. **Redis**: In-memory key-value store for caching.
4. **PostgreSQL**: Relational database for task management.
5. **NGINX Ingress Controller**: Handles ingress routing to both the frontend and backend.

The Helm chart templates and values files manage the Kubernetes resources (e.g., deployments, services, ingress, PVCs, etc.) to run these components in your cluster.


## Installation Steps

1. I have provided the demo values files, you can update everything inside those files according to your need, I have kept everything minimal.

2. Once you are done with creating values file, you can package the helm chart with below command

    ```bash
    cd task-manager-helm
    ```

    Update the dependency

    ```bash
    helm dependency update
    ```

    and then package the chart

    ```bash
    helm package .
    ```

    Output should looks like below...
    ```bash
    Successfully packaged chart and saved it to: <PATH of tgz file>
    ```

3. Once you've completed the packaging, you can run the `helm template` command. This will generate a single file containing all the Kubernetes resources, with their respective values pulled from the `values.yaml` file.

    ```bash
    # Run this command from root folder
    helm template task-manager-dev ./task-manager-helm -f task-manager-helm/values-development.yaml > rendered.yaml
    ```
    you can review every configs and manifest manually and then proceed with install

4. Execute below command to create resources in your kubernetes cluster

    ```bash
    helm install task-manager-dev ./task-manager-helm -f task-manager-helm/values-development.yaml
    ```
    > You can add `--debug` to log the installation process in STDIO, but it is not mandatory
    ```bash
    helm install task-manager-dev ./task-manager-helm -f task-manager-helm/values-development.yaml --debug
    ```

5. To verify that your Helm deployment was successful, use the following kubectl commands to check the status of your deployments:

    ```bash
    kubectl get pods -n task-manager-helm
    kubectl get svc -n task-manager-helm
    kubectl get ingress -n task-manager-helm
    ```

## Updating the Deployment

- To update your Helm deployment, modify the values.yaml file as required and use the helm upgrade command to apply the changes:

    ```bash
    helm upgrade task-manager-dev ./task-manager-helm -f task-manager-helm/values-development.yaml
    ```
    This command will update the resources in your cluster based on the changes you made to the `values.yaml` file.

## Uninstall Chart

- To uninstall the Helm release and remove the resources, use the following command:
    ```bash
    helm uninstall task-manager-dev
    ```
- This command will delete all resources associated with the Helm release from the Kubernetes cluster.


## Future Improvements
- In future updates, I plan to enhance the security of the application by following best practices. This will include implementing `NetworkPolicies`, `ServiceAccounts`, `RBAC`, as well as adding robust `Logging` and `Monitoring` features, along with any other necessary components for a production-grade application.
