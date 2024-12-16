import pytest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
import pandas as pd
from src.fleming.code_summary.repo_contents_tokenisation import GitHubRepoDataProcessor  # Replace with your actual module name

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
        pem_file="test.pem"
    )

def test_get_token(github_repo_data_processor):
    with patch("your_module.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"token": "test_token"}
        token = github_repo_data_processor.get_token()
        assert token == "test_token"

def test_num_tokens_from_string(github_repo_data_processor):
    string = "This is a test string."
    encoding_name = "cl100k_base"
    with patch("your_module.tiktoken.get_encoding") as mock_get_encoding:
        mock_get_encoding.return_value.encode.return_value = [1, 2, 3, 4, 5]
        num_tokens = github_repo_data_processor.num_tokens_from_string(string, encoding_name)
        assert num_tokens == 5

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
    with patch.object(github_repo_data_processor, "get_token", return_value="test_token"):
        with patch.object(github_repo_data_processor, "get_new_github_instance") as mock_get_github:
            mock_github = MagicMock()
            mock_get_github.return_value = mock_github
            mock_repo = MagicMock()
            mock_github.get_organization.return_value.get_repo.return_value = mock_repo
            mock_repo.get_contents.return_value = []
            start_time = time.time()
            repo_data = github_repo_data_processor.get_organization_repos_data(mock_github, start_time)
            assert isinstance(repo_data, pd.DataFrame)

def test_data_collection(github_repo_data_processor):
    with patch.object(github_repo_data_processor, "get_token", return_value="test_token"):
        with patch.object(github_repo_data_processor, "get_new_github_instance") as mock_get_github:
            mock_github = MagicMock()
            mock_get_github.return_value = mock_github
            mock_repo = MagicMock()
            mock_github.get_organization.return_value.get_repo.return_value = mock_repo
            mock_repo.get_contents.return_value = []
            repo_data = github_repo_data_processor.data_collection()
            assert isinstance(repo_data, pd.DataFrame)

def test_concatenate_repo_contents(github_repo_data_processor):
    data = {
        "RepoName": ["repo1", "repo1", "repo2"],
        "FileName": ["file1", "file2", "file3"],
        "FilePath": ["path1", "path2", "path3"],
        "DecodedContent": ["content1", "content2", "content3"],
        "TokenCountPerFile": [10, 20, 30],
        "CumulativeRepoContent": [10, 30, 60],
        "DirectoryLevel": [1, 2, 1]
    }
    repo_contents_df = pd.DataFrame(data)
    result_df = github_repo_data_processor.concatenate_repo_contents(repo_contents_df)
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
