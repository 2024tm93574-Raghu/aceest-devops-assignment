# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose Flask port
EXPOSE 5000

# Environment variable for Flask
ENV FLASK_APP=app.py

# Run the app
CMD ["python", "app.py"]
