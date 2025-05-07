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

from src.fleming.discovery.corpus_creation import CorpusTextCreation
from tests.conftest import spark_session


@pytest.fixture
def corpus_df(spark_session):
    data = [
        (
            "John",
            "Doe",
            30,
            "John is a tall man with skills in databricks.",
            "http//www.example.com",
        ),
        (
            "Jane",
            "Doe",
            25,
            "Jane is a short woman with skills in python.",
            "http//www.example.come",
        ),
    ]
    columns = ["first_name", "last_name", "age", "description", "link"]
    return spark_session.createDataFrame(data, columns)


@pytest.fixture
def corpus_file_path():
    return "/tmp/test_corpus.txt"


def test_concat_columns(corpus_df):
    corpus_file_path = "/tmp/test_corpus.txt"
    corpus_creation = CorpusTextCreation(spark_session, corpus_df, corpus_file_path)
    concatenated_list = corpus_creation.concat_columns(
        corpus_df,
        item_name_column="first_name",
        item_link_column="link",
        item_summmary_column="description",
    )
    expected_list = [
        '{"Name":"John","Link":"http//www.example.com","Summary":"John is a tall man with skills in databricks."}{"filter":{"last_name":"Doe","age":"30"}}',
        '{"Name":"Jane","Link":"http//www.example.come","Summary":"Jane is a short woman with skills in python."}{"filter":{"last_name":"Doe","age":"25"}}',
    ]
    assert concatenated_list == expected_list


def test_write_corpus_to_file(corpus_df):
    corpus_file_path = "/tmp/test_corpus.txt"
    corpus_creation = CorpusTextCreation(spark_session, corpus_df, corpus_file_path)
    concatenated_df = corpus_creation.concat_columns(
        corpus_df, "first_name", "link", "description"
    )
    corpus_creation.write_corpus_to_file(concatenated_df)
