import speech_recognition as sr

from gcloud import storage

from google.cloud import speech

import soundfile as sf

from oauth2client.service_account import ServiceAccountCredentials
import re
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./speech-recog-363719-f9d84d991d98.json"


# r = sr.Recognizer()
# r.pause_threshold = 8000
# # getting a recording
# with sr.Microphone() as source:
#     print("Say something!")
#     audio = r.listen(source, timeout=2, phrase_time_limit=10)

# with open("./audio_files/evi.wav", "wb") as f:
#     f.write(audio.get_wav_data(convert_rate=48000))


def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)

    results = response.results

    confidences = []

    for i in results:
        temp = re.findall(r'\d+', str(i.alternatives[0]))
        confidences.append(float(".".join(temp)))

    max_idx = confidences.index(max(confidences))

    

    return response.results[max_idx].alternatives[0].transcript


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(f"Transcript: {transcript}")
        print(f"Confidence: {confidence:.0%}")


language_code = "en-US"

# Sample rate in Hertz of the audio data sent
sample_rate_hertz = 48000

# Encoding of audio data sent. This sample sets this explicitly.
# This field is optional for FLAC and WAV audio formats.

config = {
    "language_code": language_code,
    "sample_rate_hertz": sample_rate_hertz,
}

with io.open("./audio_files/evi.wav", "rb") as f:
    content = f.read()
audio = {"content": content}


speech_to_text(config, audio)
