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

1. Install NGINX Ingress Controller (Cluster-Scoped)
Deploy the ingress controller in a dedicated namespace (`ingress-nginx`). This is a **one-time setup** for your cluster.

    ```bash
    # Add the ingress-nginx Helm repository
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    ```
    ```bash
    # Install the ingress controller with NodePort (for local clusters)
    helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.service.type=NodePort

    # For cloud providers (AWS/GCP/Azure), use LoadBalancer instead: --set controller.service.type=LoadBalancer (default is this so no need to change)
    ```

2. Then update values.yaml files according to your need, after that you can package the helm chart with below command

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
    helm install task-manager-dev task-manager-helm -f task-manager-helm/values-development.yaml --namespace task-manager-helm --create-namespace
    ```
    > You can add `--debug` to log the installation process in STDIO, but it is not mandatory
    ```bash
    helm install task-manager-dev task-manager-helm -f task-manager-helm/values-development.yaml --namespace task-manager-helm --create-namespace --debug
    ```

5. To verify that your Helm deployment was successful, use the following kubectl commands to check the status of your deployments:

    ```bash
    kubectl get pods -n task-manager-helm
    kubectl get svc -n task-manager-helm
    kubectl get ingress -n task-manager-helm
    ```

6. Accessing the application
    ```bash
    kubectl get svc -n ingress-nginx
    ```
    this will give output similar to below
    ```
    NAME                                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             NodePort    10.107.125.98   <none>        80:31464/TCP,443:30291/TCP   23m
    ingress-nginx-controller-admission   ClusterIP   10.106.57.224   <none>        443/TCP                      23m
    ```
    Take port from `ingress-nginx-controller`, in above case it's `31464` and access `http://localhost:31464` and you should be able to access the application.

## Updating the Deployment

- To update your Helm deployment, modify the values.yaml file as required and use the helm upgrade command to apply the changes:

    ```bash
    helm upgrade task-manager-dev ./task-manager-helm -f task-manager-helm/values-development.yaml --namespace task-manager-helm --create-namespace --debug
    ```
    This command will update the resources in your cluster based on the changes you made to the `values.yaml` file.

## Uninstall Chart

- To uninstall the Helm release and remove the resources, use the following command:
    ```bash
    helm uninstall task-manager-dev --namespace task-manager-helm
    ```
- This command will delete all resources associated with the Helm release from the Kubernetes cluster.

---
**Note:** Helm does not automatically create namespaces, and it is not recommended to manage namespace creation through Helm templates.
https://github.com/helm/helm/issues/4456#issuecomment-412134651

## Future Improvements
- In future updates, I plan to enhance the security of the application by following best practices. This will include implementing `NetworkPolicies`, `ServiceAccounts`, `RBAC`, as well as adding robust `Logging` and `Monitoring` features, along with any other necessary components for a production-grade application.
