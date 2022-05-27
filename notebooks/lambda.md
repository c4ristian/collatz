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
## Collatz lambda notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses the binary growth of a Collatz sequence, called Lambda,
for a predefined k-factor, summand and a maximum amount of iterations.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import pandas as pd
import nbutils
from collatz import commons

# Configuration
MAX_VALUE = 1001
K_FACTOR = 3
C_SUMMAND = 1
MAX_ITERATIONS = 1000
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate collatz components
analysis_frame = commons.odd_collatz_sequence_components(
    START_VALUE, k=K_FACTOR, c=C_SUMMAND, max_iterations=MAX_ITERATIONS)

# Derive new fields
analysis_frame["k**n_log2"] = log2(K_FACTOR) * analysis_frame["n"]
analysis_frame["alpha_i"] = analysis_frame["decimal"].apply(commons.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype('int64')
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

analysis_frame["log2"] = analysis_frame["decimal"].apply(log2)
analysis_frame["log2_frac"] = 2**(analysis_frame["log2"] % 1)
analysis_frame["bin_str"] = analysis_frame["decimal"].apply(commons.to_binary)
analysis_frame["bin_len"] = analysis_frame["log2"].astype('int64') + 1
analysis_frame["lambda_hyp"] = (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["lambda_max"] = analysis_frame["lambda_hyp"].astype('int64') + 2

prev_bin_len = list(analysis_frame[:-1]["bin_len"])
prev_bin_len.insert(0, prev_bin_len[0])
analysis_frame["bin_diff"] = analysis_frame["bin_len"] - pd.Series(prev_bin_len)

analysis_frame["lambda_i"] = analysis_frame["bin_diff"]
analysis_frame.loc[analysis_frame["lambda_i"] < 0, "lambda_i"] = 0
analysis_frame["lambda"] = analysis_frame["lambda_i"].cumsum()

next_decimal = list(analysis_frame[1:]["decimal"])
next_decimal.append(0)
analysis_frame["next_decimal"] = next_decimal

# Remove final result
analysis_frame = analysis_frame[:-1]

# Validate lambda
l_max_valid = int((analysis_frame["lambda"] > analysis_frame["lambda_max"]).sum()) < 1

# Print results
print_frame = analysis_frame[[
    "n", "variable", "decimal", "next_decimal",
    "log2", "log2_frac", "k**n_log2", "bin_str", "bin_len",
    "lambda_i", "lambda", "lambda_max",
    "alpha", "alpha_max"
]]

print_frame.columns = [
    "n", "var", "dec", "next",
    "log2", "log2_frac", "k**n_log2", "b_str", "b_len",
    "l_i", "l", "l_max",
    "a", "a_max"
]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " C:", C_SUMMAND,
      " n:", int(analysis_frame["n"].max()),
      " Lambda max valid:", l_max_valid,
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
#Plot results
# Decimal
plt.figure()
plt.title("Decimal")
plt.plot(analysis_frame["decimal"], "-")

# Bin len
plt.figure()
plt.title("Bin length")
plt.plot(analysis_frame["bin_len"], "-")

plt.figure()
plt.title("Lambda max")
plt.plot(analysis_frame["lambda_max"], "-")

plt.figure()
plt.title("Alpha")
plt.plot(analysis_frame["alpha"], "-")

plt.figure()
plt.title("Lambda Max vs Lambda")
plt.plot(analysis_frame["lambda_max"], label="lambda max")
plt.plot(analysis_frame["lambda"], label="lambda")
plt.legend()

plt.figure()
plt.title("Lambda Max vs Alpha")
plt.plot(analysis_frame["lambda_max"], label="lambda max")
plt.plot(analysis_frame["alpha"], label="alpha")
plt.legend()

plt.show()
```
