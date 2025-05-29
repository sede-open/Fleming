# Serve the Registered Model

# Documentation

After the model has been registered it is now possible to serve the model with the databricks serving endpoint. A unique part of Fleming is that models created can be run on Small CPU Clusters which is both cost and energy efficient.

Please find an example below.

For more information about options within the Class please follow the documentation under the [code-reference](../code-reference/ModelServe.md) section.

```python  

from fleming.discovery.model_serve import ModelServewithMosaicAI, ModelServe
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

# You can now choose how you serve your model, with or without Mosaic AI

model_serve = ModelServe(endpoint_name, model_name, workload_type, workload_size, scale_to_zero, API_ROOT, API_TOKEN)
model_serve.deploy_endpoint()

model_serve = ModelServewithMosaicAI(endpoint_name, model_name, workload_type, workload_size, scale_to_zero, API_ROOT, API_TOKEN)
model_serve.deploy_endpoint()
```