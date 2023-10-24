nagini
==============================

to take down the dark lord once and for fucking all

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── pyproject.toml     <- The requirements file for reproducing the environment
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py

Poetry Installation and Usage
-----------------------------

This uses [poetry](https://poetry.eustace.io/docs/) as the package manager.
You can install it by following the instructions [here](https://poetry.eustace.io/docs/#installation).
I recommend using [pipx](https://pipxproject.github.io/pipx/) to install it, which requires installing pipx:

```
pip install --user pipx
pipx install poetry
```

Poetry uses automatically managed virtual environments.
This template already has a pyproject.toml file so to create such an environment and install the dependencies you just need to run:
```
make requirements
```

You can install new packages with the command:
```
poetry install DEPENDENCY
```
This will record the changes in the pyproject.toml and poetry.lock files, so remember to commit them.

You can run commands directly in the virtual environment without activating it.
This is done by adding the `poetry run` prefix to your command, for example:
```
poetry run python -c 'print("Hello, World!")'
```
Invoking commands in this way means you will not change the virtual environment accidentally.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
<p><small>Refined to use poetry as the package manager</small></p>
