#!/bin/bash

# Print debug information
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"
echo "PORT environment variable: $PORT"

# Start Streamlit with explicit port configuration
# Note: order of arguments matters for Streamlit!
streamlit run sales_register_analysis/app.py --server.address=0.0.0.0 --server.port=$PORT