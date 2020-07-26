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
## Collatz Engel experiments
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook verifies the maximum alpha of a Collatz sequence for k=3 using
the so-called Engel expansion. The notebook is optimised for handling
arbitrary big integers. To avoid float values, which could cause a loss of
precision, integer divisions are used. Where this could lead to an invalidly
low result, one is added to avoid an underestimation of the result.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import pandas as pd
import nbutils

# Configuration
MAX_VALUE = 10001
MAX_N = 50

nbutils.set_default_pd_options()
start_value = nbutils.rnd_int(MAX_VALUE, odds_only=True)

# Generate data
v_i = []
a_max_p = []
next_even = []
next_odd = []
a_max_valid = []

n = pd.Series(range(1, MAX_N + 1))

for i in n:
    # Use integer division here to avoid loss of precision
    current_v_i = (3**i * (start_value + 1) - 2**i) // 2**i
    # Add one to be sure not to underestimate the result
    current_v_i += 1
    v_i.append(current_v_i)

    current_a_max = int(((i+1) * log2(3) + log2(start_value)) + 1)
    a_max_p.append(current_a_max)

    current_next_even = 3 * current_v_i + 1
    next_even.append(current_next_even)

    # Use integer division here to avoid loss of precision
    current_next_odd = current_next_even // 2**(current_a_max - i)
    next_odd.append(current_next_odd)

    a_max_valid.append(current_next_odd <= 1)

analysis_frame = pd.DataFrame({
    "n": n,
    "k": 3,
    "v_1": start_value,
    "v_i": v_i,
    "a": n,
    "a_max+": a_max_p,
    "3v_i+1": next_even,
    "v_i+": next_odd,
    "a_max_valid": a_max_valid
})

# Print results
print_frame = analysis_frame[[
    "n", "k", "v_1",
    "v_i", "3v_i+1",
    "v_i+", "a", "a_max+",
    "a_max_valid"
]]

alpha_max_valid = int((analysis_frame["a_max_valid"] == False).sum()) == 0

print("Start value:", start_value,
      " K:", 3,
      " Max n:", MAX_N,
      " Valid:", alpha_max_valid,
      "\n")

print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
plt.figure()
plt.title("v_i")
plt.plot(analysis_frame["v_i"], "-")

plt.show()
```
