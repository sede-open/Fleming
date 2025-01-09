import logging
import requests
from pyspark.sql import DataFrame, SparkSession


class OpenAIClient:
    """
    Class to interact with the OpenAI API to generate content based on a prompt and source code.

    The class contains the following methods:

    1. call_openai: Call the OpenAI API to generate documentation with AI based on the provided prompt and source code.
    2. save_results: Save the generated results to a specified output table.

    Example
    --------
    ```python
    from fleming.code_summary.fourO_mini_summary import call_openai
    from pyspark.sql import SparkSession

    # Not required if using Databricks
    spark = SparkSession.builder.appName("openai_client").getOrCreate()

    spark_input_df = "your_spark_input_df"
    output_table_name = "your_output_table"
    prompt = "Your prompt here"

    client = OpenAIClient(spark, delta_table, output_table_name, prompt)
    client.call_openai()
    ```

    Parameters:
        spark (SparkSession): Spark Session
        input_spark_df (DataFrame): Source spark DataFrame containing the input data
        output_table_name (str): Name of the output table to save results
        prompt (str): Prompt to send to the OpenAI API

    Attributes:
        api_key (str): API key for OpenAI
        endpoint (str): Endpoint for OpenAI API
        headers (dict): Headers for the API request
    """

    spark: SparkSession
    input_spark_df: DataFrame
    output_table_name: str
    prompt: str
    api_key: str
    endpoint: str
    headers: dict

    def __init__(
        self,
        spark: SparkSession,
        input_spark_df: DataFrame,
        output_table_name: str,
        prompt: str,
        api_key: str,
        endpoint: str,
    ) -> None:
        self.spark = spark
        self.input_spark_df = input_spark_df
        self.output_table_name = output_table_name
        self.prompt = prompt
        self.api_key = api_key
        self.endpoint = endpoint
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        self.results_df = None  # Initialize an instance variable to store results

    def call_openai(
        self, title: str, concatenated_content: str, total_token_count: str
    ) -> None:
        """
        Call the OpenAI API to generate summarised content based on the provided prompt and source content.

        Parameters:
        title: str - Column name for column containing summarised text title
        concatenated_content: str - Column name for column containing concatenated content
        total_token_count: str - Column name for column containing total token count

        Returns: results_df pyspark dataframe containing summarisation of each entry
        """

        results = []
        repo_contents_df = self.input_spark_df
        repo_contents_df = repo_contents_df.limit(3)

        for row in repo_contents_df.collect():
            input_source_code = row[concatenated_content]
            repo_name = row[title]
            total_token_count = row[total_token_count]

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{self.prompt}{input_source_code}",
                            }
                        ],
                    }
                ],
                "temperature": 0.0,
                "top_p": 0.95,
            }

            try:
                response = requests.post(
                    self.endpoint, headers=self.headers, json=payload
                )
                response.raise_for_status()
                json_dict = response.json()
                output = json_dict["choices"][0]["message"]["content"]
                results.append((repo_name, self.prompt, total_token_count, output))
                print(output)

            except requests.RequestException as e:
                logging.exception("Failed to make the request.")
                raise SystemExit(f"Failed to make the request. Error: {e}")

        self.results_df = self.spark.createDataFrame(
            results, ["repo_name", "prompt", "repo_token_count", "virtual_readme"]
        )

    def display_results(self) -> None:
        """
        Display the generated results.

        Returns:
        results_df dataframe gets displayed
        """
        if self.results_df is not None:
            display(self.results_df)
        else:
            raise ValueError("No results to display. Please call call_openai() first.")

    def save_results(self) -> None:
        """
        Save the generated results to the specified output table.

        Returns:
        None
        """
        if self.results_df is not None:
            self.results_df.write.mode("overwrite").option(
                "mergeSchema", "true"
            ).saveAsTable(f"hive_metastore.dev_innersource.{self.output_table_name}")
        else:
            raise ValueError("No results to save. Please call call_openai() first.")
