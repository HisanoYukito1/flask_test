import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import json
import pathlib
import matplotlib.pyplot as plt

UPLOAD_FOLDER = '/data'
CACHE_FOLDER = '/tmp/app'
ALLOWED_CONFIG_EXTENSIONS = {'json'}
ALLOWED_DATA_EXTENSIONS = {'csv', 'tsv'}
NEEDS_FILE_TYPE = {'config', 'data'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CACHE_FOLDER'] = CACHE_FOLDER


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('config' not in request.files) or ('data' not in request.files):
            flash('No file part')
            return redirect(request.url)
        config = request.files['config']
        data = request.files['data']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if config.filename == '' or data.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if (config and allowed_file(config.filename, ALLOWED_CONFIG_EXTENSIONS)) and (data and allowed_file(data.filename, ALLOWED_DATA_EXTENSIONS)):
            
            dfile = secure_filename(config.filename)
            conf_path = pathlib.Path(app.config['CACHE_FOLDER']) / secure_filename(config.filename)
            config.save(conf_path)
            data_path = pathlib.Path(app.config['CACHE_FOLDER']) / secure_filename(data.filename)
            data.save(data_path)

            with open(conf_path) as cf, open(data_path) as df:
                conf = json.load(cf)
                df = pd.read_csv(data_path)

                fig, ax = plt.subplots()
                for key, values in conf.items():
                    print(values)
                    ax.set_title(key)
                    for i in values:
                        ax.scatter(df[i["xlabel"]], df[i["ylabel"]])
                    
                dest_path = pathlib.Path(UPLOAD_FOLDER) / f"{data_path.stem}.png"
                plt.savefig(dest_path)
            
            
            
            return redirect(url_for('create_file', name=f"{data_path.stem}.png"))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <table>
        <tr>
          <td>
            <label>config:</label>
            <input type=file name=config>
          </td>
        </tr>
        <tr>
          <td>
            <label>data:</label>
            <input type=file name=data>
          </td>
        </tr>
      </table>
      <br>
      <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/uploads/<name>')
def create_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)