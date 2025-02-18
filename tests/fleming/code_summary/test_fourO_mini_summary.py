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

import pytest
from unittest.mock import MagicMock, patch
from pyspark.sql import SparkSession
from src.fleming.code_summary.fourO_mini_summary import OpenAIClient
import requests
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


@pytest.fixture
def spark():
    """Create a spark session for testing"""
    return SparkSession.builder.appName("test").getOrCreate()


@pytest.fixture
def openai_client(spark):
    """Create a test OpenAIClient instance"""
    # Create a mock DataFrame with test data
    test_data = [("test_repo", "test content", 100)]
    input_df = spark.createDataFrame(test_data, ["title", "content", "token_count"])

    return OpenAIClient(
        spark=spark,
        input_spark_df=input_df,
        output_table_name="test_table",
        prompt="Test prompt",
        api_key="test_key",
        endpoint="http://test-endpoint",
    )


def test_initialization(openai_client):
    """Test if the OpenAIClient initializes correctly"""
    assert openai_client.prompt == "Test prompt"
    assert openai_client.api_key == "test_key"
    assert openai_client.endpoint == "http://test-endpoint"
    assert openai_client.headers == {
        "Content-Type": "application/json",
        "api-key": "test_key",
    }


@patch("requests.post")
def test_call_openai_success(mock_post, openai_client):
    """Test successful API call to OpenAI"""
    # Mock the API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test summary"}}]
    }
    mock_post.return_value = mock_response

    # Call the method
    openai_client.call_openai("title", "content", "token_count")

    # Verify the results DataFrame was created
    assert openai_client.results_df is not None
    results = openai_client.results_df.collect()
    assert len(results) == 1
    assert results[0]["virtual_readme"] == "Test summary"


@patch("requests.post")
def test_call_openai_failure(mock_post, openai_client):
    """Test API call failure handling"""
    # Mock a failed API response
    mock_post.side_effect = requests.RequestException("API Error")

    # Test that the method raises SystemExit
    with pytest.raises(SystemExit):
        openai_client.call_openai("title", "content", "token_count")


def test_display_results_no_data(openai_client):
    """Test display_results when no data is available"""
    with pytest.raises(ValueError, match="No results to display"):
        openai_client.display_results()


def test_save_results_no_data(openai_client):
    """Test save_results when no data is available"""
    with pytest.raises(ValueError, match="No results to save"):
        openai_client.save_results()
