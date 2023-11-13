# Dockerfile for dev and pro environments

# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos '' fastapi \
    && pip install --upgrade pip

# Switch to the non-root user
USER fastapi

# Set the working directory in the container to /app
WORKDIR /app

COPY --chown=fastapi:fastapi requirements.txt .

# COPY the current directory contents into the container at /app
COPY --chown=fastapi:fastapi ./app .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "log_conf.yml"]