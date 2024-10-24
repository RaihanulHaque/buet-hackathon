# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any dependencies
RUN pip install -r requirements.txt

# Command to run the app (optional for testing)
CMD ["python", "app.py"]
