# /usr/env/python3
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
    An application to extract information from PDF invoices and update a
    database with that information. Intended to run in Cloud Run Jobs.

    Requirements:

    -   Python 3.7 or later
    -   All packages in requirements.txt installed
    -   A bucket with the invoice files in the /incoming folder
    -   Firestore database to store information from the invoices
    -   Software environment has ADC or other credentials to read and write
        to and from from the bucket, and to read and to the Firestore database
    -   The name of the bucket (not the URI) in the environment variable BUCKET

    This app can be run directly via "python main.py".
"""


INCOMING_PREFIX = "incoming/"
PROCESSED_PREFIX = "processed/"
FIRST_CHARACTERS = "0123456789abcdef"   # Blob names start with one of these

import os
import process
from helpers import get_project_id

from google.cloud import storage


if __name__ == "__main__":
    # Retrieve Jobs-defined env vars (for parallel processing)
    TASK_NUM = int(os.getenv("CLOUD_RUN_TASK_INDEX", 0))
    TASK_COUNT = int(os.getenv("CLOUD_RUN_TASK_COUNT", 1))
    ATTEMPT_NUM = int(os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0))
    print(f"Starting attempt {ATTEMPT_NUM} of task {TASK_NUM} of {TASK_COUNT} tasks.")

    chunks = []

    chars_remaining = FIRST_CHARACTERS
    count_remaining = TASK_COUNT

    while count_remaining > 0:
        chunk_size = int(len(chars_remaining) / count_remaining)
        chunks.append(chars_remaining[:chunk_size])
        chars_remaining = chars_remaining[chunk_size:]
        count_remaining -= 1

    print(chunks)
    my_chunk = chunks[TASK_NUM]
    print(f"My chunk is '{my_chunk}' for task {TASK_NUM}.")

    # Retrieve user-defined env vars
    location =  "us"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", get_project_id())
    processor_id = os.environ["PROCESSOR_ID"]
    bucket_name = os.environ["BUCKET"]

    client = storage.Client()

    for blob in client.list_blobs(bucket_name, prefix=INCOMING_PREFIX):
        # Is this blob our responsibility, or a different task's?
        if blob.name[len(INCOMING_PREFIX)] not in my_chunk:
            continue    # Not my problem

        # Is this really a blob, or a folder?
        if blob.name.endswith("/"):
            continue    # Not my problem

        # Okay, this one is really my responsibility

        # Extract the invoice data
        document = process.process_blob(
            project_id, location, processor_id, blob)

        # Save to Firestore
        process.save_processed_document(document, blob)

        # Move blob to the processed/ folder
        bare_name = blob.name[len(INCOMING_PREFIX):]    # Drop folder name
        new_name = f"{PROCESSED_PREFIX}{bare_name}"
        blob.bucket.rename_blob(blob, new_name)
