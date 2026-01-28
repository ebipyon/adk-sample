# Use lightweight Python base image (CPU only)
FROM python:3.9-slim

# Install system dependencies (ffmpeg is required for pydub/audio processing)
# Also install nginx and gettext-base (for envsubst)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and nginx config
COPY . .

# Expose Streamlit port (Cloud Run uses PORT env var)
EXPOSE 8501

# Default PORT for local dev, Cloud Run will override
ENV PORT=8501

# Run wrapper script
CMD ["./run.sh"]
