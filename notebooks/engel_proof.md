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
## Collatz Engel proof
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook verifies the maximum alpha of a Collatz sequence using
the so called Engel expansion. It builds on a proof that shows that a
worst-case sequence, divided by alpha max leads to a result < 2.
The notebook is optimised for handling arbitrary big integers.
"""

# Imports
from math import log2
import pandas as pd
import nbutils

# Configuration
MAX_VALUE = 10001
MAX_N = 100
K_FACTOR = 3

nbutils.set_default_pd_options()
start_value = nbutils.rnd_int(MAX_VALUE, odds_only=True)

# Generate data
left = []
right = []
valid = []

n = pd.Series(range(1, MAX_N + 1))

for i in n:
    a_max = int((i+1) * log2(K_FACTOR) + log2(start_value)) + 1
    current_left = 2**(a_max+1) + 2**(i+1)
    current_right = K_FACTOR**(i+1) * (start_value + 1)
    current_valid = current_left > current_right
    left.append(current_left)
    right.append(current_right)
    valid.append(current_valid)

analysis_frame = pd.DataFrame({
    "n": n,
    "k": K_FACTOR,
    "v_1": start_value,
    "left": left,
    "right": right,
    "valid": valid
})

# Print results
print_frame = analysis_frame

alpha_max_valid = int((analysis_frame["valid"] == False).sum()) == 0

print("Start value:", start_value,
      " K:", K_FACTOR,
      " Max n:", MAX_N,
      " Valid:", alpha_max_valid,
      "\n")

print(print_frame.to_string(index=False), "\n")
```
