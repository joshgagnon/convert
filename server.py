from __future__ import print_function
import signal
import subprocess
import logging
from flask import Flask, request, send_file, jsonify
import os
import os.path
from io import BytesIO
import tempfile
from subprocess import Popen, STDOUT, PIPE
import shutil
import errno
from data_to_png import string_to_png
import json


try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

logging.basicConfig()

PORT = 5668
SOFFICE_BIN = 'soffice'
SOFFICE_PYTHON = 'python3'
CONVERTER = 'DocumentConverter.py'


app = Flask(__name__)


MIMETYPES = {
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'odt': 'application/vnd.oasis.opendocument.text',
    'pdf': 'application/pdf',
    "png": "image/png",
    "html": "text/html",
}

EXTENSIONS = {
    'pdf': '.pdf',
    'odt': '.odt',
    'docx': '.docx',
    'png': '.png',
    'html': '.html'
}


def convert_type_service(data, type):
    try:
        with tempfile.NamedTemporaryFile(suffix='.odt') as temp_in, tempfile.NamedTemporaryFile(suffix=EXTENSIONS[type]) as temp_out:
            temp_in.write(data)
            temp_in.flush()
            args = [SOFFICE_PYTHON, CONVERTER, temp_in.name, temp_out.name]
            result = Popen(args,
                 stdout=DEVNULL,
                 stderr=DEVNULL,
                 env={}).wait()

            return temp_out.read()
    except Exception as e:
        raise e


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route('/convert', methods=['POST'])
def convert():
    try:
        file_type = request.values.get('fileType', 'docx')
        result = request.files['file']
        filename = result.filename
        file = result.read()
        if file_type != 'odt' and EXTENSIONS.get(file_type):
            file = convert_type_service(file, file_type)

        return send_file(BytesIO(file),
                         attachment_filename=os.path.splitext(filename)[0] + EXTENSIONS[file_type],
                         as_attachment=True,
                         mimetype=MIMETYPES[file_type])
    except Exception as e:
        raise InvalidUsage(e.message, status_code=500)


@app.route('/encode', methods=['POST'])
def encode():
    try:
        string = json.dumps(request.get_json())
        output = BytesIO()
        string_to_png(string, output)
        output.seek(0)
        return send_file(output,
                         attachment_filename='encoded.png',
                         as_attachment=True,
                         mimetype='image/png')
    except Exception as e:
        raise InvalidUsage(e.message, status_code=500)

@app.route('/status', methods=['GET'])
def status():
    return send_file('static/status.html')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    # dev mode
    SOFFICE_PYTHON = '/Applications/LibreOffice.app/Contents/MacOS/python'
    SOFFICE_BIN = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    print('Running on %d' % PORT)
    app.run(port=PORT, debug=True)
