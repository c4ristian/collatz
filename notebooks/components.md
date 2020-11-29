---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"name": "#%% md\n"} -->
## Collatz components notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses core components of Collatz sequences and their relationship:
a.) k**i
b.) beta_i = 1 + c/(k*v_i)
c.) gamma_i = k + c/v_i
d.) alpha_i

The alphas of the sequence are compared with predicted values for c=1.
"""

# Imports
from math import log2
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
C_SUMMAND = 1
LOG_MODE = None
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR, c=C_SUMMAND)

analysis_frame = analysis_frame[:-1]

# Derive new fields
analysis_frame["v_1"] = START_VALUE
analysis_frame["n"] = analysis_frame.index + 1
analysis_frame["kn_log"] = log2(K_FACTOR) * analysis_frame["n"]
analysis_frame["beta_i"] = 1 + 1 / (K_FACTOR * analysis_frame["collatz"])
analysis_frame["beta"] = analysis_frame["beta_i"].cumprod()

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

analysis_frame["gamma_i"] = K_FACTOR + (C_SUMMAND / analysis_frame["collatz"])
analysis_frame["gamma"] = analysis_frame["gamma_i"].cumprod()

# CAUTION: These predicted values are only valid for c=1
analysis_frame["alpha_cycle"] = (log2(K_FACTOR) * analysis_frame["n"]).astype('int64') + 1
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

# Possible set log mode
if LOG_MODE:
    analysis_frame["v_1"] = analysis_frame["v_1"].apply(LOG_MODE)
    analysis_frame["collatz"] = analysis_frame["collatz"].apply(LOG_MODE)
    analysis_frame["next_odd"] = analysis_frame["next_odd"].apply(LOG_MODE)
    analysis_frame["beta_i"] = analysis_frame["beta_i"].apply(LOG_MODE)
    analysis_frame["beta"] = analysis_frame["beta"].apply(LOG_MODE)
    analysis_frame["gamma_i"] = analysis_frame["gamma_i"].apply(LOG_MODE)
    analysis_frame["gamma"] = analysis_frame["gamma"].apply(LOG_MODE)

# Get max beta
beta_max = analysis_frame["beta"].max()

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz", "next_odd",
    "alpha_i", "alpha", "alpha_cycle", "alpha_max",
    "beta_i", "beta", "gamma_i", "gamma"]]

print_frame.columns = [
    "n", "v_1", "v_i", "v_i+",
    "a_i", "a", "a_cycle", "a_max",
    "b_i", "b", "g_i", "g"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " C:", C_SUMMAND,
      " Beta max: ", round(beta_max, 4),
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")
```
