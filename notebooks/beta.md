---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.8
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"name": "#%% md\n"} -->
## Collatz beta notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses the betas of collatz sequences and their relationship
to other components.
"""

# Imports
from math import log2
from fractions import Fraction
import matplotlib.pyplot as plt
import nbutils
from collatz import commons as com
from collatz import generator as gen

# Configuration
K_FACTOR = 3
MAX_VALUE = 101

start_value = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=start_value, k=K_FACTOR)

# Drop last row
analysis_frame = analysis_frame[:-1]

# Derive additional fields
analysis_frame["n"] = analysis_frame.index + 1
analysis_frame.insert(1, "v_1", [start_value] * len(analysis_frame))

# Calculate alpha
analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()
analysis_frame["alpha_max"] = analysis_frame["n"] * log2(K_FACTOR) + log2(start_value)
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1
analysis_frame["alpha_cycle"] = (analysis_frame["n"] * log2(K_FACTOR)).astype('int64') + 1

# Calculate beta
analysis_frame["beta_i"] = 1 + 1/(K_FACTOR * analysis_frame["collatz"])
analysis_frame["beta"] = analysis_frame["beta_i"].cumprod()
analysis_frame["beta_log"] = analysis_frame["beta"].apply(log2)
analysis_frame["beta_log_max"] = analysis_frame["alpha_max"] - \
                             analysis_frame["n"] * log2(K_FACTOR) - log2(start_value)

analysis_frame["beta_log_cycle"] = (analysis_frame["n"] * log2(K_FACTOR)).astype('int64') + 1 - \
                                   analysis_frame["n"] * log2(K_FACTOR)

analysis_frame["beta_max"] = 2**analysis_frame["beta_log_max"]
analysis_frame["beta_cycle"] = 2**analysis_frame["beta_log_cycle"]

analysis_frame["beta_frac"] = analysis_frame["beta"].apply(
    Fraction.from_float).apply(Fraction.limit_denominator)

analysis_frame["beta_max_frac"] = analysis_frame["beta_max"].apply(
    Fraction.from_float).apply(Fraction.limit_denominator)

analysis_frame["beta_cycle_frac"] = analysis_frame["beta_cycle"].apply(
    Fraction.from_float).apply(Fraction.limit_denominator)

analysis_frame["bin_str"] = analysis_frame["collatz"].apply(com.to_binary)

# Print results
print_frame = analysis_frame[[
    "n", "collatz", "next_odd",
    "beta", "beta_cycle", "beta_max",
    "alpha", "alpha_cycle", "alpha_max",
    "bin_str"]]

print_frame.columns = ["n", "v_i", "v_i+",
                       "b", "b_cycle", "b_max",
                       "a", "a_cycle", "a_max",
                       "bin_str"]

final_beta = analysis_frame["beta"][len(analysis_frame)-1]

print("Start value:", start_value, " K:", K_FACTOR,
      " Final beta:", final_beta,
      "\n")

print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
# Plot results
plt.figure()
plt.title("Log beta vs. beta max")
plt.plot(analysis_frame["beta_log_max"], "-o", label="log beta max")
plt.plot(analysis_frame["beta_log"], "-o", label='log beta')
plt.legend()

plt.figure()
plt.title("Log beta vs. beta cycle")
plt.plot(analysis_frame["beta_log_cycle"], "-o", label="log beta cycle")
plt.plot(analysis_frame["beta_log"], "-o", label='log beta')
plt.legend()
plt.show()
```
