# Collatz Python Library

## What is it?
The [Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) is an 
unsolved number theoretical problem. This python library provides tools to 
analyse it from different perspectives. The most important results are 
published in this [working paper](https://doi.org/10.25932/publishup-44325).

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

## Coding Guidelines
```sh
pylint FILENAME.py
```

## License
[Apache 2.0](LICENSE.txt)
