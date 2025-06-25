# import streamlit as st
# import os
# import uuid
# import whisper
# from dotenv import load_dotenv
# from urllib.parse import urlparse, parse_qs
# import google.generativeai as genai
# from yt_dlp import YoutubeDL

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Gemini Prompt
# prompt = """You are an expert video summarizer. Your task is to analyze the full transcript of a YouTube video and generate a clear, concise summary of the key points discussed.

# Please follow these instructions:

# - Summarize the video in bullet points or numbered lists.
# - Highlight the most important information, facts, or insights.
# - Avoid filler or redundant content.
# - Keep the summary within 700 words.
# - Use simple and readable language.

# Transcript starts here:
# """

# # Extract video ID from URL
# def get_video_id(youtube_url):
#     query = urlparse(youtube_url)
#     if query.hostname == 'youtu.be':
#         return query.path[1:]
#     if query.hostname in ('www.youtube.com', 'youtube.com'):
#         if query.path == '/watch':
#             return parse_qs(query.query).get('v', [None])[0]
#         if query.path.startswith('/embed/'):
#             return query.path.split('/')[2]
#     return None

# # Download audio using yt-dlp (only works locally)
# def download_audio(video_url, output_dir="downloads"):
#     os.makedirs(output_dir, exist_ok=True)
#     unique_id = str(uuid.uuid4())
#     output_path = os.path.join(output_dir, f"{unique_id}.mp3")

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': output_path,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }

#     try:
#         with YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#         if not os.path.exists(output_path):
#             print("[ERROR] File not found after download.")
#             return None
#         return output_path
#     except Exception as e:
#         print("yt-dlp Python error:", str(e))
#         return None

# # Transcribe audio with Whisper
# def transcribe_audio(audio_path):
#     if not os.path.exists(audio_path):
#         raise FileNotFoundError(f"Audio file not found: {audio_path}")
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path)
#     return result["text"]

# # Generate summary using Gemini
# def generate_gemini_content(transcript_text, prompt):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt + transcript_text)
#     return response.text


# # ... (all your imports and functions remain unchanged)

# # Streamlit App UI
# st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")
# st.markdown("## 🎥 YouTube Video Summarizer")
# st.markdown("Paste a YouTube link or upload an audio file to get a summary powered by Whisper + Gemini.")

# mode = st.radio("Choose input method:", ["YouTube URL", "Upload MP3 File"])

# audio_file = None

# if mode == "YouTube URL":
#     youtube_link = st.text_input("📌 Enter YouTube video URL")
#     if youtube_link:
#         video_id = get_video_id(youtube_link)
#         if video_id:
#             st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_container_width=True)
#         if st.button("Summarize", key="yt_summarize"):
#             with st.spinner("🔊 Downloading audio..."):
#                 audio_file = download_audio(youtube_link)
#                 if not audio_file:
#                     st.error("❌ Failed to download audio. This may be a protected YouTube video or unsupported format. Try another link or upload an MP3.")

# elif mode == "Upload MP3 File":
#     uploaded_file = st.file_uploader("Upload an MP3 file", type="mp3")
#     if uploaded_file is not None:
#         temp_dir = "temp_audio"
#         os.makedirs(temp_dir, exist_ok=True)
#         audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
#         with open(audio_path, "wb") as f:
#             f.write(uploaded_file.read())
#         audio_file = audio_path

# # Processing the audio if available
# if audio_file:
#     try:
#         with st.spinner("🧠 Transcribing using Whisper..."):
#             transcript_text = transcribe_audio(audio_file)

#         with st.spinner("✍️ Generating summary with Gemini..."):
#             summary = generate_gemini_content(transcript_text, prompt)
#             st.markdown("## 📝 Detailed Summary:")
#             st.write(summary)
#     except Exception as e:
#         st.error(f"❌ Failed during transcription or summarization: {e}")

#     if os.path.exists(audio_file):
#         os.remove(audio_file)
# else:
#     # fallback button (different key)
#     if st.button("Summarize", key="fallback_summarize"):
#         st.error("❌ No audio file to process. Upload an MP3 or enter a valid YouTube URL.")



import streamlit as st
import os
import uuid
import whisper
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are an expert video summarizer. Your task is to analyze the full transcript of a YouTube video and generate a clear, concise summary of the key points discussed.

Please follow these instructions:

- Summarize the video in bullet points or numbered lists.
- Highlight the most important information, facts, or insights.
- Avoid filler or redundant content.
- Keep the summary within 700 words.
- Use simple and readable language.

Transcript starts here:
"""

# Transcribe audio with Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Generate summary using Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App UI
st.set_page_config(page_title="MP3 Summarizer", layout="centered")
st.markdown("## 🎧 MP3 Audio Summarizer")
st.markdown("Upload an MP3 audio file (from lectures, podcasts, etc.) and get a clean summary powered by Whisper + Gemini.")

uploaded_file = st.file_uploader("📤 Upload an MP3 file", type="mp3")

if uploaded_file is not None:
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        with st.spinner("🧠 Transcribing using Whisper..."):
            transcript_text = transcribe_audio(audio_path)

        with st.spinner("✍️ Generating summary with Gemini..."):
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## 📝 Summary:")
            st.write(summary)

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")

    # Clean up
    os.remove(audio_path)
