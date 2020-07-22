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

<!-- #region pycharm={"name": "#%% md\n"} -->
## Collatz Engel notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook verifies the maximum alpha of a Collatz sequence using
the so called Engel expansion.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import pandas as pd
import nbutils

# Configuration
MAX_VALUE = 1001
MAX_N = 20
K_FACTOR = 3

nbutils.set_default_pd_options()
start_value = nbutils.rnd_int(MAX_VALUE, odds_only=True)

# Generate data
n = pd.Series(range(1, MAX_N + 1))

analysis_frame = pd.DataFrame({
    "n": n,
    "k": K_FACTOR,
    "v_1": start_value
})

analysis_frame["a"] = n
analysis_frame["a_max+"] = (((n+1) * log2(K_FACTOR) + log2(start_value))+1).astype('int64')
analysis_frame["v_i"] = (K_FACTOR**n * (start_value + 1) - 2**n) / 2**n
analysis_frame["3v_i+1"] = K_FACTOR * analysis_frame["v_i"] + 1
analysis_frame["v_i+"] = analysis_frame["3v_i+1"] / 2**(analysis_frame["a_max+"]-n)
analysis_frame["v_i+_valid"] = (analysis_frame["v_i+"] < 2)

analysis_frame["left"] = 2**(analysis_frame["a_max+"] + 2) + 2**(n+1)
analysis_frame["right"] = 3**(n+1) * (start_value + 1)
analysis_frame["lr_valid"] = (analysis_frame["left"] > analysis_frame["right"])

# Print results
print_frame = analysis_frame[[
    "n", "k", "v_1",
    "v_i", "3v_i+1",
    "v_i+", "a", "a_max+",
    "v_i+_valid", "lr_valid"
]]

vi_invalid = int(not analysis_frame["v_i+_valid"].sum())
lr_invalid = int(not analysis_frame["lr_valid"].sum())
alpha_max_valid = vi_invalid + lr_invalid == 0

print("Start value:", start_value,
      " K:", K_FACTOR,
      " Valid:", alpha_max_valid,
      "\n")

print(print_frame.to_string(index=False), "\n")
```
