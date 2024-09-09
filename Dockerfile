# Copyright (c) 2024 by Jonathan AW
# Use Python base image
FROM python:3.10-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the entire project into the container's `/app` directory
COPY . /app

# Install net-tools for netstat
RUN apt-get update && apt-get install -y net-tools

# Install Poetry
RUN pip install poetry 

# Install necessary dependencies for debugging
RUN poetry add debugpy

# Configure Poetry to avoid creating a virtual environment (since Docker containers already provide isolation)
RUN poetry config virtualenvs.create false 

# Install dependencies using Poetry
RUN poetry install --no-dev

# Ensure all installed packages are on the Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Copy the wait-for-it script into the root directory of the container
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Note: We've removed the CMD instruction as it's now specified in docker-compose.yml
# CMD ["bash", "-c", "./wait-for-it.sh db:5432 -- poetry run python bin/__init_sys_database.py && \
#                         poetry run python bin/__data_prep_administrators.py && \
#                         poetry run python bin/__data_prep_supported_schemes.py && \
#                         poetry run python bin/__data_prep_random_applicants.py && \
#                         poetry run python bin/__data_prep_applications.py && \
#     if [ \"$FLASK_DEBUG\" = \"1\" ]; then poetry run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run --no-reload --host=$FLASK_RUN_HOST --port=$FLASK_RUN_PORT; else poetry run flask run --host=$FLASK_RUN_HOST --port=$FLASK_RUN_PORT; fi"]