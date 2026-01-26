from google.cloud import speech

def transcribe_audio(audio_file_path):
    """
    Transcribes the given audio file using Google Cloud Speech-to-Text.
    Assumes the file is local.
    """
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    
    # Configure request - assumes LINEAR16 based on our converter
    # If language is Japanese, set language_code="ja-JP"
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP",
        enable_automatic_punctuation=True,
    )

    # Detects speech in the audio file
    print(f"Transcribing {audio_file_path}...")
    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return "\n".join(transcript_parts)
