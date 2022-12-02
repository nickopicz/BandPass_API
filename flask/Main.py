import json
from flask import Flask, request, flash, redirect, url_for, send_from_directory, abort, jsonify, make_response
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import tempfile
import os
from pyngrok import ngrok
import speech_recognition as sr
import soundfile as sf
import numpy as np
import contextlib
import wave
import webrtcvad
import config
import io
import re
from google.cloud import speech


def get_data(filepath):
    with sf.SoundFile(filepath, 'r+') as f:
        samp_rate = f.samplerate
        data = f.read()
        time = f.frames/samp_rate
        f.close()
        return data

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


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(f"Transcript: {transcript}")
        print(f"Confidence: {confidence:.0%}")


def speech_to_text(path):
    language_code = "en-US"


# Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 48000

# Encoding of audio data sent. This sample sets this explicitly.
# This field is optional for FLAC and WAV audio formats.

    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
    }

    with io.open(path, "rb") as f:
        content = f.read()

    audio = {"content": content}
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)

    results = response.results

    confidences = []

    for i in results:
        temp = re.findall(r'\d+', str(i.alternatives[0]))
        confidences.append(float(".".join(temp)))

    max_idx = confidences.index(max(confidences))

    return response.results[max_idx].alternatives[0].transcript


# speech_to_text(config, audio)

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


def refine(path):
    frames_data = get_data(path)

    # This is time in ms divided by 5 to get the amount
    # of frames collected that are in the original audio file,
    #  so its time i ms divided by five

    vad = webrtcvad.Vad()

    vad.set_mode(2)

    audio, sample_rate = read_wave(path)

    frames = frame_generator(10, audio, sample_rate)

    frames = list(frames)

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

    frames_2 = frames_data
    i = 0

    # This variable called factor, generates a ratio of frames to
    # the amount of 10ms sample frames from the previous block of code.
    # It uses this factor (ratio) as a way to convert the
    # frames of the wav file to an index of the segments

    factor = len(frames_data)/len(segments)

    for i in range(len(segments)):
        idx = int(i*factor)
        end = int((i+1)*factor)
        if segments[i] == False:
            frames_2[idx:end] = 0
        else:
            continue

    sf.write(path, frames_2, 48000)

# =====================================================================
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# =====================================================================
# FLASK API CODE STARTS BELOW HERE
# =====================================================================
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# =====================================================================


app = Flask(__name__)
app.secret_key = "wqm7dajh"

ngrok.set_auth_token(config.ngrok_key)


run_with_ngrok(app)

tempfolder = tempfile.gettempdir()


ALLOWED_EXTENSIONS = {'.wav'}

app.config['UPLOAD_FOLDER'] = tempfolder
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():

    # check if the post request has the file part
    # return jsonify(request)
    if 'audio_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['audio_file']
    # if user does not select file, browser also
    # submit an empty part without filename
    filename = file.filename

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            abort(400)

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(filename)))
        refine(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return uploaded_file(filename=filename)


@app.route('/get_file/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


@app.route('/get_transcript/<path:filename>', methods=['GET'])
def transcription(filename):
    return speech_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))


app.add_url_rule(
    "/get_file/<path:filename>", endpoint="download_file", build_only=True
)


if __name__ == "__main__":
    app.run()
