# Use a base image with Python installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install system dependencies for speech recognition
RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Run the application
CMD ["python", "your_script_name.py"]
