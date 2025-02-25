FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application in development mode
RUN pip install -e .

# Make the startup script executable
RUN chmod +x start.sh

# Set environment variable that Cloud Run will use
ENV PORT 8080

# Expose the port
EXPOSE 8080

# Use the shell script that properly expands environment variables
CMD ["/bin/bash", "start.sh"]
