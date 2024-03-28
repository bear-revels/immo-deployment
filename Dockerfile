# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the Docker container
COPY ./api /app

# Expose the port on which your FastAPI application runs
EXPOSE 8000

# Command to run the FastAPI application within the Docker container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]