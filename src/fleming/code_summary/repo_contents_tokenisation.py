import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from github import Github
import jwt
import tiktoken
from pyspark.sql import DataFrame, SparkSession


class GitHubRepoDataProcessor:
    """
    Class to process data from GitHub repositories. This class ingests the files from a list of repositories in an organization and processes the contents to return a dataframe of the contents concatenated.

    The concatenated data can then be ingest into a model for further processing. For example, the concatenated data can be used to train a model for code summarization.

    The class contains the following methods:

    1. get_token: Get the GitHub token for the GitHub App.
    2. num_tokens_from_string: Get the number of tokens from a string based on the encoding.
    3. nlp_process: Process the HTML content to remove unwanted characters.
    4. get_directory_level: Get the directory level of a file.
    5. calculate_token_count: Calculate the token count of a text.
    6. get_new_github_instance: Get a new GitHub instance.
    7. get_organization_repos_data: Get the data from the repositories in the organization.
    8. data_collection: Collect repostiory contents from the repositories in the organization and return as a dataframe.
    9. concatenate_repo_contents: Concatenate the contents of the repositories into a dataframe.


    Example
    --------
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

    Parameters:
        spark (SparkSession): Spark Session
        organization_name (str): Name of the organization in github
        repo_list (list): List of repositories
        num_token_per_repo (int): Max number of tokens per repository to be collected
        pem_key (str): PEM key for the GitHub App
        pem_file (str): Filepath to store the PEM key

    """

    spark: SparkSession
    organization_name: str
    repo_list: list
    num_token_per_repo: int
    pem_key: str
    pem_file: str

    def __init__(
        self,
        spark: SparkSession,
        organization_name: str,
        repo_list: list,
        num_token_per_repo: int,
        pem_key,
        pem_file,
    ):
        self.spark = spark
        self.organization_name = organization_name
        self.repo_list = repo_list
        self.num_token_per_repo = num_token_per_repo
        self.pem_key = pem_key
        self.pem_file = pem_file
        self.ignore_files = [
            "__init__.py",
            "LICENSE",
            "LICENSE.md",
            "LICENCE",
            "LICENCE.md",
            "CODEOWNERS.md",
            ".gitignore",
            ".gitattributes",
            ".gitmodules",
            ".git",
            ".DS_Store",
            "Thumbs.db",
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "PULL_REQUEST_TEMPLATE.md",
            "ISSUE_TEMPLATE.md",
            "MAINTAINERS.md",
            "GOVERNANCE.md",
            "RELEASE.md",
            "SUPPORT.md",
            "README.md",
            "README.txt",
        ]
        self.ignore_extensions = [
            "whitesource",
            "gitignore",
            "png",
            "jpg",
            "woff2",
            "PNG",
            "woff",
            "gif",
            "csv",
            "xlsx",
            "xls",
        ]

    def get_token(self) -> str:
        """
        Get the GitHub token for the GitHub App. This harnesses the GitHub App installation token.

        Parameters:
            None

        Returns:
            github_token['token'](str): GitHub token for the GitHub App.
        """
        app_id = 340993
        installation_id = 38193318

        with open(self.pem_file, "w") as pem_file_open:
            pem_file_open.write(self.pem_key)

        with open(self.pem_file, "rb") as pem_file_open:
            signing_key = jwt.jwk_from_pem(pem_file_open.read())

        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 600,
            "iss": app_id,
        }

        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, "RS256")

        url = (
            f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        )
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {encoded_jwt}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        github_token = requests.post(url, headers=headers).json()
        return github_token["token"]

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """
        Get the number of tokens from a string based on the encoding.

        Parameters:
            string (str): The string to be tokenized.
            encoding_name (str): The encoding to be used for tokenization.

        Returns:
            len(encoding.encode(string))(int): Number of tokens in the string.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))

    @staticmethod
    def nlp_process(html):
        """
        Process the HTML content to remove unwanted characters.

        Parameters:
            html (str): HTML content to be processed.

        Returns:
            text(str): Processed text content.
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            text = re.sub(r"\[.*?\]", "", text)
            text = re.sub(r"\n", " ", text)
            text = re.sub(r"\n\n", " ", text)
            text = re.sub(r"[_{}*//#\[\]]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text
        except Exception:
            return "Cannot be decoded"

    @staticmethod
    def get_directory_level(file_path):
        return file_path.count("/")

    @staticmethod
    def calculate_token_count(text):
        word_count = len(text.split())
        return word_count * 4 / 3

    def get_new_github_instance(self, token):
        return Github(token)

    def get_organization_repos_data(self, g, start_time):
        """
        Get the data from the repositories in the organization.

        Parameters:
            g (Github): GitHub instance
            start_time (float): Start time of the process.

        Returns:
            repo_contents_df (DataFrame): Dataframe containing the repository contents.

        """
        files = []
        print("\nBeginning data collection process...")
        for repo_item in self.repo_list:
            if time.time() > start_time + 3540:
                sleep_time = 65
                print(
                    f"Putting to sleep for {sleep_time}, reason: near 60 min runtime."
                )
                time.sleep(sleep_time)
                start_time = time.time()
                g = self.get_new_github_instance(self.get_token())

            try:
                repo = g.get_organization(self.organization_name).get_repo(repo_item)
                contents = repo.get_contents("")
                num_token_collected = 0
                while contents and num_token_collected < self.num_token_per_repo:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        contents.extend(repo.get_contents(file_content.path))
                    else:
                        file_name = file_content.path.split("/")[-1]
                        if file_name not in self.ignore_files:
                            file_extension = file_name.split(".")[-1]
                            if file_extension not in self.ignore_extensions:
                                try:
                                    if file_extension == "sql":
                                        decoded_content = file_content.decoded_content
                                    else:
                                        decoded_content = (
                                            file_content.decoded_content.decode("utf-8")
                                        )

                                    cleaned_content = self.nlp_process(decoded_content)
                                    token_count = self.num_tokens_from_string(
                                        cleaned_content, "cl100k_base"
                                    )
                                    directory_level = self.get_directory_level(
                                        file_content.path
                                    )
                                    if (
                                        num_token_collected + token_count
                                        <= self.num_token_per_repo
                                    ):
                                        num_token_collected += token_count
                                        files.append(
                                            (
                                                repo_item,
                                                file_content.name,
                                                file_content.path,
                                                cleaned_content,
                                                token_count,
                                                num_token_collected,
                                                directory_level,
                                            )
                                        )
                                except Exception as e:
                                    print(
                                        f"Error decoding file from repository {repo_item}: {e}"
                                    )
                                    print("Problem file: ", file_content.path)
            except Exception as e:
                print(f"Error for repository {repo_item}: {e}")

        repo_contents_df = pd.DataFrame(
            files,
            columns=[
                "RepoName",
                "FileName",
                "FilePath",
                "DecodedContent",
                "TokenCountPerFile",
                "CumulativeRepoContent",
                "DirectoryLevel",
            ],
        )

        return repo_contents_df

    def data_collection(self):
        """
        Collect repostiory contents from the repositories in the organization and return as a dataframe.

        Parameters:
            None

        Returns:
            repo_contents_df (DataFrame): Dataframe containing the repository contents.

        """
        token = self.get_token()
        start_time = time.time()
        g = self.get_new_github_instance(token)

        repo_contents_df = self.get_organization_repos_data(g, start_time)
        return repo_contents_df

    def concatenate_repo_contents(self, repo_contents_df):
        """
        Concatenate the contents of the repositories into a dataframe.

        Parameters:
            repo_contents_df (DataFrame): Dataframe containing the repository contents.

        Returns:
            result_df (DataFrame): Dataframe containing the concatenated contents of the repositories.
        """
        result = []
        grouped = repo_contents_df.groupby("RepoName")

        for repo_name, group in grouped:
            group = group[group["decoded_content"].str.strip() != ""]
            concatenated_content = ", ".join(group["decoded_content"])
            total_token_count = group["token_count_per_file"].sum()
            files_included = ", ".join(group["file_name"])
            result.append(
                (repo_name, concatenated_content, total_token_count, files_included)
            )

        result_df = pd.DataFrame(
            result,
            columns=[
                "RepoName",
                "ConcatenatedContent",
                "TotalTokenCount",
                "FilesIncluded",
            ],
        )
        return result_df
