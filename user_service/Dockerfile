# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code into the container
COPY user_service.py .

# Expose the service port
EXPOSE 5000

# Run the service
CMD ["python", "user_service.py"]
