import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from github import Github
import jwt
import tiktoken

class RepoDataProcessor:
    def __init__(self, data, organization_name, repo_list, num_token_per_repo):
        self.data = data
        self.organization_name = organization_name
        self.repo_list = repo_list
        self.num_token_per_repo = num_token_per_repo
        self.ignore_files = ['__init__.py', 'LICENSE','LICENSE.md','LICENCE','LICENCE.md', 'CODEOWNERS.md', '.gitignore', '.gitattributes', '.gitmodules', '.git', '.DS_Store', 'Thumbs.db', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md', 'SECURITY.md', 'PULL_REQUEST_TEMPLATE.md', 'ISSUE_TEMPLATE.md', 'MAINTAINERS.md', 'GOVERNANCE.md', 'RELEASE.md', 'SUPPORT.md', 'README.md', 'README.txt']
        self.ignore_extensions = ['whitesource', 'gitignore', 'png', 'jpg', 'woff2', 'PNG', 'woff', 'gif', 'csv', 'xlsx', 'xls']

    def get_token(self):
        app_id = 340993
        installation_id = 38193318

        pem_key = dbutils.secrets.get(scope="InnerSource-Secrets", key="InnerSource-GithubAPP")
        pem = "/dbfs/FileStore/github_app/innersource_dashboard_private_key.pem"
        with open(pem, 'w') as pem_file:
            pem_file.write(pem_key)

        with open(pem, 'rb') as pem_file:
            signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {
            'iat': int(time.time()),
            'exp': int(time.time()) + 600,
            'iss': app_id
        }

        jwt_instance = jwt.JWT()
        encoded_jwt = jwt_instance.encode(payload, signing_key, 'RS256')

        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {encoded_jwt}',
            'X-GitHub-Api-Version': '2022-11-28'
        }

        token = requests.post(url, headers=headers).json()
        return token['token']

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))

    @staticmethod
    def nlp_process(html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'\[.*?\]', '', text)
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'\n\n', ' ', text)
            text = re.sub(r'[_{}*//#\[\]]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        except Exception:
            return "Cannot be decoded"

    @staticmethod
    def get_directory_level(file_path):
        return file_path.count('/')

    @staticmethod
    def calculate_token_count(text):
        word_count = len(text.split())
        return word_count * 4 / 3

    def get_new_github_instance(self, token):
        return Github(token)

    def get_organization_repos_data(self, g, start_time):
        files = []
        print('\nBeginning data collection process...')
        for repo_item in self.repo_list:
            if time.time() > start_time + 3540:
                sleep_time = 65
                print(f'Putting to sleep for {sleep_time}, reason: near 60 min runtime.')
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
                        file_name = file_content.path.split('/')[-1]
                        if file_name not in self.ignore_files:
                            file_extension = file_name.split('.')[-1]
                            if file_extension not in self.ignore_extensions:
                                try:
                                    if file_extension == 'sql':
                                        decoded_content = file_content.decoded_content
                                    else:
                                        decoded_content = file_content.decoded_content.decode('utf-8')

                                    cleaned_content = self.nlp_process(decoded_content)
                                    token_count = self.num_tokens_from_string(cleaned_content, "cl100k_base")
                                    directory_level = self.get_directory_level(file_content.path)
                                    if num_token_collected + token_count <= self.num_token_per_repo:
                                        num_token_collected += token_count
                                        files.append((repo_item, file_content.name, file_content.path, cleaned_content, token_count, num_token_collected, directory_level))
                                except Exception as e:
                                    print(f'Error processing repository {repo_item}: {e}')
                                except Exception as e:
                                    print(f'Error decoding file from repository {repo_item}: {e}')
                                    print('Problem file: ', file_content.path)
            except Exception as e:
                print(f'Error for repository {repo_item}: {e}')

        repo_contents_df = pd.DataFrame(files, columns=["repo_name", "file_name", "file_path", "decoded_content", "token_count_per_file", "cumulative_repo_content", "directory_level"])
        return repo_contents_df

    def data_collection(self):
        token = self.get_token()
        start_time = time.time()
        g = self.get_new_github_instance(token)

        print('\nGetting list of repositories...')
        elapsed_time = (time.time() - start_time) / 60
        print(f'\nDone!\n{len(self.repo_list)} repositories identified in:{elapsed_time:.2f} minutes')

        data = self.get_organization_repos_data(g, start_time)
        print(f'Data collection completed. Collected data for {len(data)} files.')
        return data

    def concatenate_repo_contents(self, data):
        result = []
        grouped = data.groupby('repo_name')

        for repo_name, group in grouped:
            group = group[group['decoded_content'].str.strip() != '']
            concatenated_content = ', '.join(group['decoded_content'])
            total_token_count = group['token_count_per_file'].sum()
            files_included = ', '.join(group['file_name'])
            result.append((repo_name, concatenated_content, total_token_count, files_included))

        result_df = pd.DataFrame(result, columns=['repo_name', 'concatenated_content', 'total_token_count', 'files_included'])
        return result_df