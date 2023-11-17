# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye as build

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Set the working directory in the container to /report-hub
WORKDIR /report-hub

COPY requirements.txt .
COPY requirements-test.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt

COPY ./app /report-hub/app
COPY ./tests /report-hub/tests

# Run tests
RUN pytest --disable-warnings -vv

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

# Set the working directory in the container to /report-hub
WORKDIR /report-hub

COPY --from=build --chown=fastapi:fastapi /report-hub/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=fastapi:fastapi log_conf.yml /report-hub
COPY --from=build --chown=fastapi:fastapi /report-hub/app /report-hub/app

# Switch to the non-root user
USER fastapi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "log_conf.yml"]