# Use PyTorch base image with CUDA support
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Install system dependencies (ffmpeg is required for pydub/audio processing)
# Also install nginx and gettext-base (for envsubst)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nginx \
    gettext-base \
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
