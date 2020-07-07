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
This notebook analyses betas of cycles with an experimental formula, based on
the Engel expansion.
"""

# Fix possible import problems
import sys
sys.path.append("..")

# Imports
from math import log2
import matplotlib.pyplot as plt
import pandas as pd


# Configuration
MAX_N = 10
K_FACTOR = 3
START_VALUE = 33

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.expand_frame_repr', False)

# Generate data
n = pd.Series(range(1, MAX_N + 1))

analysis_frame = pd.DataFrame({
    "n": n,
    "k": K_FACTOR,
    "v_1": START_VALUE
})

analysis_frame["alpha"] = \
    (analysis_frame["n"] * log2(K_FACTOR)).astype('int64') + 1

analysis_frame["alpha_max"] = analysis_frame["n"] * log2(K_FACTOR) + log2(START_VALUE)
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

analysis_frame["alpha_1"] = analysis_frame["alpha"] - analysis_frame["n"] + 1

analysis_frame["beta_log_cycle"] = \
    (analysis_frame["n"] * log2(K_FACTOR)).astype('int64') + 1 - \
    analysis_frame["n"] * log2(K_FACTOR)

analysis_frame["beta_cycle"] = 2**analysis_frame["beta_log_cycle"]
analysis_frame["beta_engel"] = \
    (1 + 2**analysis_frame["alpha_1"]) / (K_FACTOR * START_VALUE) - \
    ((2**(analysis_frame["alpha_1"] - 1)) / START_VALUE) * ((2/3)**analysis_frame["n"]) + 1

# Print results
print_frame = analysis_frame[[
    "n", "k","v_1",
    "alpha", "alpha_max", "alpha_1",
    "beta_cycle", "beta_engel"
]]

print_frame.columns = [
    "n", "k","v_1",
    "a", "a_max", "a_1",
    "b_cycle", "b_engel"
]

print("Start value:", START_VALUE, " K:", K_FACTOR,
      "\n")

print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
# Plot results
plt.figure()
plt.title("Beta cycle vs. beta Engel")
plt.plot(analysis_frame["beta_cycle"], "-o", label="beta cycle")
plt.plot(analysis_frame["beta_engel"], "-o", label='beta engel')
plt.legend()

plt.show()
```
