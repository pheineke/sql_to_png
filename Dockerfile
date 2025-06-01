# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install fontconfig and common fonts first to ensure they are available
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY app.py .
COPY templates ./templates

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py with Gunicorn when the container launches
# Gunicorn will serve the Flask app named 'app' in the 'app.py' file
# Listening on all interfaces (0.0.0.0) on port 5000, with 4 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "-w", "4", "app:app"]
