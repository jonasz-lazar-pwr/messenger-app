# Build stage – install dependencies
FROM python:3.11-alpine AS build-stage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building packages like psycopg2-binary
RUN apk add --no-cache gcc musl-dev libpq-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage – cleaner and smaller image
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add only runtime dependencies
RUN apk add --no-cache libpq

WORKDIR /app

# Copy installed dependencies and binaries from build stage
COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin

# Copy application source code
COPY . .

# Expose port
EXPOSE 80

# Remove pip cache (cleanup)
RUN rm -rf /root/.cache

# Default command to start media-service
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]