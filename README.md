# Messenger App
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![AWS Deployment](https://img.shields.io/badge/deployed-AWS-232F3E)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![Frontend](https://img.shields.io/badge/frontend-Angular-DD0031)
![Docker](https://img.shields.io/badge/containerized-Docker-2496ED)
![Infrastructure as Code](https://img.shields.io/badge/IaC-Terraform-623CE4)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791)
![Storage](https://img.shields.io/badge/storage-S3-569A31)
![Authentication](https://img.shields.io/badge/authentication-Cognito-FF9900)

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [License](#license)

## About the Project
Messenger App is a simple web-based chat application that allows users to participate in conversations by sending text messages and media files.

This project is designed with a modular architecture, separating the frontend and backend into independent services.
It focuses on delivering a functional, user-friendly, and scalable chat experience deployed in the cloud.

## Features
- 📨 **Real-time Messaging** - Users can exchange text messages within conversations.
- 📁 **Media File Uploads** - Support for sending and receiving media files via the chat interface.
- 🔐 **User Authentication** - Secure login and session management powered by AWS Cognito.
- 🛠️ **Modular Architecture** - Separation of concerns between the Angular frontend and FastAPI backend.
- ☁️ **Cloud Deployment** - Full deployment on AWS infrastructure using Elastic Beanstalk, RDS, S3, and CloudWatch.
- 🐳 **Dockerized Services** - Both frontend and backend are containerized using Docker for easy deployment.
- 🏗️ **Infrastructure as Code** - Terraform used for automating the provisioning of cloud infrastructure.
- 📊 **Monitoring and Logging** - Application and infrastructure logs collected and monitored through AWS CloudWatch.
- 🛡️ **Secure Media Storage** - Uploaded media files are securely stored in AWS S3 buckets.
- 🧩 **RESTful API** - Backend provides a clean and well-structured RESTful API for frontend communication.

## Architecture
- **Frontend** - Developed using **Angular**, the frontend delivers a responsive SPA that communicates with the backend via REST API. It also manages the OAuth2-based authentication flow with AWS Cognito.
- **Backend** - Powered by **FastAPI**, the backend handles user authentication, conversation management, message processing, and file uploads. It secures all API endpoints using JWT tokens issued by AWS Cognito.
- **Authentication** - User authentication and authorization are managed via **AWS Cognito**, providing secure, scalable identity management.
- **Database** - Persistent storage for users, conversations, and messages is provided by a **PostgreSQL** database hosted on **Amazon RDS**.
- **Media Storage** - Media files exchanged between users are securely stored in **AWS S3** buckets.
- **Deployment** - Both frontend and backend services are containerized using **Docker** and deployed independently on **AWS Elastic Beanstalk** environments.
- **Infrastructure Management** - The entire AWS infrastructure (Elastic Beanstalk, RDS, S3, CloudWatch, VPC) is provisioned and managed through **Terraform**, embracing Infrastructure as Code (IaC) practices.

## Technologies
| Part               | Technologies                                     |
|--------------------|--------------------------------------------------|
| **Frontend**       | Angular, Bootstrap, Docker                       |
| **Backend**        | Python, FastAPI, SQLAlchemy, Docker              |
| **Authentication** | AWS Cognito                                      |
| **Database**       | PostgreSQL (Amazon RDS)                          |
| **Storage**        | AWS S3                                           |
| **Infrastructure** | Terraform, AWS Elastic Beanstalk, AWS CloudWatch |

## Deployment
The deployment process for the Messenger App is fully automated using **Terraform**:

1. **Infrastructure Provisioning**  
   Terraform scripts located in the `config/terraform/` directory automate the creation of all necessary AWS resources.  
   Running `terraform apply` provisions the entire cloud environment, including VPC, RDS, S3, CloudWatch, Cognito, and Elastic Beanstalk environments.

2. **Application Deployment**  
   Both the frontend and backend are containerized using Docker and deployed independently to AWS Elastic Beanstalk environments.

3. **Configuration Management**  
   Application environment variables, database connection strings, and AWS credentials are securely managed through Elastic Beanstalk environment settings.

## Documentation
A full report and technical documentation of the project can be found [here](./docs/Messenger%20App%20-%20Report.pdf).

## License
This project is licensed under the terms of the MIT License. See the [LICENSE](./LICENSE) file for details.
