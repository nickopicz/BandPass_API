import speech_recognition as sr

from gcloud import storage


from oauth2client.service_account import ServiceAccountCredentials


r = sr.Recognizer()
r.pause_threshold = 8000
# getting a recording
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout=2)

with open("evi.wav", "wb") as f:
    f.write(audio.get_wav_data())
