import speech_recognition as sr

from gcloud import storage


from oauth2client.service_account import ServiceAccountCredentials


r = sr.Recognizer()
# getting a recording
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

with open("microphone_results.wav", "wb") as f:
    f.write(audio.get_wav_data())


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

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)

client = storage.Client(credentials=credentials, project="sound_recog")
bucket = client.get_bucket("spr_nick")
blob = bucket.blob("./microphone_Results.wav")
blob.upload_from_filename("./microphone_Results.wav")
