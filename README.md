# Messenger App

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

![Architecture](https://img.shields.io/badge/architecture-Hybrid%20(Lambda%20%2B%20Fargate)-purple)
![Deployment](https://img.shields.io/badge/deployment-AWS%20%7C%20Terraform-232F3E)
![IaC](https://img.shields.io/badge/IaC-Terraform-623CE4)

![Backend](https://img.shields.io/badge/backend-Lambda%20%2B%20FastAPI-009688)
![Frontend](https://img.shields.io/badge/frontend-Angular-DD0031)
![Containerization](https://img.shields.io/badge/containers-Docker%20%7C%20Fargate-2496ED)

![Databases](https://img.shields.io/badge/databases-RDS%20%7C%20DynamoDB-336791)
![Storage](https://img.shields.io/badge/storage-S3-569A31)
![Authentication](https://img.shields.io/badge/authentication-Cognito-FF9900)
![Notifications](https://img.shields.io/badge/messaging-SNS%20%7C%20SQS-D854A1)

![Messenger App Dashboard](./assets/images/messenger-dashboard-screenshot.png)

## Table of Contents
- [About the Project](#about-the-project)
- [Features & Microservice Architecture](#features--microservice-architecture)
- [Technologies](#technologies)
- [AWS Infrastructure Overview](#aws-infrastructure-overview)
- [Deployment with Terraform](#deployment-with-terraform)
- [License](#license)

## About the Project
Messenger App is a web-based chat application allowing users to exchange text messages and media files. This version of the project has been re-architected into a **microservices-based system**, with each service independently deployable and scalable.
The application backend has been re-architected using **AWS Lambda** and **API Gateway**, with selected services (media, notifications, frontend) still running as containerized workloads on **ECS Fargate**. All resources are managed using **Terraform**, forming a hybrid serverless-containerized architecture focused on scalability, simplicity and modularity.

## Features & Microservice Architecture

Messenger App is a cloud-native application built with a microservice architecture to deliver a scalable and resilient chat experience. Key features are supported by dedicated, independently deployable services:

*   📨 **Messaging & Chat Management:**
    *   Handled by a set of **AWS Lambda functions** behind **API Gateway**.
    *   Uses AWS RDS PostgreSQL for persistent chat storage.
*   📁 **Media File Handling:**
    *   Support for sending, receiving, and storing media files.
    *   Managed by the **Media Service**, utilizing AWS S3 for file storage and DynamoDB for metadata.
*   🔐 **User Authentication & Authorization:**
    *   Secure user registration, login, and session management powered by **AWS Cognito**.
    *   Validated by the **API Gateway Service**.
*   🔔 **Event-Based Notifications:**
    *   Events like "new message" are published from Lambda functions to **AWS SQS**.
    *   **Notification Service** (on ECS) consumes these events and triggers **SNS notifications** and stores metadata in **DynamoDB**.
*   ⚙️ **API Orchestration & Frontend Delivery:**
    *   **API Gateway (HTTP API)** acts as the public-facing gateway, validating Cognito JWT and invoking Lambda functions.
    *   **Frontend Service** (Angular SPA) is containerized and deployed via **ECS Fargate**, integrated with Cognito OIDC flow.
*   ☁️ **Cloud-Native Foundation:**
    *   All services are **Dockerized** and deployed on **AWS ECS Fargate** for serverless container orchestration.
    *   Each service benefits from **Application Auto Scaling** and a minimum of two replicas for high availability.
    *   The entire infrastructure is defined and managed using **Terraform (IaC)**.
    *   Logs are centralized in **AWS CloudWatch Logs**.

## Technologies
| Component                | Technologies & AWS Services                         |
|--------------------------|-----------------------------------------------------|
| **Frontend**             | Angular, Bootstrap, Docker                          |
| **API Gateway**          | AWS API Gateway, Lambda Proxy Integration           |
| **Chat Service**         | AWS Lambda (Python), FastAPI logic, AWS RDS         |
| **Media Service**        | Python, FastAPI, Docker, AWS S3, DynamoDB           |
| **Notification Service** | Python, FastAPI, Docker, AWS SNS, DynamoDB, SQS     |
| **Authentication**       | AWS Cognito (User Pools, App Clients)               |
| **Containerization**     | Docker                                              |
| **Orchestration**        | AWS ECS Fargate, Application Auto Scaling           |
| **Load Balancing**       | AWS Application Load Balancer (ALB)                 |
| **Infrastructure (IaC)** | Terraform                                           |
| **Logging**              | AWS CloudWatch Logs                                 |
| **Networking**           | AWS VPC, Subnets, Security Groups, Internet Gateway |
| **Container Registry**   | AWS ECR (Elastic Container Registry)                |

## AWS Infrastructure Overview
The application's cloud infrastructure, managed by Terraform, leverages the following core AWS services:

-   **Networking (VPC):** A custom Virtual Private Cloud providing network isolation, configured with public subnets.
-   **Load Balancing (ALB):** ALB is used only for Fargate services (frontend, media, notification). Public-facing HTTPS is handled by ALB (frontend) and **API Gateway** (for Lambda endpoints).
-   **Container Orchestration (ECS & Fargate):** Used for non-Lambda services (media, notification, frontend). All other business logic is implemented as AWS Lambda functions.
-   **Serverless Backend (Lambda):** Stateless Python-based functions handling chats, messages, and user actions.
-   **API Gateway (HTTP API):** Low-latency gateway that forwards HTTP requests to Lambda functions and validates Cognito JWT tokens.
-   **Event-Driven Messaging (SQS → SNS):** Lambda functions publish events to SQS queues; backend services consume them and send SNS notifications to subscribed users.
-   **Container Registry (ECR):** Dedicated ECR repositories for storing Docker images of each microservice.
-   **Databases:**
    *   **RDS PostgreSQL:** For `chat-service` data.
    *   **DynamoDB:** For `media-service` metadata and `notification-service` history.
-   **Storage (S3):** An S3 bucket for media file storage.
-   **Messaging (SNS):** An SNS topic for user notifications.
-   **Identity (Cognito):** Integrated with API Gateway for token validation and frontend login via OIDC flow.
-   **Security & Access (IAM):** Roles and policies, including the ECS Task Execution Role, to manage permissions.

## Deployment with Terraform

The entire cloud infrastructure is provisioned and managed using Terraform. The code is organized into reusable modules (`terraform/modules/`) orchestrated by the root `main.tf`.

1.  **Prerequisites:** Ensure AWS CLI is configured and Terraform is installed.
2.  **Build & Push Docker Images:** BBuild Docker images for containerized services (`frontend`, `media-service`, `notification-service`).
3.  **Initialize Terraform:** Navigate to the Terraform root directory (e.g., `terraform/`) and run `terraform init`.
4.  **Plan Changes:** Execute `terraform plan -out=tfplan` to review the planned infrastructure changes.
5.  **Apply Changes:** Run `terraform apply tfplan` to create or update the AWS resources.

## License
This project is licensed under the terms of the MIT License. See the [LICENSE](./LICENSE) file for details.
