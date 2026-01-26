import streamlit as st
import os
import tempfile
from agent.speech_client import transcribe_audio
from utils.audio_converter import convert_to_linear16

st.set_page_config(page_title="Audio Transcription Agent", page_icon="🎙️")

st.title("🎙️ Audio Transcription Agent")
st.write("Upload an audio file to transcribe using Google Cloud Speech-to-Text.")

uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            try:
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Convert if necessary (Google Cloud STT prefers specific formats)
                # For simplicity, we'll try to convert everything to WAV LINEAR16 mono
                st.info("Processing audio format...")
                converted_path = convert_to_linear16(tmp_file_path)

                # Transcribe
                st.info("Sending to Google Cloud...")
                transcript = transcribe_audio(converted_path)
                
                st.success("Transcription Complete!")
                st.text_area("Transcript", transcript, height=300)

                # Cleanup
                os.remove(tmp_file_path)
                if converted_path != tmp_file_path:
                    os.remove(converted_path)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
