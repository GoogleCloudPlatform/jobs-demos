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

import google.auth
import requests

METADATA_URI = "http://metadata.google.internal/computeMetadata/v1/"


def get_project_id() -> str:
    """Use the 'google-auth-library' to make a request to the metadata server or
    default to Application Default Credentials in your local environment."""
    _, project = google.auth.default()
    return project


def get_service_region() -> str:
    """Get region from local metadata server
    Region in format: projects/PROJECT_NUMBER/regions/REGION"""
    slug = "instance/region"
    data = requests.get(METADATA_URI + slug, headers={"Metadata-Flavor": "Google"})
    return data.content

