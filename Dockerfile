FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy startup script first and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Copy the rest of the application
COPY . .

# Install the application in development mode
RUN pip install -e .

# Set environment variable for local testing
ENV PORT 8080

# Use shell script to start the application
CMD ["/app/start.sh"]