# Collatz Python Library

## What is it?
The [Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) is an 
unsolved number theory problem. This Python library provides tools to 
analyse it from different perspectives. The key results of this library have 
been published in different papers [[koch]](https://doi.org/10.34646/thn/ohmdok-620), 
[[sultanow]](https://doi.org/10.25932/publishup-44325).

## Main Features
The library provides four modules:
- [commons](collatz/commons.py) - common methods for creating and analysing Collatz sequences
- [cycles](collatz/cycles.py) - methods to analyse cycles in Collatz sequences
- [generator](collatz/generator.py) - methods to generate Collatz sequences and related features
- [graph](collatz/graph.py) - methods to create and analyse Collatz graphs

The project furthermore offers [jupyter notebooks](notebooks) and scripts for data exports. 
The notebooks are stored as [markdown](https://en.wikipedia.org/wiki/Markdown) files to support efficient 
versioning in git. The synchronisation between markdown files and ipynb files is handled by the framework 
[jupytext](https://github.com/mwouts/jupytext) (for further instructions see below).

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/c4ristian/collatz

## Setup
```sh
conda env create -f environment.yml

conda activate collatz
```

## Run Tests
```sh
pytest
```

## Code Coverage
```sh
pytest --cov
```

## Code Quality
```sh
pylint FILENAME.py
```

## Run script
```sh
python FILENAME.py
```

## Jupyter
### Sync Notebooks
```sh
jupytext --sync notebooks/*.md

jupytext --sync notebooks/*/*.md
```

### Pair Notebook
```sh
jupytext --set-formats ipynb,md notebooks/NOTEBOOK.ipynb
```

### Install Kernel 
```sh
python -m ipykernel install --user --name=collatz
```

### Run Notebooks
```sh
jupyter notebook --notebook-dir="./notebooks"
```

## License
[Apache 2.0](LICENSE.txt)
