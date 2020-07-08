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

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses the predecessors of numbers in a a collatz sequences for a
specific factor k. The predecessors are determined with the help of an iterative 
process. As a result the predecessors are printed.
"""

# Imports
import nbutils
from collatz import commons, graph

# Configure the analyser
K_FACTOR = 3
POWER_RANGE = range(1, 51)
START_VALUE = 1

nbutils.set_default_pd_options()

# Get the predecessors of the starting value and analyse them
predecessors, alphas = graph.get_odd_predecessors(START_VALUE, K_FACTOR, POWER_RANGE)
analysis_frame = commons.analyse_collatz_basic_attributes(predecessors)

analysis_frame["mod_k"] = analysis_frame["collatz"] % K_FACTOR
analysis_frame["alpha_i"] = alphas

# Print results
start_mod = START_VALUE % K_FACTOR
print("Start Value:", START_VALUE, " K:", K_FACTOR, " mod:", start_mod,"\n")
print(analysis_frame[["collatz", "alpha_i", "mod_k"]])
```
