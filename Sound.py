from warnings import catch_warnings
import speech_recognition as sr
import soundfile as sf
# from pydub import AudioSegment
import os

path = "c:/users/nicko/spr/microphone_results.wav"


# assert os.path.isfile(path)


# input = input(
#     "to get a more balanced sound, press b: \n to get a louder sound, press l: ")

# the data to be returned is where there is speech
r = sr.Recognizer()

energy = 6000
r.energy_threshold = energy
# r.dynamic_energy_threshold = True

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

segments = []

for i in speech:
    segments.append([i["start"], i["end"]])
# print(speech)

print("cleaned data: ", segments)
print("\n================================================")
print("amount of voice segments: ", len(segments))
print("number currently: ", energy)
print("==================================================")

# divide the total time by amount of frames, then multiply the index by that constant


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
        print("size of data: ", data.size)
        while x < data.size:
            print("current index: ", x)
            print("current time: ", x/samp_rate)
            print("segment index:  ", baby)
            if baby < len(segments):
                idx = int(segments[baby][0]*true_fpms)
                print("cleaning... ", x, " to ", idx)
                if x != idx:
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
        # f.seek(pos)

        print(
            "======================================================================")
        print("new data: ", data)
        print(
            "======================================================================")

        print("new size: ", f.frames)
        sf.write(path, data, samplerate=samp_rate)
        f.close()


refine()
