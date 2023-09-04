#!/usr/bin/env python3

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import math
import os
import time

import google.auth
from google.cloud import storage

storage_client = storage.Client()

_, PROJECT_ID = google.auth.default()
TASK_INDEX = int(os.environ.get("CLOUD_RUN_TASK_INDEX", 0))
TASK_COUNT = int(os.environ.get("CLOUD_RUN_TASK_COUNT", 1))

INPUT_BUCKET = os.environ.get("INPUT_BUCKET", f"input-{PROJECT_ID}")
INPUT_FILE = os.environ.get("INPUT_FILE", "input_file.txt")

# Process a Cloud Storage object.
def process():
    method_start = time.time()

    # Output useful information about the processing starting.
    print(
        f"Task {TASK_INDEX}: Processing part {TASK_INDEX} of {TASK_COUNT} "
        f"for gs://{INPUT_BUCKET}/{INPUT_FILE}"
    )

    # Download the Cloud Storage object
    bucket = storage_client.bucket(INPUT_BUCKET)
    blob = bucket.blob(INPUT_FILE)

    # Split blog into a list of strings.
    contents = blob.download_as_string().decode("utf-8")
    data = contents.split("\n")

    # Determine the chunk size, and identity this task's chunk to process.
    chunk_size = math.ceil(len(data) / TASK_COUNT)
    chunk_start = chunk_size * TASK_INDEX
    chunk_end = chunk_start + chunk_size

    # Process each line in the chunk.
    count = 0
    loop_start = time.time()
    for line in data[chunk_start:chunk_end]:
        # Perform your operation here. This is just a placeholder.
        _ = hashlib.md5(line.encode("utf-8")).hexdigest()
        time.sleep(0.1)
        count += 1

    # Output useful information about the processing completed.
    time_taken = round(time.time() - method_start, 3)
    time_setup = round(loop_start - method_start, 3)
    print(
        f"Task {TASK_INDEX}: Processed {count} lines "
        f"(ln {chunk_start}-{min(chunk_end-1, len(data))} of {len(data)}) "
        f"in {time_taken}s ({time_setup}s preparing)"
    )


if __name__ == "__main__":
    process()
