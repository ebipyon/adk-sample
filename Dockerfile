FROM python:3.9-slim

# Install system dependencies (ffmpeg is required for pydub/audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port (Cloud Run uses PORT env var)
EXPOSE 8501

# Default PORT for local dev, Cloud Run will override
ENV PORT=8501

# Run Streamlit with dynamic port
CMD streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
