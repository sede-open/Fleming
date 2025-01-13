# Installation Process

## Prerequisite

### Python

There are a few things to note before using the Fleming. The following prerequisites will need to be installed on your local machine.

Python version 3.9 >= and < 3.12 should be installed. Check which python version you have with the following command:

    python --version

Find the latest python version [here](https://www.python.org/downloads/) and ensure your python path is set up correctly on your machine.

### Python Package Installers

Installing Fleming can be done using the package installer [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

### Java

To use Fleming in your own environment that leverages [pyspark](https://spark.apache.org/docs/latest/api/python/getting_started/install.html), Java 8 or later is a [prerequisite](https://spark.apache.org/docs/latest/api/python/getting_started/install.html#dependencies). See below for suggestions to install Java in your development environment.

Follow the official Java JDK installation documentation [here.](https://docs.oracle.com/en/java/javase/11/install/overview-jdk-installation.html)

- [Windows](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html)
- [Mac OS](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-macos.html)
- [Linux](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-linux-platforms.html)

!!! note 
    Windows requires an additional installation of a file called **winutils.exe**. Please see this [repo](https://github.com/steveloughran/winutils) for more information.


## Installation

1) To get started with developing for this project, clone the repository. 
```
    git clone https://github.com/sede-open/Fleming.git
```
2) Open the respository in VS Code, Visual Studio or your preferered code editor.

3) Create a new environment using the following command:
```
    micromamba create -f environment.yml

```

> **_NOTE:_**  You will need to have conda, python and pip installed to use the command above.

4) Activate your newly set up environment using the following command:
```
    micromamba activate fleming
```
You are now ready to start developing your own functions. Please remember to follow Felming's development lifecycle to maintain clarity and efficiency for a fully robust self serving platform. 

5) For better readability of code is would be useful to enable black and isort on autosave by simply adding this to the VSCode user settings json(Ctrl + Shft + P):

```
    {
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "python.formatting.blackArgs": [
            "--line-length=119"
        ],
        "python.sortImports.args": [
            "--profile",
            "black"
        ],
        "[python]": {
            "editor.codeActionsOnSave": {
                "source.organizeImports": true
            }
        }
    }
```
    