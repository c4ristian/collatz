# Collatz Python Library

## What is it?
The [Collatz conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) is an 
unsolved number theoretical problem. This python library provides tools to 
analyse it from different perspectives.

## Main Features
The library provides four modules:
- commons: common methods for creating and analysing Collatz sequences
- cycles:  methods to analyse cycles in Collatz sequences
- generator:  methods that generate Collatz sequences and analyse their results
- graph: methods that can be used to generate and analyse Collatz graphs

The project furthermore provides jupyter notebooks and scripts for data generation.

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


