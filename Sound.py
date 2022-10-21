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


# assert os.path.isfile(path)


# input = input(
#     "to get a more balanced sound, press b: \n to get a louder sound, press l: ")

# the data to be returned is where there is speech
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
            # print(
            #     f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            # )
    print(segments)
# r.dynamic_energy_threshold = True


def transpose_wit():
    with sr.AudioFile(path) as source:
        audio = r.record(source)  # read the entire audio file

    # Wit.ai keys are 32-character uppercase alphanumeric strings
    WIT_AI_KEY = "B6BWMKRUCVRZMC5TZN5FEHDSQMUCSR5F"
    try:
        words = r.recognize_wit(audio, key=WIT_AI_KEY, show_all=True)
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("object returned: ", words)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # Object with speech details. This object will contain the speech confidence
    # and the start and end time in milliseconds for each token contained in the transcript.
    # This value should be used only for debugging purposes
    # as Wit.ai focuses on intents, entities and traits.
    try:
        speech = words["speech"]["tokens"]
    except:
        print("no speech recognized")

    for i in speech:
        segments.append([i["start"], i["end"]])
    # print(speech)

    print("cleaned data: ", segments)
    print("\n================================================")
    print("amount of voice segments: ", len(segments))
    print("number currently: ", energy)
    print("==================================================")

# divide the total time by amount of frames, then multiply the index by that constant


# smooths audio and removes unexpected jumps in sample, causing an unwanted noise
def fourier_smooth():
    return


def refine():
    with sf.SoundFile(path, 'r+') as f:
        samp_rate = f.samplerate
        data = f.read()
        # print("size of data: ", data.size)
        print(f.frames)
        print("=================================")
        print("data: ", data)
        print("=================================")
        x = 0
        baby = 0
        true_fpms = samp_rate/1000
        print("ratio: ", true_fpms)
        print("size of data : ", data.size)

        while x < data.size:
            print("current index: ", x)
            print("current time: ", x/samp_rate)
            print("segment index:  ", baby)
            if baby < len(segments)-1:

                idx = int(segments[baby][0]*true_fpms)
                print("cleaning... ", x, " to ", idx)
                # if x != idx:
                data[x:idx] = 0
                print("data cleaned: ", data[x:idx])
            else:
                print("to end : ", data[x:])
                data[x:] = 0
                print("NEW to end : ", data[x:])
                break
            # print("time of frame: ", time)

            # checks if frame is not part of the segments containing words, greater than the current segment
            # then it increments the segment if true

            x = int(segments[baby][1]*true_fpms)
            print("x is now : ", segments[baby][1],
                  " x ", true_fpms)
            baby += 1

        temp = []

        for i in data:
            temp.append(i[0])

        temp = np.sort(data)
        temp = np.delete(temp, np.where(temp == 0))

        sevenfive = temp[temp.size-temp.size//4]
        twofive = temp[temp.size//4]

        interquartile_range = stat.iqr(temp)

        iqr_rule_1p5 = interquartile_range*1.5

        upper = sevenfive + iqr_rule_1p5

        lower = twofive - iqr_rule_1p5
        print(lower)
        print("interquartile range: ", interquartile_range)
        # f.seek(pos)

        # print(
        #     "======================================================================")
        # print("new data: ", data)
        # print(
        #     "======================================================================")

        for i in range(len(data)):
            if data[i][0] > upper:
                data[i] = 0
            elif data[i][0] < lower:
                data[i] = 0

        # print("new size: ", f.frames)

        sf.write(path, data, samplerate=samp_rate)
        f.close()


transpose_gs()
refine()
