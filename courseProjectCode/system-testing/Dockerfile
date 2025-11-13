# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

# Install mkdocs and pytest
RUN pip install --no-cache-dir mkdocs pytest requests

# Set default entrypoint to pytest
ENTRYPOINT ["pytest", "-v"]