Once you have extracted and concatenated the contents of a repository, this class can be used to then generate descriptive documentation using Azure OpenAI. Please note, this class requires you to have a working Azure OpenAI API Key. 

This class then authenticates to the API, and passes in the concatenated repository content with a prompt of your choosing (an example has been provided below). The output is descriptive documentation that identifies code functionality, which can then be indexed by Fleming, to allow users to find specific code functionality that may not have been sufficiently detailed in the readme, or hidden by a domain context.

For more information about options within the Class please follow the documentation under the [code-reference](../code-reference/40-MiniSummary.md) section.

# Example

    ```python
    from fleming.code_summary.fourO_mini_summary import call_openai
    from pyspark.sql import SparkSession

    # Not required if using Databricks
    spark = SparkSession.builder.appName("openai_client").getOrCreate()

    spark_input_df = "your_spark_input_df"
    output_table_name = "your_output_table"

    prompt = "The following code is the contents of a repository, generate a short summary paragraph describing what the repository purpose is. A paragraph detailing the key functionalities and technologies integrate with and a list of key words associated with this repository underneath. Focus on the purpose of the code contained in the repository, and the technologies, data and platforms it integrates with"

    api_key = "your_api_key"
    endpoint = "https://api.openai.com/yourendpointhere"
    
    headers = {
    "Content-Type": "application/json",
    "api-key": api_key,
    }

    client = OpenAIClient(spark, delta_table, output_table_name, prompt, api_key, endpoint, headers)
    client.call_openai()
    ```