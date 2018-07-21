from flask import Flask
from flask import render_template, request, flash, g, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
from flask_bootstrap import Bootstrap
from lib.EventLog import EventLog

global event_log
UPLOAD_FOLDER = r"./upfiles"
ALLOWED_EXTENSIONS = {'gz', 'zip'}

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/show", methods=['GET'])
def show_data():
    global event_log
    try:
        sn = event_log.Node[0]
    except Exception as e:
        sn = str(e)
    return render_template('show.html', serial_number=sn)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global event_log
            event_log = EventLog(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return url_for(".show_data")


@app.route("/get_detail", methods=['GET'])
def get_detail():
    global event_log
    param_id = request.args.get('id')
    try:
        param_id = int(param_id)
        return event_log.MessageText[param_id]
    except Exception as e:
        return "Server Error.\n" + str(e)


@app.route("/get_data", methods=['POST'])
def get_data():
    global event_log
    page = request.values.get('page')
    rows = request.values.get('rows')
    error_dict = {"total": 1,
                  "rows": [{
                      "id": 1,
                      "severity": "Error in Server",
                      "datetime": "Error in Server",
                      "messageid": "Error in Server",
                      "messagetext": "Error in Server", }]}
    # try to convert from string to int
    try:
        page = int(page)
        rows = int(rows)
    except Exception as e:
        print(str(e))
        return error_dict
    try:
        dic2 = {
            "total": event_log.ItemQuantity,
            "rows": event_log.DictList[(page - 1) * rows: (page - 1) * rows + rows]}
        json_str = json.dumps(dic2)
    except Exception as e:
        non_initial = {"total": 1,
                       "rows": [{
                           "id": 1,
                           "severity": "n.a.",
                           "datetime": "n.a.",
                           "messageid": "n.a.",
                           "messagetext": str(e), }]}
        json_str = json.dumps(non_initial)
    return json_str


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
