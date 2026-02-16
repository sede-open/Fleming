# Copyright 2024
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

"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""


import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README-PYPI.md").read_text()


INSTALL_REQUIRES = [
    "pytest==7.4.0",
    "pyspark>=3.3.0,<3.6.0",
    "pytest-mock>=3.14.0",
    "sentence-transformers>=3.2.0",
    "mlflow>=2.0.1",  # Updated to a secure version
    "black>=24.1.0",
    "nltk>=3.8.2",  # Updated to a secure version,
    "torch>=2.4.1",
    "tiktoken>=0.8.0",
    "time>=1.0.0",
    "databricks-sdk>=0.20.0,<1.0.0",
    "beautifulsoup4==4.12.3",
    "PyGithub==2.5.0",
    "jwt==1.3.1",
    "pytest-mock==3.14.0",
    "requests<=2.32.4",
    "numpy>=1.23.4,<2.0.0",
    "pandas>=1.5.2,<2.2.0",
    "mkdocs-material==9.5.20",
    "mkdocs-material-extensions==1.3.1",
    "mkdocstrings==0.25.0",
    "mkdocstrings-python==1.10.8",
    "mkdocs-macros-plugin==1.0.1",
]

PYSPARK_PACKAGES = [
    "pyspark>=3.3.0,<3.6.0",
]

EXTRAS_DEPENDENCIES: dict[str, list[str]] = {
    "pyspark": PYSPARK_PACKAGES,
}

setup(
    name="project-fleming",
    url="https://github.com/sede-open/Fleming",
    description="Fleming is a library that helps you to create models using PySpark to run on CPU.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/sede-open/Fleming/issues",
        "Source": "https://github.com/sede-open/Fleming",
    },
    version="0.0.4",
    package_dir={"": "src"},
    include_package_data=True,
    packages=find_packages(where="src"),
    python_requires=">=3.9, <3.12",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_DEPENDENCIES,
)
