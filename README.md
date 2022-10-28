# SpecialSound
An audio refinery program that uses speech-to-text and cleans out background noise.




# 1. Install Dependencies.
First make sure python3 is installed on your local system.
Make sure you have pip installed as a cli. 
<br />
After creating a dedicated python workspace...
<br />
<br />
Run these following commands:
<br />
<br />
pip install speech_recognition
<br />pip install soundfile as sf
<br />pip install wave
<br />pip install webrtcvad
<br />pip install contextlib



# 2. Make a Recording.

You can create your own recording within this directory by running the file "make_recording.py"
This makes it easy to test, since it generates an uncorrupted wav file. 


# 3. Clean up Audio.

You can either make a short recording within the directory, or import an audio file from your system. 
You can clean your custom audio by changing the "path1" variable of "Refine.py",
to the path of your specific audio file. This algorithm utilizes webrtcvad, which is a tool that google developed.
It can be used for a wide variety of things, but for this application it just detects when audio is speech. 
The algorithm used in this repository to clean your audio returns your original file in "new_file.wav".



