#!/bin/bash
set -e

# Substitute PORT in nginx config
envsubst '${PORT}' < nginx.conf.template > /etc/nginx/nginx.conf

# Start Streamlit in the background (listen on localhost:8502)
streamlit run app.py --server.port=8502 --server.address=127.0.0.1 &

# Start Nginx in the foreground
nginx -g 'daemon off;'
