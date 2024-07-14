# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# first install poetry in the docker container
RUN pip3 install poetry

# poetry doesn't need a virtualenv INSIDE a docker container
RUN poetry config virtualenvs.create false

# Copy over dependencies before code so this step can be cached
COPY poetry.lock pyproject.toml /app/

RUN poetry install --without dev

# Copy the source code into the container.
COPY . .

# Change the ownership of the entrypoint.sh file to the appeaser user
RUN chown appuser:appuser /app/entrypoint.sh
# Set the execute permission for the entrypoint.sh file
RUN chmod +x /app/entrypoint.sh

# Switch to the non-privileged user to run the application.
USER appuser

CMD ["/bin/bash", "/app/entrypoint.sh"]