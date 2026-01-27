#!/bin/bash
set -e

# Configuration
# Please set these variables or ensure they are set in your environment
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"speech-to-text-sample-485505"}
BUCKET_NAME=${GCS_BUCKET_NAME:-"speech-to-text-sample-485505-audio-temp"}
REGION="asia-northeast1"
SERVICE_NAME="adk-transcription-agent"
REPO_NAME="adk-sample"
IMAGE_TAG="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/transcription-agent:latest"

echo "Deploying to Project: $PROJECT_ID"
echo "Region: $REGION"

# 1. Enable APIs
echo "Enabling APIs..."
gcloud services enable artifactregistry.googleapis.com run.googleapis.com speech.googleapis.com

# 2. Service Account (Check if exists first or ignore error)
echo "Creating Service Account..."
gcloud iam service-accounts create adk-transcription-sa --display-name="ADK Transcription SA" || echo "Service account might already exist."

# 3. Grant Permissions
echo "Granting IAM roles..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:adk-transcription-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/speech.client"

# 4. Create Artifact Registry (Check if exists or ignore error)
echo "Creating Artifact Registry repository..."
gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION || echo "Repository might already exist."

# 5. Build and Push
echo "Building and pushing image..."
gcloud builds submit --tag $IMAGE_TAG

# 6. Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_TAG \
    --platform managed \
    --region $REGION \
    --memory 4Gi \
    --cpu 2 \
    --timeout 600 \
    --allow-unauthenticated \
    --use-http2 \
    --gpu 1 \
    --gpu-type nvidia-l4 \
    --no-cpu-throttling \
    --service-account adk-transcription-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GCS_BUCKET_NAME=$BUCKET_NAME

echo "Deployment Complete!"
