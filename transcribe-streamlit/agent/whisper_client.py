import whisper
import os

def transcribe_with_whisper(audio_file_path: str, model_size: str = "small") -> str:
    """
    Transcribes the given audio file using OpenAI's Whisper model locally.
    
    Args:
        audio_file_path: Path to the local audio file.
        model_size: Size of the Whisper model to use (tiny, base, small, medium, large).
        
    Returns:
        The transcribed text.
    """
    print(f"Loading Whisper model: {model_size}...")
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = whisper.load_model(model_size, device=device)
    
    print(f"Transcribing {audio_file_path} with Whisper...")
    result = model.transcribe(audio_file_path, language="ja")
    
    return result["text"]
