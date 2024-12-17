# Installation

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
    