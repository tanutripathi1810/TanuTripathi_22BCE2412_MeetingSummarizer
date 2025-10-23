## 🚀 Project Objective

This project delivers a web application designed to automate the transcription and analysis of meeting audio. It utilizes powerful, free-to-use models to produce a full text transcript and an action-oriented summary, focusing on **key decisions** and **action items**.

The application is built using **Python Flask** for the web interface, the open-source **OpenAI Whisper** model for local transcription, and the **Google Gemini API (Free Tier)** for advanced natural language processing.

***

## ✨ Key Features

* **File Upload:** Simple HTML frontend allows users to upload standard audio formats (MP3, WAV, M4A, FLAC).
* **ASR Transcription:** Leverages **OpenAI Whisper** for high-accuracy, resource-efficient local Speech-to-Text conversion.
* **LLM Summarization:** Uses the **Gemini 2.5 Flash** model with a specific prompt structure to ensure output is strictly formatted into:
    1.  A concise **Summary** paragraph.
    2.  A list of **Key Decisions**.
    3.  A list of **Action Items/Tasks**.
* **Download Feature:** Users can download the structured summary as a clean `.txt` file directly from the results page.
* **Security:** Sensitive API keys are managed using the `.env` file and `python-dotenv`, and uploaded files are deleted immediately after processing.

***
## 🛠️ Technical Stack

| Component | Technology | Role | Cost |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML5, Jinja2 (Flask Templates) | User Interface for upload and results display. | Free |
| **Backend** | Flask (Python) | Routes, File Handling, Orchestration. | Free |
| **Transcription (ASR)** | **OpenAI Whisper** (`openai-whisper` package) | Speech-to-Text conversion. | Free (Local Run) |
| **Summarization (LLM)**| **Google Gemini API** (`gemini-2.5-flash`) | NLP for structured summarization and task extraction. | Free Tier |
| **Deployment** | Docker, Gunicorn (Recommended) | Containerization for consistent deployment. | Free-to-Start |
## ⚙️ Setup and Installation

Follow these steps to get the application running on your local machine.

### Step 1: Clone Repository & Create Environment

```bash
# 1. Clone your repository (replace with your actual link)
git clone [https://github.com/YOUR_USERNAME/meeting-summarizer-app.git](https://github.com/YOUR_USERNAME/meeting-summarizer-app.git)
cd meeting-summarizer-app

# 2. Create and activate a Python virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\activate
```
### Step 2: Install System Dependency (FFmpeg)
The Whisper model relies on FFmpeg to process audio files. You must install this tool globally on your system.

- Windows (via Chocolatey): choco install ffmpeg (or download and add to PATH)

- macOS (via Homebrew): brew install ffmpeg

- Linux (Debian/Ubuntu): sudo apt update && sudo apt install ffmpeg

### Step 3: Install Python Dependencies
Install the required packages within your active virtual environment:
```
Bash

pip install -r requirements.txt
```
(Your requirements.txt should contain: openai-whisper, google-genai, pydub, python-dotenv, Flask)

### Step 4: Configure Gemini API Key
1. Get Key: Obtain your Gemini API Key from [Google AI Studio].

2. Create .env: Create a new file named .env in the root of the project directory.

3. Add Key: Paste your key inside the file:
```
GEMINI_API_KEY="YOUR_API_KEY_STRING_GOES_HERE"
```

## ▶️ Running the Application
1. Ensure your virtual environment is active.

2. Start the Flask server from the project root:
```
Bash

python app.py
```
3. Open your web browser and navigate to: http://127.0.0.1:5000/

## 📂 Project Structure
This structure demonstrates a clear separation of concerns:
```
meeting-summarizer/
├── app.py              # Flask server, routes, file I/O, download logic.
├── summarizer.py       # Core logic: Whisper ASR, LLM prompting (free of Flask dependencies).
├── requirements.txt    # All Python dependencies.
├── .env                # Stores API key securely.
├── .gitignore          # Prevents venv, .env, and uploads from Git.
├── Dockerfile          # Container setup for deployment.
├── frontend/           # Custom template directory used by Flask.
│   └── index.html      # Frontend (Upload form, results display, download button).
└── uploads/            # Temporary directory for uploaded audio (ignored by Git).
```
