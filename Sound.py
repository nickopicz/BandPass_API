from statistics import median
from warnings import catch_warnings
import speech_recognition as sr
import soundfile as sf
# from pydub import AudioSegment
import os
from google.cloud import speech
from google.oauth2 import service_account
import numpy as np
import scipy.stats as stat
path = "./zara_love.wav"


r = sr.Recognizer()
energy = 6000
r.energy_threshold = energy
segments = []


def transpose_gs():
    credentials = service_account.Credentials.from_service_account_file(
        "bin\speech-recog-363719-5d0d5205a97a.json")

    client = speech.SpeechClient(credentials=credentials)

    # The name of the audio file to transcribe
    gcs_uri = "gs://spr_nick/./evi.wav"

    audio1 = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        language_code="en-US",
        enable_word_confidence=True,
        enable_word_time_offsets=True,
        audio_channel_count=2,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio1)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)
    print("+++++++++++++++++++++++++++++++++++++++++ \n Speech to text \n=================================================")
    print("results: ", result.results)

    for result in result.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))
        print(alternative)

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print("datatype: ", type(start_time))

            print("both start and end times for ", word, ": ",
                  start_time.total_seconds()*1000, " - ", end_time.total_seconds()*1000)

            print("time in seconds: ", start_time.seconds,
                  " to ", end_time.seconds)

            # appends the recognized words start and end point as segments of talking
            # values to be used when setting dcb to 0,
            segments.append([start_time.total_seconds()*1000,
                            end_time.total_seconds()*1000])
            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )
    print(segments)


transpose_gs()
