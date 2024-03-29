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
## Collatz basics
<!-- #endregion -->

```python
"""
This notebook analyses basic attributes of Collatz sequences and visualises them.
For this purpose, a random Collatz sequence is generated for a predefined k-factor,
summand and a max amount of iterations.
"""

# Imports
import matplotlib.pyplot as plt
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
C_SUMMAND = 1
MAX_ITERATIONS = 300
ODDS_ONLY = False
PRINT_TABLE = False

START_VALUE = nbutils.rnd_int(MAX_VALUE)
nbutils.set_default_pd_options()

# Create a collatz sequence
if ODDS_ONLY:
    analysis_frame = gen.generate_odd_collatz_sequence(
        start_value=START_VALUE, k=K_FACTOR, c=C_SUMMAND,
        max_iterations=MAX_ITERATIONS)
else:
    analysis_frame = gen.generate_collatz_sequence(
        start_value=START_VALUE, k=K_FACTOR, c=C_SUMMAND,
        max_iterations=MAX_ITERATIONS)

# Derive additional fields
next_frame = com.analyse_collatz_basic_attributes(analysis_frame["next_collatz"])
analysis_frame["next_log2"] = next_frame["log2"]
analysis_frame["n_log2_fraction"] = next_frame["log2_fraction"]
analysis_frame["fraction_diff"] = \
    analysis_frame["log2_fraction"] - analysis_frame["n_log2_fraction"]

analysis_frame["mod_k"] = analysis_frame["collatz"] % K_FACTOR
analysis_frame["mod_4"] = analysis_frame["collatz"] % 4

analysis_frame["bin_str"] = analysis_frame["collatz"].apply(com.to_binary)
analysis_frame["bin_len"] = analysis_frame["log2"].astype('int64') + 1

start_value = analysis_frame["collatz"][0]

# Print data
print("Start value:", start_value, " K:", K_FACTOR, " C:", C_SUMMAND, "\n")

if PRINT_TABLE:
    print(analysis_frame[["collatz", "log2", "log2_fraction",
                      "n_log2_fraction", "bin_str", "mod_4"]])
```

```python pycharm={"name": "#%%\n"}
#Plot results
# Collatz
plt.figure()
plt.title("Collatz sequence")
plt.plot(analysis_frame["collatz"])

# log2
plt.figure()
plt.title("Collatz log2")
plt.plot(analysis_frame["log2"])

# bin length
plt.figure()
plt.title("Bin length")
plt.plot(analysis_frame["bin_len"], "-")

# log2 _fraction
plt.figure()
plt.title("Collatz log2 _fraction")
plt.plot(analysis_frame["log2_fraction"], "o-")

# collatz vs next collatz
plt.figure()
plt.title("Collatz vs next collatz")
plt.plot(analysis_frame["collatz"], analysis_frame["next_collatz"], "o-")

# log2 vs next log2
plt.figure()
plt.title("Log2 vs next log2")
plt.plot(analysis_frame["log2"], analysis_frame["next_log2"], "o-")

# log _fraction vs next log _fraction
plt.figure()
plt.title("Log2 _fraction vs next log2 _fraction")
plt.plot(analysis_frame["log2_fraction"], analysis_frame["n_log2_fraction"], "o-")
plt.show()
```
