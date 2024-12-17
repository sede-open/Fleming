
# Extracting GitHub Repo Contents and Concatenating for Summarisation

# Documentation

To prepare a github repository to be summarised it is important to extract all relevant files and concantenate the information. This class ingests the files from a list of repositories in an organization and processes the contents to return a dataframe of the contents concatenated.

Different summerisation tools will have different limits on the number of tokens which can be ingested, the below class allows you to limit this for each repository ingested. 

Please find an example below.

For more information about options within the Class please follow the documentation under the [code-reference](../code-reference/RepoContentsTokenisation.md) section.

# Example

```python

from fleming.code_summary.repo_contents_tokenisation import GitHubRepoDataProcessor
from pyspark.sql import SparkSession

# Not required if using Databricks
spark = SparkSession.builder.appName("RepoConcat").getOrCreate()

organization_name = 'company-x'
repo_list = ['repo1', 'repo2', 'repo3']
num_token_per_repo = 100000
pem_key = 'xxxxx'
pem_file = '/dbfs/FileStore/github_app/pem_key.pem'

github_repo_data_processor = GitHubRepoDataProcessor(spark, organization_name, repo_list, num_token_per_repo, pem_key, pem_file)
repo_contents_df = github_repo_data_processor.data_collection()
repo_contents_df_concat = github_repo_data_processor.concatenate_repo_contents(repo_contents_df)

```