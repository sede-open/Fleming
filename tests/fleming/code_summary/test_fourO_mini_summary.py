import pytest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from tests.conftest import spark_session

from src.fleming.code_summary.fourO_mini_summary import OpenAIClient


def test_display_results():
  """
  Unit test verifies that you are getting a ValueError, and the ValueError string matches the one you're expecting
  This is based on not running the OpenAIClient first, so you are always expecting a none dataframe
  """  
  openaiclient = OpenAIClient(spark_session, input_spark_df="input_spark_df", output_table_name="output_table_name", prompt="prompt", api_key="api_key", endpoint="endpoint")
  actual_output_none = openaiclient.display_results()
  actual_output_none_string = str(actual_output_none)

  expected_output = ValueError("No results to display. Please call call_openai() first.")
  expected_output_string = str(expected_output)

  assert type(actual_output_none) == type(expected_output)
  assert actual_output_none_string == expected_output_string

test_display_results()
  

def test_display_results(openai_client):
    openai_client.results_df = openai_client.spark.createDataFrame(
        [("repo1", "prompt", "token1", "summary")],
        ["repo_name", "prompt", "repo_token_count", "virtual_readme"]
    )

    with patch("builtins.print") as mock_print:
        openai_client.display_results()
        mock_print.assert_called()

def test_display_results_no_results(openai_client):
    with pytest.raises(ValueError):
        openai_client.display_results()
