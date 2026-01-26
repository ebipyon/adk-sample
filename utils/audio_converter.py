import os
from pydub import AudioSegment

def convert_to_linear16(input_path):
    """
    Converts audio to 16000Hz mono WAV (LINEAR16) which is ideal for Google Cloud Speech.
    Returns the path to the converted file.
    """
    try:
        audio = AudioSegment.from_file(input_path)
        
        # Set frame rate to 16000Hz and channels to 1 (mono)
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Export as wav
        output_path = os.path.splitext(input_path)[0] + "_converted.wav"
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        # Return original if conversion fails, though it might fail in STT
        return input_path
