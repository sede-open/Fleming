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

import mlflow
import pytest
import torch

from src.fleming.discovery.model_train_register import ModelTrainRegister

import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


@pytest.fixture
def model_train_register(spark_session):
    return ModelTrainRegister(
        spark=spark_session,
        model_directory="/tmp/test_model",
        corpus_file="/tmp/test_corpus.txt",
        corpus_embedding_file="/tmp/test_corpus_embedding.pt",
        semantic_search_model="multi-qa-mpnet-base-dot-v1",
    )


def test_initialization(model_train_register):
    assert model_train_register.model_directory == "/tmp/test_model"
    assert model_train_register.corpus_file == "/tmp/test_corpus.txt"
    assert model_train_register.corpus_embedding_file == "/tmp/test_corpus_embedding.pt"
    assert model_train_register.semantic_search_model == "multi-qa-mpnet-base-dot-v1"


def test_register_model(mocker, model_train_register):
    mocker.patch("sentence_transformers.SentenceTransformer")
    model_train_register.register_model()


def test_embed_corpus(mocker, model_train_register):
    mocker.patch("sentence_transformers.SentenceTransformer")
    mocker.patch("torch.save")

    model_train_register.embed_corpus()

    torch.save.assert_called_once()


def test_create_registered_model(mocker, model_train_register):
    mocker.patch("mlflow.set_experiment")
    mocker.patch("mlflow.start_run")
    mocker.patch("mlflow.pyfunc.log_model")
    mocker.patch("mlflow.register_model")

    model_train_register.create_registered_model(
        unique_model_name="test_model",
        input_example=["example"],
        signature=None,
        artifacts={},
        experiment_location="/tmp/experiment",
    )

    mlflow.set_experiment.assert_called_once_with("/tmp/experiment")
    mlflow.start_run.assert_called_once()
    mlflow.pyfunc.log_model.assert_called_once()
    mlflow.register_model.assert_called_once()
