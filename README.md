# Fleming

<img align="right" src="docs/images/logo.png" title="Logo Discovery" alt="Logo Discovery" width="33%"></a>

An open-source project of the "brain" of the AI Discovery Tool. Including technical scripts to build, register, serve and query models on databricks which use Semantic Search. These models can be run on cpu and not gpu providing signiifcant cost reductions.

[Databricks](https://www.databricks.com), a popular big data processing and analytics platform, is utilized to build and train machine learning models on the ingested data.

By combining data ingestion from GitHub with Databricks' model training and serving capabilities, pipelines can provide a seamless end-to-end solution for processing and analyzing data from GitHub repositories.

The serving endpoint designed to process and analyze large volumes of data, enabling efficient data discovery and insights.

## Corpus Creation

Class to create the corpus txt file for the semantic search model from a dataframe.

The class contains the following methods:   

1. concat_columns: Concatenate the columns to create the corpus from the dataframe. This will take all the columns in the dataframe and concatenate them to create the corpus.

2. write_corpus_to_file: Write the corpus to a file from the concatenated columns.

```python
from fleming.discovery.corpus_creation import CorpusCreation
from pyspark.sql import SparkSession

# Not required if using Databricks
spark = SparkSession.builder.appName("corpus_creation").getOrCreate()

corpus_df = spark.read.csv("/tmp/corpus.csv", header=True, inferSchema=True)
corpus_file_path = "/tmp/search_corpus.txt"

corpus_creation = CorpusCreation(corpus_df, corpus_file_path)
corpus = corpus_creation.concat_columns(df_analytics_cleaned)
corpus_creation.write_corpus_to_file(corpus)
```

## Model Creation and Registering

A class to train and register a semantic search model.

```python
from fleming.discovery.model_train_register import ModelTrainRegister, SemanticSearchModel    
from pyspark.sql import SparkSession

# Not required if using Databricks
spark = SparkSession.builder.appName("model_serving").getOrCreate()

model_directory = "/tmp/BERT_Semantic_Search_model"
corpus_file = "/tmp/search_corpus.txt"
corpus_embedding_file = '/tmp/corpus_embedding.pt'

model_developer = ModelTrainRegister(spark, model_directory, corpus_file, corpus_embedding_file)

# Register the model
semantic_search_model = "multi-qa-mpnet-base-dot-v1"
model_developer.register_model(semantic_search_model)

# Embed the corpus
model_developer.embed_corpus()

# Define parameters and artifacts
parameters = {"top_k": 50, "relevancy_score": 0.45}
input_example = ["InnerSource best practices"]
test_output = ["match 1", "match 2"]
signature = infer_signature(input_example, test_output, params=parameters)
artifacts = {
    "model_path": model_directory,
    "corpus_file": corpus_file,
    "corpus_embedding_file": corpus_embedding_file
}
unique_model_name = "semantic_search_model"

# Create and serve the model
experiment_location = "/path/to/experiment"
model_developer.create_registered_model(unique_model_name, input_example, signature, artifacts, experiment_location)
```

## Model Serving

This class creates a model serving endpoint on databricks.
   
```python
from fleming.discovery.corpus_creation import CorpusCreation
from pyspark.sql import SparkSession

# Not required if using Databricks
spark = SparkSession.builder.appName("model_serving").getOrCreate()

# Set the name of the MLflow endpoint
endpoint_name = "aidiscoverytool"
print(f'Endpoint name: {endpoint_name}')

# Name of the registered MLflow model
model_name = "BERT_Semantic_Search" 
print(f'Model name: {model_name}')

# Get the latest version of the MLflow model
model_version = MlflowClient().get_registered_model(model_name).latest_versions[1].version 
print(f'Model version: {model_version}')

# Specify the type of compute (CPU, GPU_SMALL, GPU_LARGE, etc.)
workload_type = "CPU"
print(f'Workload type: {workload_type}')

# Specify the scale-out size of compute (Small, Medium, Large, etc.)
workload_size = "Small"
print(f'Workload size: {workload_size}')

# Specify Scale to Zero(only supported for CPU endpoints)
scale_to_zero = False
print(f'Scale to zero: {scale_to_zero}')

API_ROOT = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
API_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

model_serve = ModelServe(endpoint_name, model_name, workload_type, workload_size, scale_to_zero, API_ROOT, API_TOKEN)
model_serve.deploy_endpoint()
```

## Model Querying

A class which allows for querying a model serving endpoint on databricks.

This class is used to query a model serving endpoint on databricks with a dataset.

```python
url = "https://example.com/model_endpoint"
token = "your_auth_token"
    
# Create an instance of ModelQuery
model_query = ModelQuery(url, token)
    
# Example dataset
dataset = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
    
try:
    # Score the model using the dataset
    response = model_query.score_model(dataset)
    print(response)
except requests.exceptions.HTTPError as e:
    print(f"Error: {str(e)}")
```

## Github Repository Extraction and Tokenisation

This class ingests the files from a list of repositories in an organization and processes the contents to return a dataframe of the contents concatenated.

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
## Code Summarisation

This class authenticates to the Azure OpenAI API and passes the concatenated repository contents into the LLM with an accompanying prompt to generate documentation. 

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


# Repository Guidelines

## Folder Structure

| Folder Name        | Description                                                          |
|--------------------|----------------------------------------------------------------------|
|`.github/workflows` | yml files for Github Action workflows                                | 
|`src`               | Main projects and all souce code, organised by language and sdk name |
|`tests`             | Test projects and unit tests, organised by language and sdk name     |

## File Structure

| File Name        | Description                                                                             |
|------------------|-----------------------------------------------------------------------------------------|
|`setup.py`        | Set up requirements for python package deployment                                       |
|`environment.yml` | yml file to create an environment with all the dependencies for developers              |
|`CODE_OF_CONDUCT.md` | code of conduct                                                                         |
|`CODEOWNERS.md`      | codeowners                                                                              |
|`CONTRIBUTING.md`| contributing                                                                            |
|`LICENSE`     | license                                                                                 |
|`RELEASE.md`     | releases                                                                                |
|`SUPPORT.md`     | support                                                                                 |
|`README.md`      |  read me documentation                                                             |
|`.gitignore`      | Informs Git which files to ignore when committing your project to the GitHub repository |

# Developer Guide - How to Use

## Prerequisite

### Python

There are a few things to note before using the Fleming. The following prerequisites will need to be installed on your local machine.

Python version 3.9 >= and < 3.12 should be installed. Check which python version you have with the following command:

    python --version

Find the latest python version [here](https://www.python.org/downloads/) and ensure your python path is set up correctly on your machine.

### Python Package Installers

Installing Fleming can be done using the package installer [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

### Java

To use Fleming in your own environment that leverages [pyspark](https://spark.apache.org/docs/latest/api/python/getting_started/install.html), Java 8 or later is a [prerequisite](https://spark.apache.org/docs/latest/api/python/getting_started/install.html#dependencies). See below for suggestions to install Java in your development environment.

Follow the official Java JDK installation documentation [here.](https://docs.oracle.com/en/java/javase/11/install/overview-jdk-installation.html)

- [Windows](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html)
- [Mac OS](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-macos.html)
- [Linux](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-linux-platforms.html)

!!! note 
    Windows requires an additional installation of a file called **winutils.exe**. Please see this [repo](https://github.com/steveloughran/winutils) for more information.

## Getting Started 

1) To get started with developing for this project, clone the repository. 
```
    git clone https://github.com/sede-open/Fleming.git
```
2) Open the repository in VS Code, Visual Studio or your preferred code editor.

3) Create a new environment using the following command:
```
    micromamba create -f environment.yml
```

> **_NOTE:_**  You will need to have conda, python and pip installed to use the command above.

4) Activate your newly set up environment using the following command:
```
    micromamba activate fleming
```
You are now ready to start developing your own functions. Please remember to follow Felming's development lifecycle to maintain clarity and efficiency for a fully robust self serving platform. 

5) For better readability of code is would be useful to enable black and isort on autosave by simply adding this to the VSCode user settings json(Ctrl + Shft + P):

```
    {
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "python.formatting.blackArgs": [
            "--line-length=119"
        ],
        "python.sortImports.args": [
            "--profile",
            "black"
        ],
        "[python]": {
            "editor.codeActionsOnSave": {
                "source.organizeImports": true
            }
        }
    }
```
    
## Development Lifecycle

1) Develop

2) Write unit tests

3) Document

4) Publish

> **_NOTE:_**  Ensure you have read the [Release Guidelines](RELEASE.md) before publishing your code.

# Support and contacts

If you encounter any issues or have questions, please reach out to the team by raising an issue on the repo. They will be happy to assist you and provide further information about the project.

# Contributing

Contributions to this project are welcome! If you would like to contribute, please refer to our [Contributing Guide](CONTRIBUTION.md) for guidelines on how to get started. We appreciate your support in making this project even better.

# Licensing

The code in this repository is licensed under the default copyright notice, which can be found in the [LICENSE](LICENSE) file. Please review the license before using or distributing the code.
