import speech_recognition as sr
import soundfile as sf
# from pydub import AudioSegment
import os
import numpy as np
import time as t
import statistics as stat

path = "c:/users/nicko/spr/microphone_results.wav"


# assert os.path.isfile(path)


# input = input(
#     "to get a more balanced sound, press b: \n to get a louder sound, press l: ")

# the data to be returned is where there is speech
r = sr.Recognizer()
# getting a recording
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

with open("microphone_results.wav", "wb") as f:
    f.write(audio.get_wav_data())


r.energy_threshold = 4000
r.dynamic_energy_threshold = True

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

speech = words["speech"]["tokens"]

segments = []

for i in speech:
    segments.append([i["start"], i["end"]])
# print(speech)


print("cleaned data: ", segments)

# divide the total time by amount of frames, then multiply the index by that constant


with sf.SoundFile(path, 'r+') as f:
    samp_rate = f.samplerate
    data = f.read()
    # print("size of data: ", data.size)
    # print(f.frames)
    for x in range(data.size):
        time = x/samp_rate
        print("time of frame: ", time)
        baby = 0
        if time > segments[baby][1]:
            baby += 1
        else:
            if segments[baby][0] <= time <= segments[baby][1]:
                continue
            else:
                data[x] = 0

    # f.seek(pos)

    print(
        "======================================================================")
    print("new data: ", data)
    print(
        "======================================================================")

    f.write(data)
    f.close()

    # while f.tell() < f.frames:

    #     pos = f.tell()
    #     print("position: ", pos)

# print("old data: ", data)

# stdv = np.std(data)

# print("-----------------------")
# print("standard dev: ", stdv)
# print("-----------------------")

# mean = np.mean(data)

# print("-----------------------")
# print("mean: ", mean)
# print("-----------------------")

# sum = 0
# elements = 0
# this just checks to see if the audio volume val is relative to the mean and adds it to be averaged
# for i in data:

#     if abs(abs(i[0])-stdv) > mean:
#         elements += 1
#         sum += abs(i[0])

# avg = sum/len(data)

# refine(1)
# f.close()
# play(song)
