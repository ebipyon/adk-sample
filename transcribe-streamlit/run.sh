#!/bin/bash
set -e

# Substitute PORT in nginx config


# Start Streamlit in the background (listen on localhost:8502)
# Run Streamlit directly on the port provided by Cloud Run
python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.maxUploadSize=5120
