from google.cloud import speech
from pydub import AudioSegment
import os
from utils.gcs_helper import upload_blob, delete_blob

GCS_BUCKET_NAME = "speech-to-text-sample-485505-audio-temp"

def transcribe_audio(audio_file_path):
    """
    Transcribes the given audio file using Google Cloud Speech-to-Text.
    Uses synchronous recognize for short files (< 60s) and 
    LongRunningRecognize with GCS for longer files.
    """
    client = speech.SpeechClient()
    
    # Check duration
    audio_segment = AudioSegment.from_file(audio_file_path)
    duration_seconds = audio_segment.duration_seconds
    
    # Configure request
    # If language is Japanese, set language_code="ja-JP"
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP",
        enable_automatic_punctuation=True,
    )

    if duration_seconds > 60:
        print(f"Audio is {duration_seconds:.2f}s long. Using LongRunningRecognize with GCS.")
        
        # Upload to GCS
        file_name = os.path.basename(audio_file_path)
        gcs_uri = upload_blob(GCS_BUCKET_NAME, audio_file_path, file_name)
        
        audio = speech.RecognitionAudio(uri=gcs_uri)
        
        try:
            print(f"Starting LongRunningRecognize for {gcs_uri}...")
            operation = client.long_running_recognize(config=config, audio=audio)
            
            print("Waiting for operation to complete...")
            response = operation.result(timeout=None) # Wait indefinitely (or set a reasonable timeout)
            
        finally:
            # Delete from GCS
            delete_blob(GCS_BUCKET_NAME, file_name)
            
    else:
        print(f"Audio is {duration_seconds:.2f}s long. Using synchronous recognize.")
        
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        
        print(f"Transcribing {audio_file_path}...")
        response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return "\n".join(transcript_parts)
