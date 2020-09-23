---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"name": "#%% md\n"} -->
## Collatz self contained notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses Collatz sequences that lead to self contained numbers. Self contained
means in this context that an odd Collatz number leads to an even Collatz number that is
a multiple of the odd number. The odd number 31 e.g. results for k= 3 in the even number
310 which equals 10 * 31.
"""

# Imports
from math import log2
from matplotlib import pyplot as plt
import pandas as pd
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 1001
K_FACTOR = 3
MAX_ITERATIONS = 300
ODDS_ONLY = True
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)

nbutils.set_default_pd_options()
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR, max_iterations=MAX_ITERATIONS)

# Drop last row
analysis_frame = analysis_frame[:-1]

# Derive new fields
analysis_frame["n"] = analysis_frame.index + 1

analysis_frame["beta_i"] = 1 + 1 / (K_FACTOR * analysis_frame["collatz"])
analysis_frame["beta"] = analysis_frame["beta_i"].cumprod()

analysis_frame["sigma_i"] = K_FACTOR + (1 / analysis_frame["collatz"])
analysis_frame["sigma"] = analysis_frame["sigma_i"].cumprod()
analysis_frame["sigma"] = analysis_frame["sigma"]
analysis_frame["sigma_natural"] = analysis_frame["sigma"] % 1 == 0

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype('int64')
analysis_frame["alpha_cycle"] = (log2(K_FACTOR) * analysis_frame["n"]).astype('int64') + 1
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

analysis_frame["v_1"] = START_VALUE
analysis_frame["n"] = analysis_frame.index + 1

analysis_frame["multiple"] = analysis_frame["next_odd"] / analysis_frame["v_1"]
analysis_frame["self_contained"] = (analysis_frame["multiple"] % 1 == 0) &  \
                                   (analysis_frame["multiple"] > 1)

# Print results
is_self_contained = analysis_frame["self_contained"].sum() >= 1
is_sigma_natural = (analysis_frame["sigma_natural"]).sum() >= 1

print_frame = analysis_frame[[
    "n", "v_1", "collatz", "next_odd", "multiple",
    "self_contained", "beta_i", "beta",
    "alpha", "sigma", "sigma_natural"]]

print_frame.columns = [
    "n", "v_1", "v_i", "v_i+", "m", "sc", "b_i", "b",
    "a", "s", "s_natural"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " Self contained:", is_self_contained,
      " Sigma natural:", is_sigma_natural,
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
# Plot results
plt.figure()
plt.title("Collatz")
plt.plot(analysis_frame["collatz"], "-")
plt.show()
```
