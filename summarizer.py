import whisper
from google import genai
from google.genai.errors import APIError
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Uses the 'base' model for faster local transcription. 
# You can use 'small', 'medium', or 'large' for better accuracy if you have a GPU.
WHISPER_MODEL_SIZE = "base"
GEMINI_MODEL = "gemini-2.5-flash" 

class MeetingSummarizer:
    def __init__(self):
        """Initializes the Whisper model and Gemini Client."""
        print(f"Loading Whisper model: {WHISPER_MODEL_SIZE}...")
        try:
            # Load the local Whisper model
            self.asr_model = whisper.load_model(WHISPER_MODEL_SIZE)
        except Exception as e:
            print(f"Error loading Whisper model: {e}. Check FFmpeg installation.")
            self.asr_model = None

        # Initialize the Gemini Client
        self.gemini_client = None
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            self.gemini_client = genai.Client(api_key=gemini_api_key)
        else:
            print("GEMINI_API_KEY not found in .env file. Summarization will fail.")

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribes the meeting audio file using the local Whisper model.
        
        Input: Path to the audio file (e.g., MP3, M4A, WAV).
        Output: The full text transcript.
        """
        if not self.asr_model:
            return "Transcription failed due to model loading error."

        print(f"Starting transcription for {audio_path}...")
        try:
            # The transcribe function handles all audio formats supported by FFmpeg
            result = self.asr_model.transcribe(audio_path)
            transcript = result["text"]
            print("Transcription complete.")
            return transcript
        except Exception as e:
            print(f"Transcription error: {e}")
            return f"Error during transcription: {e}"

    def summarize_transcript(self, transcript: str) -> dict:
        """
        Generates summary, key decisions, and action items using the Gemini LLM.
        
        Input: The full text transcript.
        Output: A dictionary containing the Summary, Decisions, and Action Items.
        """
        if not self.gemini_client:
            return {"error": "LLM client not initialized. Check API Key."}

        # --- LLM Prompt Example ---
        prompt = f"""
        Analyze the following meeting transcript. Your output must be in JSON format
        with three top-level keys: 'summary', 'key_decisions', and 'action_items'.

        1.  'summary': A concise paragraph summarizing the entire meeting.
        2.  'key_decisions': A numbered list of all finalized decisions made in the meeting.
        3.  'action_items': A numbered list of all tasks assigned, clearly stating the task
            and the person responsible (if mentioned), or 'TBD' if not.

        TRANSCRIPT:
        ---
        {transcript}
        ---
        """

        print("Starting summarization and action item generation...")
        
        try:
            response = self.gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json" # Enforce JSON output
                }
            )
            
            # The response text will be a JSON string
            import json
            summary_data = json.loads(response.text)
            print("Summarization complete.")
            return summary_data

        except APIError as e:
            print(f"Gemini API Error: {e}")
            return {"error": f"LLM API Error: {e}"}
        except json.JSONDecodeError:
            print("Error decoding JSON from LLM response.")
            return {"error": "LLM did not return valid JSON."}
        except Exception as e:
            print(f"An unexpected error occurred during summarization: {e}")
            return {"error": f"Unexpected error: {e}"}

# --- Demo Usage ---
if __name__ == "__main__":
    
    # 1. Ensure you have an audio file in the 'data' folder
    TEST_AUDIO_PATH = "data/meeting_audio.mp3" 
    
    if not os.path.exists(TEST_AUDIO_PATH):
        print(f"Error: Test audio file not found at {TEST_AUDIO_PATH}.")
        print("Please place a sample audio file there to test.")
    else:
        # Initialize
        summarizer = MeetingSummarizer()
        
        # 2. Transcribe
        transcript_text = summarizer.transcribe_audio(TEST_AUDIO_PATH)
        
        if "Error" in transcript_text:
            print("\n--- Transcription Failed ---")
            print(transcript_text)
        else:
            print("\n--- Full Transcript (Partial View) ---")
            print(transcript_text[:500] + "...")
            
            # 3. Summarize
            summary_output = summarizer.summarize_transcript(transcript_text)

            print("\n--- Summary and Action Items ---")
            if "error" in summary_output:
                print(summary_output["error"])
            else:
                print("\n## Summary")
                print(summary_output.get("summary", "N/A"))
                
                print("\n## Key Decisions")
                for i, decision in enumerate(summary_output.get("key_decisions", [])):
                    print(f"- {decision}")
                    
                print("\n## Action Items")
                for i, action in enumerate(summary_output.get("action_items", [])):
                    print(f"- {action}")