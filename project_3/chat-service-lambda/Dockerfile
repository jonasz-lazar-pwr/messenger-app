# === Stage 1: Build dependencies in a compatible Lambda environment ===
FROM public.ecr.aws/lambda/python:3.11 AS builder

# Install system-level dependencies needed to compile packages
RUN yum install -y gcc postgresql-devel

# Set working directory inside the container
WORKDIR /var/task

# Copy requirements file and install Python dependencies to /opt/python
COPY chat-service-lambda/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt -t /opt/python

# === Stage 2: Prepare the final ZIP package in /tmp ===
FROM alpine:3.18 AS packager

# Install zip utility
RUN apk add --no-cache zip

# Copy installed Python packages from the builder stage
COPY --from=builder /opt/python /tmp/lambda-package/

# Copy source code into the packaging directory
WORKDIR /tmp/lambda-package
COPY chat-service-lambda/handlers handlers
COPY chat-service-lambda/shared shared
COPY chat-service-lambda/*.py .

# Create ZIP archive with all source files and dependencies
RUN zip -r9 /tmp/messenger-app-chat-service.zip .

# === Stage 3: Export the final ZIP artifact ===
FROM scratch AS export
COPY --from=packager /tmp/messenger-app-chat-service.zip /messenger-app-chat-service.zip