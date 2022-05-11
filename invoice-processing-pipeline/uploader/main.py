# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    This web app allows users to upload one or more files to a particular bucket,
    where they may later be processed. The canonical use case is for uploading
    invoices in human-readable form, with the expectation that the information
    in those invoices will be later extracted and handled by an organization's
    standard business practices.

    Requirements:

    -   Python 3.7 or later
    -   All packages in requirements.txt installed
    -   A bucket to place the files in
    -   Software environment has ADC or other credentials to write to the bucket
    -   The name of the bucket (not the URI) in the environment variable BUCKET

    This Flask app can be run directly via "python main.py" or with gunicorn
    or other common WSGI web servers.
"""

from flask import Flask, render_template, request
import os
from uuid import uuid4

from google.cloud import storage


app = Flask(__name__)


@app.route("/", methods=["GET"])
def show_upload_page():
    return render_template("index.html"), 200


@app.route("/", methods=["POST"])
def handle_uploads():
    BUCKET_NAME = os.environ.get("BUCKET")
    client = storage.Client()

    try:
        bucket = client.get_bucket(BUCKET_NAME)
    except Exception as e:
        return f"Could not open bucket: {e}", 400

    handled = 0
    for key in request.files:
        for file in request.files.getlist(key):
            if uploaded_to_storage(file, bucket):
                handled += 1

    return f"Uploaded {handled} file(s)", 200


def uploaded_to_storage(file, bucket):
    mimetype = file.mimetype
    if mimetype is None:
        mimetype = "application/octet-stream"

    blob_key = f"incoming/{uuid4()}"
    blob = bucket.blob(blob_key)
    blob.content_type = mimetype

    blob.upload_from_file(file.stream)

    return True


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)