# Copyright 2024 Fleming
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

from unittest.mock import MagicMock, patch

from src.fleming.discovery.model_serve import ModelServe

import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def test_deploy_endpoint(spark_session):
    # Mock the requests.put response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_requests_put = MagicMock(return_value=mock_response)
    with patch("requests.put", mock_requests_put):
        pass
    # Call the method
    model_serve = ModelServe(
        spark=spark_session,
        endpoint_name="test_endpoint",
        model_name="test_model",
        workload_type="CPU",
        workload_size="Small",
        scale_to_zero=True,
        API_ROOT="http://test-api-root",
        API_TOKEN="test-api-token",
    )

    try:
        model_serve.deploy_endpoint()
    except Exception as e:
        f"An error occurred: {e}"
