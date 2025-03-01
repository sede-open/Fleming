
# Create the Corpus

# Documentation

The first step is to create a corpus.txt file, this includes all the values you will search over. The below function ingests a dataframe each row being a seperate entry into the corpus. 

Please find an example below.

For more information about options within the Class please follow the documentation under the [code-reference](../code-reference/CorpusTextCreation.md) section.

# Example

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
