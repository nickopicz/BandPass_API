import numpy as np


binaryHeader = {}
binarySound = {}
song = {}


with open("Recording.wav", 'rb') as f:
    buffer = f.read(16)
    print(buffer)
    binaryHeader = np.frombuffer(buffer, dtype=np.uint8)
    buffer = f.read()
    binarySound = np.frombuffer(buffer, dtype=np.uint8)


with open("header.bin", "wb") as f:
    f.write(binaryHeader)

with open("data.bin", "wb") as f:
    f.write(binarySound)


with open("data.bin", "rb") as d:
    song = d.read()

with open("new.wav", "wb") as f:
    song = np.array(song)
    f.write(song.tobytes())
