FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application in development mode
RUN pip install -e .

# Set environment variable that Cloud Run will use
ENV PORT 8080

# Command to run the application (note the port setting)
CMD ["streamlit", "run", "sales_register_analysis/app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]

# The container must listen on the port specified by the PORT environment variable
EXPOSE $PORT
