# Use official Python 3.11 image with Alpine for a lightweight base
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the list of dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full application source code into the container
COPY . .

# Define the default command to run the notification-service
CMD ["python", "main.py"]