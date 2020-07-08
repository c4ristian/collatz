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
## Collatz cycle notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses hypothetical cycles in collatz sequences and their corresponding features.
"""

# Imports
from math import log2
from fractions import Fraction
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nbutils
from collatz import commons


# Helper functions
def _calculate_max_beta(k:int, max_iterations:int):
    """
    This function calculates the (hypothetical) maximum beta of a Collatz
    sequence for a specific k factor.
    :param k: The k factor.
    :param max_iterations: Maximum number of iterations.
    :return: The maximum beta
    """
    collatz = pd.Series(commons.odd_collatz_sequence(1, k, max_iterations))
    collatz = collatz[:-1]
    beta_i = 1 + 1/(k * collatz)
    beta = beta_i.product()
    return float(beta)


# Configuration
MAX_N = 20
K_FACTOR = 3
MAX_ITERATIONS = 300

nbutils.set_default_pd_options()

# Generate data
n = pd.Series(range(1, MAX_N + 1))
alpha_cycle = (n * log2(K_FACTOR)).astype('int64') + 1

analysis_frame = pd.DataFrame({
    "n": n,
    "alpha_cycle": alpha_cycle
})

analysis_frame["beta_cycle"] = 2**(analysis_frame["alpha_cycle"] - (n * log2(K_FACTOR)))
analysis_frame["beta_cycle_frac"] = analysis_frame["beta_cycle"].apply(
    Fraction.from_float).apply(Fraction.limit_denominator)

beta_max = _calculate_max_beta(K_FACTOR, MAX_ITERATIONS)
analysis_frame["beta_max"] = beta_max
analysis_frame["beta_possible"] = \
    analysis_frame["beta_cycle"].round(5) <= analysis_frame["beta_max"].round(5)

# Print results
print_frame = analysis_frame[[
    "n", "alpha_cycle", "beta_cycle", "beta_max",
    "beta_possible", "beta_cycle_frac",
]]

print_frame.columns = [
    "n","a_cycle", "b_cycle", "b_max",
    "b_possible", "b_frac"
]

print("K:", K_FACTOR,
      "\n")

print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
# Plot results
beta_colors = np.where(analysis_frame["beta_possible"] == True, 'b', 'r')

plt.figure()
plt.title("Beta cycle")
plt.plot(analysis_frame["n"], analysis_frame["beta_cycle"], "-o")
plt.axhline(beta_max, c="red")


plt.figure()
plt.title("Beta cycle")
plt.scatter(analysis_frame["n"], analysis_frame["beta_cycle"], c=beta_colors)

plt.show()
```
