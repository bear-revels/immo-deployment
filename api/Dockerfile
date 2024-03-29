# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8000 to allow communication to/from the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]