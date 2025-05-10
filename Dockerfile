# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency list into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the ports needed for Flask
EXPOSE 5000

# Run the Flask Web UI
CMD ["sh", "-c", "python web-ui.py"]