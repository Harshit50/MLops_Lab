# Base image with Python 3.10
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the source code into the container
COPY src/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run when the container starts
CMD ["python", "main.py"]