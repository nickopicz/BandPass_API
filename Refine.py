import speech_recognition as sr
import soundfile as sf
import numpy as np
import collections
import contextlib
import sys
import wave
import webrtcvad


path = "./audio_files/evi.wav"
path1 = "./audio_files/evi.wav"
path2 = './audio_files/new_file.wav'


# This is a helper function that returns:
#
# - true sample rate
# - frames data
# - duration of the audio in seconds

def get_data():
    with sf.SoundFile(path, 'r+') as f:
        samp_rate = f.samplerate
        data = f.read()
        time = f.frames/samp_rate
        print("sample rate: ", samp_rate)
        print("duration of file: ", time)
        print(f.frames)
        print("=================================")
        print("data: ", data)
        print("=================================")
        f.close()
        return data, time, samp_rate


frames_data, time, samp_rate = get_data()


# These are helper functions given by the github for webrtcvad.
# They enable the use of audio data to detect voiced data

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels in (1, 2)
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


class Frame(object):
    """Represents a "frame" of audio data."""

    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """

    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


dur = time*1000

# This is time in ms divided by 5 to get the amount
# of frames collected that are in the original audio file,
#  so its time i ms divided by five

print("webrtcvad frames in og: ", dur/5)

print("duration: ", dur)

vad = webrtcvad.Vad()

vad.set_mode(3)

audio, sample_rate = read_wave(path1)

print("sample rate: ", sample_rate)

frames = frame_generator(10, audio, sample_rate)

frames = list(frames)

print("amount of frames: ", len(frames))

segments = []

# This next loop iterates through the generated frames and
# checks if they contain speech. If the frame does, appends True
# to a list of the same length of the frames list.
#  Or this loop appends False to the list if it doesn't
# have any voiced frames


for frame in frames:
    if vad.is_speech(frame.bytes, sample_rate):
        segments.append(True)
    else:
        segments.append(False)

print("------------------------------------------------------------------------\n")
print("Segments: ", segments)
print("------------------------------------------------------------------------\n")


frames_2 = frames_data
i = 0


# This variable called factor, generates a ratio of frames to
# the amount of 10ms sample frames from the previous block of code.
# It uses this factor (ratio) as a way to convert the
# frames of the wav file to an index of the segments


factor = len(frames_data)/len(segments)
print()
print('factor: ', factor)

for i in range(len(segments)):
    idx = int(i*factor)
    end = int((i+1)*factor)
    print("start idx: ", idx, " end index: ", end)
    if segments[i] == False:
        print("editing section: \n ========================================= \n",
              frames_2[idx:end])
        frames_2[idx:end] = 0
    else:
        print("glossed over ", idx, " to ", end)
        continue


sf.write('./audio_files/new_file.wav', frames_2, 48000)
