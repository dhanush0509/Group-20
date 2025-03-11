# YourTTS Zero-Shot Voice Cloning with Sentiment Conditioning in voice

%pip install TTS yt-dlp transformers pydub

import os
from pydub import AudioSegment
from transformers import pipeline
from yt_dlp import YoutubeDL

# Download audio from YouTube
video_url = input("Enter YouTube video URL for voice cloning: ")
output_filename = "yourtts_voice_sample.mp3"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_filename,
    'quiet': False
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# Convert MP3 to WAV,  16kHz
audio = AudioSegment.from_file(output_filename)
audio = audio.set_channels(1).set_frame_rate(16000)
audio.export("yourtts_voice_sample.wav", format="wav")

# Get user text input
user_text_input = input("Enter the text you want the cloned voice to say: ")

# Analyze sentiment
sentiment_analyzer = pipeline("sentiment-analysis")
sentiment = sentiment_analyzer(user_text_input)[0]
print(f"Sentiment detected: {sentiment['label']} with confidence {sentiment['score']:.2f}")

# Set emotion conditioning based on sentiment
emotion_mapping = {
    "POSITIVE": "Happy",
    "NEGATIVE": "Sad",
    "NEUTRAL": "Neutral"
}

emotion = emotion_mapping.get(sentiment['label'], "Neutral")
print(f"Emotion applied: {emotion}")


from TTS.api import TTS

# Load YourTTS model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

# Generate speech with speaker reference and sentiment-based tone
output_file = "yourtts_cloned_voice.wav"
tts.tts_to_file(
    text=user_text_input,
    speaker_wav="yourtts_voice_sample.wav",
    language="en",
    file_path=output_file
)


import IPython.display as ipd

# Play the result
ipd.Audio(output_file)
