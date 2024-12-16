import pytest
from pyspark.sql import SparkSession
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from github import Github
import time

from src.fleming.code_summary.repo_contents_tokenisation import (
    GitHubRepoDataProcessor,
)


@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()


@pytest.fixture
def github_repo_data_processor(spark):
    return GitHubRepoDataProcessor(
        spark=spark,
        organization_name="test_org",
        repo_list=["repo1", "repo2"],
        num_token_per_repo=100000,
        pem_key="test_key",
        pem_file="test.pem",
    )


def test_get_token(github_repo_data_processor):
    try:
        token=github_repo_data_processor.get_token()
    except:
        token=None
    assert token is None
    


def test_num_tokens_from_string(github_repo_data_processor):
    string = "This is a test string."
    encoding_name = "cl100k_base"
    num_tokens = github_repo_data_processor.num_tokens_from_string(
            string, encoding_name
        )
    print(num_tokens)
    assert num_tokens == 6


def test_nlp_process():
    html = "<html><body><p>This is a test.</p></body></html>"
    processed_text = GitHubRepoDataProcessor.nlp_process(html)
    assert processed_text == "This is a test."


def test_get_directory_level():
    file_path = "dir1/dir2/file.txt"
    level = GitHubRepoDataProcessor.get_directory_level(file_path)
    assert level == 2


def test_calculate_token_count():
    text = "This is a test string with several words."
    token_count = GitHubRepoDataProcessor.calculate_token_count(text)
    assert token_count == pytest.approx(10.67, 0.1)


def test_get_new_github_instance(github_repo_data_processor):
    token = "test_token"
    github_instance = github_repo_data_processor.get_new_github_instance(token)
    assert isinstance(github_instance, Github)


def test_get_organization_repos_data(github_repo_data_processor):
    with patch.object(
        github_repo_data_processor, "get_token", return_value="test_token"
    ):
        with patch.object(
            github_repo_data_processor, "get_new_github_instance"
        ) as mock_get_github:
            mock_github = MagicMock()
            mock_get_github.return_value = mock_github
            mock_repo = MagicMock()
            mock_github.get_organization.return_value.get_repo.return_value = mock_repo
            mock_repo.get_contents.return_value = []
            start_time = time.time()
            repo_data = github_repo_data_processor.get_organization_repos_data(
                mock_github, start_time
            )
            assert isinstance(repo_data, pd.DataFrame)


def test_data_collection(github_repo_data_processor):
    with patch.object(
        github_repo_data_processor, "get_token", return_value="test_token"
    ):
        with patch.object(
            github_repo_data_processor, "get_new_github_instance"
        ) as mock_get_github:
            mock_github = MagicMock()
            mock_get_github.return_value = mock_github
            mock_repo = MagicMock()
            mock_github.get_organization.return_value.get_repo.return_value = mock_repo
            mock_repo.get_contents.return_value = []
            repo_data = github_repo_data_processor.data_collection()
            assert isinstance(repo_data, pd.DataFrame)


def test_concatenate_repo_contents(github_repo_data_processor):
    data = {'RepoName': {0: 'test_repo', 1: 'test_repo', 2: 'test_repo'},
    'FileName': {0: 'CONTRIBUTION.md',
    1: 'sonar-project.properties',
    2: 'evaluate.py'},
    'FilePath': {0: 'CONTRIBUTION.md',
    1: 'sonar-project.properties',
    2: 'aiacs/evaluate_aiacs.py'},
    'DecodedContent': {0: 'Contribution Model - Please create a PR to contribute',
    1: 'sonar.projectKey=yyyyyyy',
    2: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'},    
    'TokenCountPerFile': {0: 10, 1: 10, 2: 3297},
    'CumulativeRepoContent': {0: 10, 1: 20, 2: 3317},
    'DirectoryLevel': {0: 0, 1: 0, 2: 1}}
    
    repo_contents_df = pd.DataFrame(data)
    result_df = github_repo_data_processor.concatenate_repo_contents(repo_contents_df)

    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
