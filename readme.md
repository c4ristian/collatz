# Collatz Python Library

## What is it?
The [Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) is an 
unsolved number theory problem. This python library provides tools to 
analyse it from different perspectives. The most important results achieved with this library 
have been published in this [working paper](https://doi.org/10.34646/thn/ohmdok-620).

## Main Features
The library provides four modules:
- [commons](collatz/commons.py) - common methods for creating and analysing Collatz sequences
- [cycles](collatz/cycles.py) - methods to analyse cycles in Collatz sequences
- [generator](collatz/generator.py) - methods to generate Collatz sequences and related features
- [graph](collatz/graph.py) - methods to create and analyse Collatz graphs

The project furthermore provides [jupyter notebooks](notebooks) 
and scripts for data exports.

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
### Pair Notebooks
```sh
jupytext --set-formats ipynb,md notebooks/*.md
```

### Sync Notebooks
```sh
jupytext --sync notebooks/*.md
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
