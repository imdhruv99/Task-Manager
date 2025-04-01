# Deploying with Kubernetes

This documentation covers the end-to-end setup and management of the **Task Manager** project using Kubernetes. The project is composed of several components like **Backend (Flask)**, **Frontend (React + Vite)**, **Redis**, **PostgreSQL**, and **NGINX Ingress Controller**.

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Kubernetes Cluster**: Ensure that you have a running Kubernetes cluster.
  - You can use a local Kubernetes environment like [Minikube](https://minikube.sigs.k8s.io/docs/) or [Docker Desktop](https://www.docker.com/products/docker-desktop) for testing.

- **kubectl**: Ensure you have access to `kubectl` and that it is connected to your Kubernetes cluster.
  - Install kubectl from [here](https://kubernetes.io/docs/tasks/tools/).

## Components Overview

This directory responsible for deploying the following components of the **Task Manager** application:

1. **Backend (Flask)**: A Flask based REST API.
2. **Frontend (Vite)**: A React and Vite based frontend application.
3. **Redis**: In-memory key-value store for caching.
4. **PostgreSQL**: Relational database for task management.
5. **NGINX Ingress Controller**: Handles ingress routing to both the frontend and backend.

The Kubernetes resources (e.g., deployments, services, ingress, PVCs, etc.) to run these components in your cluster.

## Setting Up

1. Apply the manifest files in given order.

    ```bash
    kubectl apply -f namespace.yaml

    kubectl apply -f postgres/*.yaml

    kubectl apply -f redis/*.yaml

    kubectl apply -f frontend/*.yaml

    kubectl apply -f backend/*.yaml
    ```

2. Check the Pod logs for each components, verify the services and all other configs.

    ```bash
    kubectl get all,cm,secrets -n task-manager
    ```

    ```bash
    kubectl logs -f <Pod Name> --tail=20 -n task-manager
    ```

    ```bash
    kubectl describe secrets <Secret Name> -n task-manager
    ```

3. Install and verify Nginx Ingress Controller, By default it comes with `LoadBalancer` as service type to use DNS, but since we are running for localhost, I have updated service type to `NodePort`.

    ```bash
    kubectl apply -f ingress-controller/*.yaml
    ```

    ```bash
    kubectl get all,cm,secrets -n ingress-nginx
    ```

4. Deploy Ingress resource.

    ```bash
    kubectl apply -f ingress.yaml
    ```

    ```bash
    kubectl get ingress -n task-manager
    ```

5. Get the Port from Ingress Controller NodePort Service and access web application.

    ```bash
    kubectl get svc -n ingress-nginx
    ```
    sample output:

    ```
    NAME                                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    ingress-nginx-controller             NodePort    10.104.82.212   <none>        80:31453/TCP,443:30442/TCP   9h
    ingress-nginx-controller-admission   ClusterIP   10.108.83.211   <none>        443/TCP                      9h
    ```

    > Access the WebApp on http port, since we do not have ssl setup as of now. In above case it would be `http://localhost:31453`


## Future Improvements
- In future updates, I plan to enhance the security of the application by following best practices. This will include implementing `NetworkPolicies`, `ServiceAccounts`, `RBAC`, as well as adding robust `Logging` and `Monitoring` features, along with any other necessary components for a production-grade application.
