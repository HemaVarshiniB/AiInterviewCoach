# utils/audioHelper.py

import requests
import sounddevice as sd
from scipy.io.wavfile import write
import re

VAPI_API_KEY = "3cb0ead9-07b7-4ad5-98a3-651cf8792d5e"  # Replace with your actual Vapi API key
def speak_text(text, filename="response.mp3"):
    """Convert text to speech using Vapi TTS and save as MP3."""
    url = "https://api.vapi.ai/api/text-to-speech"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_id": "voice_olivia_us",
        "output_format": "mp3"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        audio_url = response.json().get("audio_url")
        audio_data = requests.get(audio_url).content
        with open(filename, "wb") as f:
            f.write(audio_data)
        return filename
    else:
        print("TTS Error:", response.text)
        return None

def record_audio(duration=5, filename="response.wav", fs=16000):
    """Record audio from microphone and save to 16kHz mono WAV."""
    print("🎤 Recording started...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, audio_data)
    print("✅ Recording complete")
    return filename

import re
from google.cloud import texttospeech

def clean_text_for_tts(text):
    # Remove asterisks, commas, and full stops
    cleaned = re.sub(r'[*.,]', '', text)
    # Optionally, remove other unwanted symbols or extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def speak_text(text, filename="response.mp3"):
    text = clean_text_for_tts(text)
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    return filename

from google.cloud import speech
import io

def speech_to_text(audio_file="response.wav"):
    client = speech.SpeechClient()
    with io.open(audio_file, "rb") as audio:
        content = audio.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""
