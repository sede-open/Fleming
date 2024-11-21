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

import requests
from mlflow.deployments import get_deploy_client
from mlflow.tracking import MlflowClient
from pyspark.sql import SparkSession


class ModelServe:
    """
    A class which allows for creating a model serving endpoint on databricks.

    Example:
    --------
    ```python

    from fleming.discovery.corpus_creation import CorpusCreation
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
    latest_version = max(MlflowClient().get_latest_versions(model_name), key=lambda v: v.version)
    model_version = latest_version.version
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

    model_serve = ModelServe(endpoint_name, model_name, workload_type, workload_size, scale_to_zero, API_ROOT, API_TOKEN)
    model_serve.deploy_endpoint()

    ```

    Parameters:
        endpoint_name (str): The name of the model serving endpoint.
        model_name (str): The name of the model to be served.
        workload_type (str): The type of compute to be used for the endpoint.
        workload_size (str): The scale-out size of the compute.
        scale_to_zero (bool): Whether to scale the compute to zero when not in use.
        API_ROOT (str): The API root of the Databricks workspace.
        API_TOKEN (str): The API token of the Databricks workspace.
    """

    spark: SparkSession
    endpoint_name: str
    model_name: str
    workload_type: str
    workload_size: str
    scale_to_zero: bool
    API_ROOT: str
    API_TOKEN: str

    def __init__(
        self,
        spark: SparkSession,
        endpoint_name: str,
        model_name: str,
        workload_type: str,
        workload_size: str,
        scale_to_zero: str,
        API_ROOT: str = None,
        API_TOKEN: str = None,
    ) -> None:
        self.spark = spark
        self.endpoint_name = endpoint_name
        self.model_name = model_name
        self.workload_type = workload_type
        self.workload_size = workload_size
        self.scale_to_zero = scale_to_zero
        self.API_ROOT = API_ROOT
        self.API_TOKEN = API_TOKEN

    def deploy_endpoint(self) -> None:
        """
        Create the model serving endpoint on Databricks

        """

        try:
            client = get_deploy_client("databricks")
            client.create_endpoint(
                name=self.endpoint_name,
                config={
                    "served_entities": [
                        {
                            "name": self.model_name,
                            "entity_name": self.model_name,
                            "entity_version": MlflowClient()
                            .get_registered_model(self.model_name)
                            .latest_versions[1]
                            .version,
                            "workload_type": self.workload_type,
                            "workload_size": self.workload_size,
                            "scale_to_zero_enabled": self.scale_to_zero,
                        }
                    ],
                    "traffic_config": {
                        "routes": [
                            {
                                "served_model_name": self.model_name,
                                "traffic_percentage": 100,
                            }
                        ]
                    },
                },
            )
        except requests.exceptions.RequestException as e:
            put_url = "/api/2.0/serving-endpoints/{}/config".format(self.endpoint_name)
            put_url

            data = {
                "name": self.endpoint_name,
                "config": {
                    "served_entities": [
                        {
                            "name": self.model_name,
                            "entity_name": self.model_name,
                            "entity_version": max(
                                MlflowClient().get_latest_versions(self.model_name),
                                key=lambda v: v.version,
                            ).version,
                            "workload_type": self.workload_type,
                            "workload_size": self.workload_size,
                            "scale_to_zero_enabled": self.scale_to_zero,
                        }
                    ],
                    "traffic_config": {
                        "routes": [
                            {
                                "served_model_name": self.model_name,
                                "traffic_percentage": 100,
                            }
                        ]
                    },
                },
            }

            headers = {
                "Context-Type": "text/json",
                "Authorization": f"Bearer {self.API_TOKEN}",
            }

            response = requests.put(
                url=f"{self.API_ROOT}{put_url}", json=data["config"], headers=headers
            )

            if response.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"Request failed with status {response.status_code}, {response.text}"
                )

            return response.json()
            raise