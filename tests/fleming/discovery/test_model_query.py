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

import json

import os
import sys
from unittest.mock import MagicMock, patch
import numpy as np
import pandas as pd
import pytest
import requests

from src.fleming.discovery.model_query import ModelQuery


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


@pytest.fixture
def model_query():
    url = "http://example.com/score"
    token = "test_token"
    return ModelQuery(url, token)


def test_create_tf_serving_json_with_ndarray(model_query):
    data = np.array([[1, 2, 3], [4, 5, 6]])
    expected_output = {"inputs": [[1, 2, 3], [4, 5, 6]]}
    assert model_query.create_tf_serving_json(data) == expected_output


@patch("requests.request")
def test_score_model_success(mock_request, model_query):
    dataset = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"predictions": [0.1, 0.2, 0.3]}
    mock_request.return_value = mock_response

    response = model_query.score_model(dataset)
    assert response == {"predictions": [0.1, 0.2, 0.3]}
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs["method"] == "POST"
    assert kwargs["url"] == model_query.url
    assert kwargs["headers"] == {
        "Authorization": f"Bearer {model_query.token}",
        "Content-Type": "application/json",
    }
    assert json.loads(kwargs["data"]) == {
        "dataframe_split": dataset.to_dict(orient="split")
    }


@patch("requests.request")
def test_score_model_failure(mock_request, model_query):
    dataset = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_request.return_value = mock_response

    with pytest.raises(
        requests.exceptions.HTTPError,
        match="Request failed with status 400, Bad Request",
    ):
        model_query.score_model(dataset)
    mock_request.assert_called_once()
