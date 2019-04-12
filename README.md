---
services: hdinsight
platforms: python
author: tylerfox
ms.author: tyfox
---

# [HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) Python SDK Samples

This repo provides samples for the [HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) Python SDK.

## Features

Samples showing use of the [HDInsight](https://azure.microsoft.com/en-us/services/hdinsight/) Python SDK.
The idea behind these samples is to showcase 1) how to utilize the HDInsight Python SDK and 2) best practices for handling data associated with these APIs.

## Getting Started

Get more information on HDInsight offerings from [here](https://azure.microsoft.com/en-us/services/hdinsight/).
This should provide you information on various APIs along with their demos and documentation.

### Prerequisites

All samples in this folder require:

- Python, whose latest version can be downloaded from here: <https://www.python.org/downloads/>.
- HDInsight Python SDK. You can get the Python Package from here: <https://pypi.org/project/azure-mgmt-hdinsight/>.

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.4, 3.5, 3.6 and 3.7.

2.  General recommendation for Python development is to use a Virtual Environment.
    For more information, see https://docs.python.org/3/tutorial/venv.html

    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

### Quickstart

1.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/hdinsight-python-sdk-samples.git
    ```

2.  Install the dependencies using pip.

    ```
    cd hdinsight-python-sdk-samples
    pip install -r requirements.txt
    ```

3.  In the samples folder, rename `sample_settings.py.template` to `sample_settings.py` and fill it with the correct information.

## Demo

To run each individual demo, point directly to the file. For example:

- `python samples/create_spark_cluster_sample.py`
- `python samples/create_kafka_cluster_sample.py`

## Resources

- Azure HDInsight Python SDK documentation: <https://docs.microsoft.com/en-us/python/api/overview/azure/hdinsight?view=azure-python>
- HDInsight .NET SDK samples: <https://github.com/Azure-Samples/hdinsight-dotnet-sdk-samples>
- HDInsight Java SDK samples: <https://github.com/Azure-Samples/hdinsight-java-sdk-samples>
- HDInsight Documentation: <https://docs.microsoft.com/en-us/azure/hdinsight/>
