FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application in development mode
RUN pip install -e .

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "sales_register_analysis/app.py", "--server.address=0.0.0.0"]
