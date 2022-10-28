from json import JSONEncoder
from flask import Flask, request, flash, redirect, url_for, send_from_directory
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import os
from pyngrok import ngrok

app = Flask(__name__)
app.secret_key = "wqm7dajh"

ngrok.set_auth_token("2GkgswOuCD9edDpcX4vAmal3Xs8_4pW8C8s7AAbitRR8Vf4EA")


run_with_ngrok(app)


upload_dir = "./uploads"

ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = upload_dir


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    this is returned if the post method
    doesnt work
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run()
