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
## Collatz omega notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses omegas of randomly generated Collatz sequences. Omega is
defined as the difference between the binary growth (lambda) and the divisions by two (alpha)
of a sequence.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import numpy as np
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
LOG_MODE = None
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR)

# Drop last row
analysis_frame = analysis_frame[:-1]

# Derive new fields
analysis_frame["v_1"] = START_VALUE
analysis_frame["n"] = analysis_frame.index + 1
analysis_frame["v_i_log2"] = analysis_frame["collatz"].apply(log2)
analysis_frame["kv_i+1_log2"] = analysis_frame["next_collatz"].apply(log2)
analysis_frame["v_i_log2_frac"] = analysis_frame["v_i_log2"] % 1
analysis_frame["v_i_mod4"] = analysis_frame["collatz"] % 4

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

# Lambda
analysis_frame["bin_len"] = analysis_frame["v_i_log2"].astype('int64') + 1
analysis_frame["next_bin_len"] = analysis_frame["kv_i+1_log2"].astype('int64') + 1

analysis_frame["bin_diff"] = analysis_frame["next_bin_len"] - analysis_frame["bin_len"]
analysis_frame["lambda_i"] = analysis_frame["bin_diff"]
analysis_frame.loc[analysis_frame["lambda_i"] < 0, "lambda_i"] = 0
analysis_frame["lambda"] = analysis_frame["lambda_i"].cumsum()

analysis_frame["lambda_i_min"] = int(log2(K_FACTOR))
analysis_frame["lambda_i_max"] = int(log2(K_FACTOR) + 1)

analysis_frame["lambda_hyp"] = (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["lambda_min"] = analysis_frame["lambda_hyp"].astype('int64')
analysis_frame["lambda_max"] = analysis_frame["lambda_hyp"].astype('int64') + 2

 # Omega
analysis_frame["omega_i"] = analysis_frame["lambda_i"] - analysis_frame["alpha_i"]
analysis_frame["omega"] = analysis_frame["lambda"] - analysis_frame["alpha"]
analysis_frame["omega_i_positive"] = np.where(analysis_frame["omega_i"] > 0, 1, 0)

analysis_frame["omega_i_max"] = analysis_frame["lambda_i_max"] - 1
analysis_frame["omega_max"] = analysis_frame["lambda_max"] - analysis_frame["n"]

max_bin_len = int(analysis_frame["bin_len"].max())
analysis_frame["bin_str"] = analysis_frame["collatz"].apply(com.to_binary).str.zfill(max_bin_len)

analysis_frame["b2"] = analysis_frame["bin_str"].str[max_bin_len-2]
analysis_frame["b3"] = analysis_frame["bin_str"].str[max_bin_len-3]
analysis_frame["b32"] = analysis_frame["b3"].astype('str') + analysis_frame["b2"]

# Validate omega boundaries
o_max_valid = int((analysis_frame["omega_i"] > analysis_frame["omega_i_max"]).sum()) < 1
o_max_valid &= int((analysis_frame["omega"] > analysis_frame["omega_max"]).sum()) < 1

# Calculate means
o_i_mean = round(analysis_frame["omega_i"].mean(), 2)
l_i_mean = round(analysis_frame["lambda_i"].mean(), 2)

# Print results
print_frame = analysis_frame[[
    "n", "collatz", "next_odd", "v_i_log2_frac",
    "lambda_i", "lambda", "lambda_max", "alpha_i", "omega_i", "omega",
    "omega_max", "bin_str", "b3", "b2", "b32"
]]

print_frame.columns = [
    "n", "v_i", "v_i+", "log_frac",
    "l_i", "l", "l_max", "a_i", "o_i", "o",
    "o_max", "bin_str", "b3", "b2", "b32"
]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " Omega max valid:", o_max_valid,
      " o_i:", o_i_mean,
      " l_i:", l_i_mean,
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
#Plot results
# Omega
plt.figure()
plt.title("Omega i")
plt.plot(analysis_frame["omega_i"], "-o")
plt.axhline(y=0, xmin=0.0, xmax=1.0, color="tab:orange")

plt.figure()
plt.title("Omega")
plt.plot(analysis_frame["omega"], "-o")
plt.axhline(y=0, xmin=0.0, xmax=1.0, color="tab:orange")

plt.figure()
plt.title("Log fraction")
plt.plot(analysis_frame["v_i_log2_frac"], "-o")

fraction_line = 1 - (log2(K_FACTOR) % 1)
plt.axhline(y=fraction_line, xmin=0.0, xmax=1.0, color="tab:orange")

plt.figure()
plt.title("Log fraction vs mod 4")
plt.plot(analysis_frame["v_i_log2_frac"], analysis_frame["v_i_mod4"], "-o")

plt.show()
```
