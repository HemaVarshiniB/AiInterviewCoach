import google.generativeai as genai
import os  # For environment variables
import io
import base64

# Load your API key from an environment variable (more secure than hardcoding)
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"  # Replace with your actual API key

# Configure the Gemini API
genai.configure(api_key="AIzaSyCgCTGjBH-LOI-u4cS9lfqbTooL1Jpc0Pw")

# Select the Gemini Flash 2.0 model
model = genai.GenerativeModel('gemini-1.5-flash')  # 'gemini-1.5-flash-latest' is also an option

def process_audio(audio_file_path, prompt):
    """Processes the audio file with Gemini Flash 2.0 and returns the text response."""

    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Prepare the prompt with the audio data
        contents = [
            {"mime_type": "audio/wav", "data": audio_data}, # Ensure your audio is WAV format or change the mime type
            prompt
        ]

        # Generate content with the model
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None



if __name__ == "__main__":
    audio_file = "your_audio.wav"  # Replace with the path to your audio file
    user_prompt = "Summarize the key points of this audio."  # Your specific prompt

    result = process_audio(audio_file, user_prompt)

    if result:
        print("Gemini Flash 2.0 response:")
        print(result)
    else:
        print("Audio processing failed.")