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
## Collatz binary experiments
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This experimental notebook analyses randomly generated collatz sequences
from a binary perspective.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import pandas as pd
import nbutils
from collatz import generator as gen
from collatz import commons as com


# Configuration
MAX_VALUE = 101
K_FACTOR = 3
MAX_ITERATIONS = 600
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate Collatz sequence
analysis_frame = gen.generate_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR, max_iterations=MAX_ITERATIONS)

# Derive new fields
analysis_frame["v_1"] = START_VALUE
analysis_frame["bin_str"] = analysis_frame["collatz"].apply(com.to_binary)
analysis_frame["bin_len"] = analysis_frame["bin_str"].apply(len)
analysis_frame["log2_xi"] = analysis_frame["collatz"].apply(log2)

prev_bin_len = list(analysis_frame[:-1]["bin_len"])
prev_bin_len.insert(0, prev_bin_len[0])
analysis_frame["bin_diff"] = analysis_frame["bin_len"] - pd.Series(prev_bin_len)
analysis_frame["tz"] = analysis_frame["collatz"].apply(com.trailing_zeros)
analysis_frame["to"] = analysis_frame["collatz"].apply(com.trailing_ones)

# Print data
print_frame = analysis_frame[[
    "v_1", "collatz", "odd", "bin_len", "bin_str", "log2_xi", "bin_diff", "tz", "to"]]

print_frame.columns = [
    "v_1", "x_i", "odd", "bin_len", "bin_str", "log2_xi", "bin_diff", "tz", "to"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      "Len:", len(analysis_frame),
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
plt.figure()
plt.title("Bin length")
plt.plot(analysis_frame["bin_len"], "-")

plt.figure()
plt.title("Bin diff")
plt.bar(analysis_frame.index, analysis_frame["bin_diff"])

plt.show()
```
