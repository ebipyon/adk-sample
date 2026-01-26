import streamlit as st
import os

# Set Google Cloud Project ID explicitly
os.environ["GOOGLE_CLOUD_PROJECT"] = "speech-to-text-sample-485505"

import tempfile
from agent.speech_client import transcribe_audio
from agent.whisper_client import transcribe_with_whisper
from utils.audio_converter import convert_to_linear16
from utils.diff_helper import generate_diff_html
import streamlit.components.v1 as components

st.set_page_config(page_title="Audio Transcription Agent", page_icon="🎙️", layout="wide")

st.title("🎙️ Audio Transcription Agent")
st.write("Upload an audio file to transcribe using Google Cloud Speech-to-Text and Local Whisper.")

uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    col1, col2 = st.columns(2)
    with col1:
        model_size = st.selectbox("Whisper Model Size", ["tiny", "base", "small", "medium", "large"], index=2)
    
    if st.button("Transcribe"):
        with st.spinner("Processing..."):
            try:
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Convert for Google STT (and normalize for Whisper if needed)
                converted_path = convert_to_linear16(tmp_file_path)

                # --- Google Cloud STT ---
                st.write("---")
                st.subheader("1. Google Cloud Speech-to-Text")
                with st.spinner("Transcribing with Google Cloud..."):
                    google_text = transcribe_audio(converted_path)
                st.success("Google Cloud Transcription Complete")

                # --- Local Whisper ---
                st.write("---")
                st.subheader("2. Local Whisper")
                with st.spinner(f"Transcribing with Whisper ({model_size})..."):
                    # Whisper can take the original file, but converted is also fine (16k wav)
                    whisper_text = transcribe_with_whisper(converted_path, model_size=model_size)
                st.success("Whisper Transcription Complete")

                # --- Display Results Side-by-Side ---
                st.write("---")
                st.subheader("Results Comparison")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.text_area("Google Cloud STT", google_text, height=300)
                with res_col2:
                    st.text_area("Local Whisper", whisper_text, height=300)

                # --- Diff ---
                st.write("---")
                st.subheader("Diff Analysis")
                diff_html = generate_diff_html(google_text, whisper_text)
                components.html(diff_html, height=600, scrolling=True)

                # Cleanup
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                if os.path.exists(converted_path) and converted_path != tmp_file_path:
                    os.remove(converted_path)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
