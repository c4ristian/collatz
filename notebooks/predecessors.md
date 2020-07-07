---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.1
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"is_executing": false, "name": "#%% md\n"} -->
## Collatz predecessor notebook
<!-- #endregion -->

```python pycharm={"is_executing": false, "name": "#%%\n"}
"""
This notebook analyses the predecessors of numbers in a a collatz sequences for a
specific factor k. The predecessors are determined with the help of an iterative 
process. As a result the predecessors are printed.
"""

# Fix possible import problems
import sys
sys.path.append("..")

import random as rnd
import pandas as pd
from collatz import commons, graph

# Configure the analyser
K_FACTOR = 3
POWER_RANGE = range(1, 51)

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.expand_frame_repr', False)

start_value = rnd.randint(1, 1000)
start_value = start_value if start_value % 2 == 1 else start_value + 1
start_value = 1

# Get the predecessors of the starting value and analyse them
predecessors, alphas = graph.get_odd_predecessors(start_value, K_FACTOR, POWER_RANGE)
analysis_frame = commons.analyse_collatz_basic_attributes(predecessors)

analysis_frame["mod_k"] = analysis_frame["collatz"] % K_FACTOR
analysis_frame["alpha_i"] = alphas

# Print results
start_mod = start_value % K_FACTOR
print("Start Value:", start_value, " K:", K_FACTOR, " mod:", start_mod,"\n")
print(analysis_frame[["collatz", "alpha_i", "mod_k"]])
```
