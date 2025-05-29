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

import logging
from pyspark.sql.functions import (
    col,
    lit,
    expr,
    create_map,
    to_json,
    concat_ws,
    regexp_replace,
)
from pyspark.sql import DataFrame, SparkSession


class CorpusTextCreation:
    """
    Class to create the corpus txt file for the semantic search model from a dataframe.

    The class contains the following methods:

    1. concat_columns: Concatenate the columns to create the corpus from the dataframe. This will take all the columns in the dataframe and concatenate them to create the corpus in the correct format for the Fleming Frontend.
    2. write_corpus_to_file: Write the corpus to a file from the concatenated columns.

      Example
    --------
    ```python

    from fleming.discovery.corpus_creation import CorpusCreation
    from pyspark.sql import SparkSession

    # Not required if using Databricks
    spark = SparkSession.builder.appName("corpus_creation").getOrCreate()

    corpus_df = spark.read.csv("/tmp/corpus.csv", header=True, inferSchema=True)
    corpus_file_path = "/tmp/search_corpus.txt"

    corpus_creation = CorpusCreation(corpus_df, corpus_file_path)
    corpus = corpus_creation.concat_columns("RepoName", "RepoLink", "RepoDescription")
    corpus_creation.write_corpus_to_file(corpus)

    ```


    Parameters:
        spark (SparkSession): Spark Session
        corpus_df (df): Source dataframe of the corpus
        corpus_file_path (str): File path to write the corpus

    """

    spark: SparkSession
    corpus_df: DataFrame
    corpus_file_path: str

    def __init__(
        self, spark: SparkSession, corpus_df: DataFrame, corpus_file_path: str
    ) -> None:
        self.spark = spark
        self.corpus_df = corpus_df
        self.corpus_file_path = corpus_file_path

    def concat_columns(self) -> list:
        """
        Concatenate the columns to create the corpus

        Parameters:
        None

        Returns:
        corpus(list): List of concatenated columns

        """
        df = self.corpus_df.withColumn(
            "ConcatColumns", concat_ws(" ", *self.corpus_df.columns)
        )

        corpus = [row["ConcatColumns"] for row in df.collect()]

        return corpus

    def concat_columns(
        self, df, item_name_column, item_link_column, item_summmary_column
    ) -> list:
        """
        Concatenate the columns to create the corpus

        Parameters:
        df(df): Cleaned dataframe

        Returns:
        corpus(list): List of concatenated columns with the format of each string consising of the following:

        Example:
        {"Name":"Fleming","Link":"https://github.com/sede-open/Fleming","Summary":"Open-source project of the \"brain\" of the ai discovery tool. Includes technical scripts to build, register, serve and query models on databricks. Models can be run on cpu and not gpu providing signiifcant cost reductions. Databricks is utilized to build and train machine learning models on the ingested data. "}{"filter":{"LicenceFileContent":"Apache License 2.0","Archived":"Active"}}

        """

        exclude_cols = [item_name_column, item_link_column, item_summmary_column]
        include_cols = [c for c in df.columns if c not in exclude_cols]
        map_expr = create_map(
            *[item for c in include_cols for item in (lit(c), col(c))]
        )
        df = df.withColumn("filter", map_expr)

        df = df.withColumn(
            "dict_column",
            expr(
                f"map('Name', {item_name_column}, 'Link', {item_link_column}, 'Summary', {item_summmary_column})"
            ),
        )

        df = df.withColumn("filter", create_map(lit("filter"), col("filter")))

        df = df.withColumn("filter", to_json(col("filter")))
        df = df.withColumn("dict_column", to_json(col("dict_column")))

        df = df.withColumn(
            "ReadMe_W_Answer", concat_ws("", col("dict_column"), col("filter"))
        )
        df = df.withColumn(
            "ReadMe_W_Answer", regexp_replace("ReadMe_W_Answer", r"\}\{", ",")
        )

        # COLLECTING ONLY THE README_W_ANSWER TEXT INFORMATION AS THE CORPUS
        corpus = [row["ReadMe_W_Answer"] for row in df.collect()]

        return corpus

    def write_corpus_to_file(self, corpus) -> None:
        """
        Write the corpus to a file

        Parameters:
        corpus(list): List of concatenated columns

        Returns:
        None
        """
        with open(self.corpus_file_path, "w") as file:
            for sentence in corpus:
                try:
                    file.write(sentence + "\n")
                    print(sentence)
                except Exception as e:
                    logging.exception(str(e))
                    raise e
