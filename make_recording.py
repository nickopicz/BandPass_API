import speech_recognition as sr

from gcloud import storage


from oauth2client.service_account import ServiceAccountCredentials


r = sr.Recognizer()
r.pause_threshold = 8000
# getting a recording
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout=2, phrase_time_limit=10)

with open("./audio_files/evi.wav", "wb") as f:
    f.write(audio.get_wav_data(convert_rate=48000))
