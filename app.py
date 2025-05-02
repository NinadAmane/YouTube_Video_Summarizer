# import streamlit as st
# import os
# from dotenv import load_dotenv
# from youtube_transcript_api import YouTubeTranscriptApi
# load_dotenv() #this will load all the environment variables
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt = """you are a youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 300 words. 
# Please provide the transcript summary here: """


# #GETTING THE TRANSCRIPT FROM YT VIDEO
# def extract_transcript_detail(youtube_video_url):
#     try:
#         video_id= youtube_video_url.split("=")[1]
#         print(video_id)
#         transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

#         transcript = ""
#         for i in transcript_text:
#             transcript += " " + i["text"]

#         return transcript

#     except Exception as e:
#         raise e



# #GETTING THE SUMMARY BASED ON PROMPT FROM GOOGLE GEMINI
# def generate_gemini_content(transcript_text,prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(prompt+transcript_text)
#     return response.text

# st.title("🎬 YouTube Video Summarizer")
# youtube_link = st.text_input("Enter YouTube video url: ")

# if youtube_link:
#     video_id = youtube_link.split("=")[1]
#     print(video_id)
#     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_column_width=True)


# if st.button("Summarize"):
#     transcript_text = extract_transcript_detail(youtube_link)

#     if transcript_text:
#         summary = generate_gemini_content(transcript_text, prompt)
#         st.markdown("## DETAILED SUMMARY: ")
#         st.write(summary)

import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are an expert video summarizer. Your task is to analyze the full transcript of a YouTube video and generate a clear, concise summary of the key points discussed.

Please follow these instructions:

Summarize the video in bullet points or numbered lists.

Highlight only the most important information, facts, or insights.

Avoid filler or redundant content.

Keep the summary within 500 words.

Use simple and readable language.

Transcript starts here:"""

# Extract video ID from various YouTube URL formats
def get_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query).get('v', [None])[0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
    return None

# Get transcript using video ID
def extract_transcript_detail(video_id):
    try:
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

# Use Gemini to summarize transcript
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title("🎬 YouTube Video Summarizer")
youtube_link = st.text_input("Enter YouTube video URL:")

if youtube_link:
    video_id = get_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_column_width=True)

        if st.button("Summarize"):
            transcript_text = extract_transcript_detail(video_id)
            if "Error" not in transcript_text:
                summary = generate_gemini_content(transcript_text, prompt)
                st.markdown("## 📝 Detailed Summary:")
                st.write(summary)
            else:
                st.error(transcript_text)
    else:
        st.warning("Invalid YouTube link. Please enter a proper URL.")
