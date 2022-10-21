import speech_recognition as sr
from google.cloud import speech
from google.oauth2 import service_account

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = "c:/users/nicko/spr/microphone_results.wav"
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")


credentials_dict = {
    "type": "service_account",
    "project_id": "speech-recog-363719",
    "private_key_id": "5d0d5205a97a0f3a30801319f4b79fbbfbe91b17",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDnaT81pjBfGBtd\nqYyQ9MCu2ZbfGvAxIjh4CxL/ayN/rO0mHB1le+yoYvKyZNHQXO3P2CsxJdznZJit\nvHq0vP7W+r3zW+adnjkgvNiJyPakpkWHEiVpJ2wzchSIstWCctWPRjIz5xMX8py9\nArer3R9JT2JpOzhD17o3R2LgxOb/djNfJo482nB3BfXpEwmCsY5uDviIVJ7saeo/\nwz9ZzVfh7HlnhUEX7WQGLDogoE1h/UZh0FEGeXcgo7oZDIeJppK7/9M9EsVfHY/6\ntCLrW3/JmRy3dfqdj/Gd38nyiJUClqvSmJA1TUgMTS1A+WW+O+5FgQpxyFvFHzNg\neYXwOvCNAgMBAAECggEAB4pa6G0fY2HeNmmZbnnDM49chq2SiQ9T5rl5p3/+uqDQ\nY28EGDP3DK+Yt+5oFdGJYD3rfmD89z9EaFjdaLlF1ox6Fw12EMnAk8wDhE3bl5bh\nahrRxEDoGi8L8z5cjbEfO1lutlk/uoaJy/DkOkHszI89Ji+rUC6d30JAuxE/c7B+\n8BxPwYAOCeNKs+VExY7w2TlPQ0UThjbFFenShiA4DGrnlfzTUb/flFPns2Fc1CV0\nd5FthuvjERZECi+hQ5CJh0v8Dkg5HH8/7ApGP1wcjT9OtMyQ/TmHGnoWN0519KiA\nK4EnJMYwUFpCjuspAcuSJ+R1rMkfi/E7plb+S3x68QKBgQD+vr0/BQDwE8einfTw\nhnp3OJDHKWUkZct8MNQseVArjCSXWSeEJryv6q+DIFMWwCp4Y2n/jkSwXuppBYA0\n+LIpwBX+6T9hZMO4jvhVoq6UFt20kHyEnI4iCcbUbqbqr3bFqQuRsAf9Ne32STLn\nq8nwpYQDb0NYt7E1yR2CFCAWyQKBgQDojRTAWIoEgBgxdx3HIQ1iWlYntgvawNgs\n4e49+raS7zsGkmw03xDGyMXlqNfEgcgujYwCMCttY//KOBc1HOBhF4s0BKw0AA/T\njMvkGsdspOcrAGairwIhkx2cdVrkCCVfxzY+mrBkmzQCYT31xpzpusRv0F/uAYc2\nw7J9t+25pQKBgQCfQIp6PRyK+TKSPIEFZGxm35vShdRO3rxI1RWu/9/YeXHek8Oa\nX8URjHtQVALddCCYxj1bn4rdX1jXcrLlapumcgjOJO6UajPYyrgAgQT2Wx0aZkER\nffV03fvIjawXhr2Pb9BlsVAtQWuTzcre/Yvuvuo6Y3IMojlMUH/786zj0QKBgBTl\ngITcL+LBo+rl+j4HgU1iMrW0zRHmHEbEMoVNPxSq/JHVnHWPydEi/21oo6LbyqIs\nQ/V6YJyezMBeE+/I3Xy8Ad01wkeV7dYjo7qmkV743nDlw1NBCJ79uj5x6S3ucXVO\n0FgFzG3t6FmCZW/tXfI+vyIRBl27s2u/YA2d9nWlAoGAPRSN1hsMJfN26QLMCmF7\n+V3lSK1FJl+Mlzbx5OBqmWanajKvUOaEMvxWefexzt0CItpm9phutHMcza79PVNz\nM5Lhc/7g0OgfOsRZQ85rvozsdrM21Pn6SmEbKT9TY/BSxMJFPZLsnp8OJSF1gB5C\n13FH8eSsOebmZyMXb/XSZl4=\n-----END PRIVATE KEY-----\n",
    "client_email": "nick-devmane@speech-recog-363719.iam.gserviceaccount.com",
    "client_id": "114238067351695446618",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/nick-devmane%40speech-recog-363719.iam.gserviceaccount.com"
}
# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

# recognize speech using Sphinx
try:
    print("+++++++++++++++++++++++++++++++++++++++++ \n Sphinx\n=================================================")

    print(r.recognize_sphinx(audio, show_all=True))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("+++++++++++++++++++++++++++++++++++++++++ \n Google AI\n=================================================")
    print(r.recognize_google(audio, show_all=True))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(
        "Could not request results from Google Speech Recognition service; {0}".format(e))

# recognize speech using Google Cloud Speech
# GOOGLE_CLOUD_SPEECH_CREDENTIALS = "AIzaSyCWplwr7WvmrmeO7MlNdy14efVLW2Yw27k"

credentials = service_account.Credentials.from_service_account_file(
    "bin\speech-recog-363719-5d0d5205a97a.json")

client = speech.SpeechClient(credentials=credentials)

# The name of the audio file to transcribe
gcs_uri = "gs://spr_nick/./microphone_Results.wav"


audio1 = speech.RecognitionAudio(uri=gcs_uri)


config = speech.RecognitionConfig(
    language_code="en-US",
    enable_word_confidence=True,
    enable_word_time_offsets=True,
)

# Detects speech in the audio file
operation = client.long_running_recognize(config=config, audio=audio1)

print("Waiting for operation to complete...")
result = operation.result(timeout=90)
print("+++++++++++++++++++++++++++++++++++++++++ \n Speech to text \n=================================================")
for result in result.results:
    alternative = result.alternatives[0]
    print("Transcript: {}".format(alternative.transcript))
    print("Confidence: {}".format(alternative.confidence))

    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time

        print(
            f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
        )


# # recognize speech using Wit.ai
# Wit.ai keys are 32-character uppercase alphanumeric strings
WIT_AI_KEY = "B6BWMKRUCVRZMC5TZN5FEHDSQMUCSR5F"
try:

    print("+++++++++++++++++++++++++++++++++++++++++ \n Wit AI\n=================================================")
    print(r.recognize_wit(audio, key=WIT_AI_KEY, show_all=True))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))

# recognize speech using Houndify
# Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_ID = "GcIuOSlP9tOLfoieoYgxMg=="
# Houndify client keys are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "tGUjCMskM41RYqSrmCQkM8IzfBIsPV0F9eVeE4fc6GxhSnMPalihcvq8pd8ck8zekJNQunFVPCV3FWjoKkPGsQ=="
try:
    print("+++++++++++++++++++++++++++++++++++++++++ \n Houndify\n=================================================")
    print(r.recognize_houndify(audio,
          client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY, show_all=True))
except sr.UnknownValueError:
    print("Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))

# recognize speech using IBM Speech to Text
# IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
# IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE"
# # IBM Speech to Text passwords are mixed-case alphanumeric strings
# IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE"
# try:
#     print("IBM Speech to Text thinks you said " +
#           r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
# except sr.UnknownValueError:
#     print("IBM Speech to Text could not understand audio")
# except sr.RequestError as e:
#     print(
#         "Could not request results from IBM Speech to Text service; {0}".format(e))
