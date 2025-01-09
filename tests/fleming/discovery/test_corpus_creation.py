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
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


@pytest.fixture
def corpus_df(spark_session):
    data = [("John", "Doe", 30), ("Jane", "Doe", 25)]
    columns = ["first_name", "last_name", "age"]
    return spark_session.createDataFrame(data, columns)


@pytest.fixture
def corpus_file_path():
    return "/tmp/test_corpus.txt"


def test_concat_columns(corpus_df):
    corpus_file_path = "/tmp/test_corpus.txt"
    corpus_creation = CorpusTextCreation(spark_session, corpus_df, corpus_file_path)
    concatenated_list = corpus_creation.concat_columns()
    expected_list = ["John Doe 30", "Jane Doe 25"]
    assert concatenated_list == expected_list


def test_write_corpus_to_file(corpus_df):
    corpus_file_path = "/tmp/test_corpus.txt"
    corpus_creation = CorpusTextCreation(spark_session, corpus_df, corpus_file_path)
    concatenated_df = corpus_creation.concat_columns()
    corpus_creation.write_corpus_to_file(concatenated_df)
