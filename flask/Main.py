import json
from flask import Flask, request, flash, redirect, url_for, send_from_directory, abort, jsonify, make_response
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import tempfile
import os
from pyngrok import ngrok
app = Flask(__name__)
app.secret_key = "wqm7dajh"

ngrok.set_auth_token("2GkgswOuCD9edDpcX4vAmal3Xs8_4pW8C8s7AAbitRR8Vf4EA")


run_with_ngrok(app)

tempfolder = tempfile.gettempdir()


ALLOWED_EXTENSIONS = {'.wav'}

app.config['UPLOAD_FOLDER'] = tempfolder
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
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
            # return "file extension: " + str(file_ext)
            if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                abort(400)

        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
            return "no file was selected or corrupted request"
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return "average thingie always getting"


@app.route('/', methods=["GET"])
def uploaded_file(filename):

    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,
                               filename)


if __name__ == "__main__":
    app.run()
