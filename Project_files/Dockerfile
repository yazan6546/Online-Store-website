# Start with a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /Project_files

# Copy everything (including requirements.txt) into the image first
COPY . .

# Install system build dependencies and Python dependencies in one RUN command
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    python3-dev \
    build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

# Set the command to run your app
CMD ["python", "store.py"]

