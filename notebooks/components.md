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
## Collatz components notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses core components of collatz 
sequences and their relationship: 
a.) k**i 
b.) beta_i = 1 + 1/(k*xi)
c.) alpha_i

The alphas of the sequence are compared with a predicted alphas values.
"""

# Fix possible import problems
import sys
sys.path.append("..")

# Imports
import random as rnd
from math import log2
import pandas as pd
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
MAX_ITERATIONS = 100
LOG_MODE = None
PRINT_TABLE = True

START_VALUE = rnd.randint(1, MAX_VALUE)

if START_VALUE % 2 == 0:
    START_VALUE = START_VALUE + 1

# START_VALUE = 13

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.expand_frame_repr', False)

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR, max_iterations=MAX_ITERATIONS)

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
analysis_frame["alpha_cycle"] = (log2(K_FACTOR) * analysis_frame["n"]).astype('int64') + 1
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

analysis_frame["v_i_hyp"] = (analysis_frame["v_1"] * K_FACTOR**analysis_frame["n"])
analysis_frame["v_i_hyp"] = analysis_frame["v_i_hyp"] * analysis_frame["beta"]
analysis_frame["v_i_hyp"] = analysis_frame["v_i_hyp"] / 2**analysis_frame["alpha_max"]

analysis_frame["beta_hyp"] = analysis_frame["alpha_cycle"] - analysis_frame["kn_log"]

analysis_frame["v_i_bin"] = analysis_frame["collatz"].apply(com.to_binary)
analysis_frame["v_i_1_bin"] = analysis_frame["next_odd"].apply(com.to_binary)

analysis_frame["gamma_i"] = 1 / (K_FACTOR * analysis_frame["collatz"])
analysis_frame["gamma"] = analysis_frame["gamma_i"].cumsum()

# Possible set log mode
if LOG_MODE:
    analysis_frame["v_1"] = analysis_frame["v_1"].apply(LOG_MODE)
    analysis_frame["collatz"] = analysis_frame["collatz"].apply(LOG_MODE)
    analysis_frame["next_odd"] = analysis_frame["next_odd"].apply(LOG_MODE)
    analysis_frame["beta_i"]= analysis_frame["beta_i"].apply(LOG_MODE)
    analysis_frame["beta"]= analysis_frame["beta"].apply(LOG_MODE)
    analysis_frame["beta"]= analysis_frame["gamma_i"].apply(LOG_MODE)
    analysis_frame["beta"]= analysis_frame["gamma"].apply(LOG_MODE)
else:
    analysis_frame["beta_hyp"] = 2**analysis_frame["beta_hyp"]

# Validate alpha max & alpha pred
final_alpha = analysis_frame["alpha"].max()
final_alpha_max = analysis_frame["alpha_max"].max()

alpha_max_valid = final_alpha == final_alpha_max

# Get max beta
beta_max = analysis_frame["beta"].max()

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz", "next_odd",
    "alpha_i", "alpha", "alpha_cycle", "alpha_max", 
    "beta_i", "beta", "gamma_i", "gamma"]]

print_frame.columns = [
    "n","v_1", "v_i", "v_i+",
    "a_i", "a", "a_cycle", "a_max", 
    "b_i", "b", "g_i", "g"]

print("Start value:", START_VALUE, 
      " K:", K_FACTOR, 
      " Beta max: ", round(beta_max, 4), " ",
       " Alphas valid:", alpha_max_valid, "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")

```
