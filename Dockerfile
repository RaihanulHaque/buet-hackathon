# Dockerfile

FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application using Gunicorn (optional, can also run Flask in debug mode for testing)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]  # or you can use "python app.py" if you prefer
