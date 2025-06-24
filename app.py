# import streamlit as st
# import os
# from dotenv import load_dotenv
# from youtube_transcript_api import YouTubeTranscriptApi
# import google.generativeai as genai
# from urllib.parse import urlparse, parse_qs

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt = """You are an expert video summarizer. Your task is to analyze the full transcript of a YouTube video and generate a clear, concise summary of the key points discussed.

# Please follow these instructions:

# Summarize the video in bullet points or numbered lists.

# Highlight only the most important information, facts, or insights.

# Avoid filler or redundant content.

# Keep the summary within 500 words.

# Use simple and readable language.

# Transcript starts here:"""

# # Extract video ID from various YouTube URL formats
# def get_video_id(youtube_url):
#     query = urlparse(youtube_url)
#     if query.hostname == 'youtu.be':
#         return query.path[1:]
#     if query.hostname in ('www.youtube.com', 'youtube.com'):
#         if query.path == '/watch':
#             return parse_qs(query.query).get('v', [None])[0]
#         if query.path[:7] == '/embed/':
#             return query.path.split('/')[2]
#     return None

# # Get transcript using video ID
# def extract_transcript_detail(video_id):
#     try:
#         transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = " ".join([i["text"] for i in transcript_text])
#         return transcript
#     except Exception as e:
#         return f"Error fetching transcript: {str(e)}"

# # Use Gemini to summarize transcript
# def generate_gemini_content(transcript_text, prompt):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt + transcript_text)
#     return response.text

# # Streamlit UI
# st.title("🎬 YouTube Video Summarizer")
# youtube_link = st.text_input("Enter YouTube video URL:")

# if youtube_link:
#     video_id = get_video_id(youtube_link)
#     if video_id:
#         st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_column_width=True)

#         if st.button("Summarize"):
#             transcript_text = extract_transcript_detail(video_id)
#             if "Error" not in transcript_text:
#                 summary = generate_gemini_content(transcript_text, prompt)
#                 st.markdown("## 📝 Detailed Summary:")
#                 st.write(summary)
#             else:
#                 st.error(transcript_text)
#     else:
#         st.warning("Invalid YouTube link. Please enter a proper URL.")


import streamlit as st
import os
import subprocess
import uuid
import whisper
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini
prompt = """You are an expert video summarizer. Your task is to analyze the full transcript of a YouTube video and generate a clear, concise summary of the key points discussed.

Please follow these instructions:

- Summarize the video in bullet points or numbered lists.
- Highlight only the most important information, facts, or insights.
- Avoid filler or redundant content.
- Keep the summary within 500 words.
- Use simple and readable language.

Transcript starts here:
"""

# Extract video ID
def get_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [None])[0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
    return None

# Download audio using yt-dlp
def download_audio(video_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(output_dir, f"{unique_id}.mp3")

    yt_dlp_path = r"C:\Python313\Scripts\yt-dlp.exe"  # Your yt-dlp path
    ffmpeg_path = r"D:\YT_VIDEO_SUMMARIZER\ffmpeg\ffmpeg-7.1.1-essentials_build\bin"  # Your ffmpeg folder path

    try:
        result = subprocess.run(
            [
                yt_dlp_path,
                "-x", "--audio-format", "mp3",
                "--ffmpeg-location", ffmpeg_path,   # 👈 pass the ffmpeg path
                "-o", output_path,
                video_url
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("yt-dlp output:\n", result.stdout)
        return output_path
    except subprocess.CalledProcessError as e:
        print("yt-dlp error:\n", e.stderr)
        return None


# Transcribe using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path)
    return result["text"]

# Gemini Summarizer
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit App
st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")
st.markdown("## 🎥 YouTube Video Summarizer")
st.markdown("Paste a YouTube link below and get a clean summary powered by Whisper + Gemini.")

youtube_link = st.text_input("📎 Enter YouTube video URL")

if youtube_link:
    video_id = get_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_column_width=True)

        if st.button("Summarize"):
            with st.spinner("🔊 Downloading audio..."):
                audio_file = download_audio(youtube_link)

            if audio_file:
                with st.spinner("🧠 Transcribing using Whisper..."):
                    transcript_text = transcribe_audio(audio_file)

                with st.spinner("✍️ Generating summary with Gemini..."):
                    summary = generate_gemini_content(transcript_text, prompt)
                    st.markdown("## 📝 Detailed Summary:")
                    st.write(summary)

                os.remove(audio_file)  # Clean up
            else:
                st.error("Failed to download audio. Please check the video link.")
    else:
        st.warning("Invalid YouTube link.")
