# 🎬 YouTube Video Summarizer App

A Streamlit web app that summarizes YouTube videos by extracting transcripts and generating concise summaries using AI models like Google's Gemini.

## 🚀 Features

- 📥 Accepts YouTube video URL input
- 🧠 Extracts video transcript automatically
- ✍️ Summarizes content into key points (under 300 words)
- 🖼️ Displays video thumbnail
- 🧪 Clean, interactive UI using Streamlit

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Transcription:** yt-dlp / Whisper
- **Summarization:** Google Gemini Pro
- **Environment Variables:** `dotenv`

---

## 📦 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/yt-video-summarizer.git
   cd yt-video-summarizer

   ```

2. **Create and activate virtual environment:**
   python -m venv venv
   venv\Scripts\activate # On Windows

3. **Install Dependecies**
   pip install -r requirements.txt

4. **Setup Environment Variable:**
   Create a .env file and add your Gemini API key:
   GOOGLE_API_KEY=your_gemini_api_key
   FFmpeg (must be installed and added to PATH): https://ffmpeg.org/download.html
5. **RUN THE APP**

   streamlit run app.py
