# Use the official Python 3.10 image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt if you have any dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (if needed)
EXPOSE 8000

# Command to run your application (replace with the actual start command of your app)
CMD ["python", "app.py"]
