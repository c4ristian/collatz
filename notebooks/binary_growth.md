---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.9.1
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

## Collatz binary growth

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses the binary growth of randomly generated Collatz sequences
of the generalised variant *kx+c*.
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

# Binary attributes
analysis_frame["bin"] = analysis_frame["collatz"].apply(com.to_binary)
analysis_frame["next_bin"] = analysis_frame["next_collatz"].apply(com.to_binary)
analysis_frame["next_odd_bin"] = analysis_frame["next_odd"].apply(com.to_binary)

analysis_frame["bin_len"] = analysis_frame["collatz"].apply(log2).astype('int64') + 1
analysis_frame["next_bin_len"] = analysis_frame["next_collatz"].apply(log2).astype('int64') + 1

max_bin_len = int(analysis_frame["bin_len"].max())

analysis_frame["bin_str"] = analysis_frame["bin"].str.zfill(max_bin_len)
analysis_frame["t2"] = analysis_frame["bin_str"].str[max_bin_len-2]
analysis_frame["t3"] = analysis_frame["bin_str"].str[max_bin_len-3]
analysis_frame["t4"] = analysis_frame["bin_str"].str[max_bin_len-4]
analysis_frame["t32"] = analysis_frame["t3"].astype('str') + analysis_frame["t2"]
analysis_frame["t432"] = analysis_frame["t4"].astype('str') + analysis_frame["t32"]
analysis_frame["l23"] = analysis_frame["bin"].str[1:3]

# Lambda
analysis_frame["lambda_i"] = analysis_frame["next_bin_len"] - analysis_frame["bin_len"]
analysis_frame["lambda"] = analysis_frame["lambda_i"].cumsum()
analysis_frame["lambda_max"] = (analysis_frame["n"] * log2(K_FACTOR)).astype('int64') + 2

# Alpha
analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

# Omega
analysis_frame["omega_i"] = analysis_frame["lambda_i"] - analysis_frame["alpha_i"]
analysis_frame["omega"] = analysis_frame["omega_i"].cumsum()

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz","next_odd", "bin", "next_odd_bin", "t32",
    "omega_i", "omega", "l23", "lambda_i", "lambda", "lambda_max", "alpha_i", "alpha"]]

print_frame.columns = [
    "n", "v_1", "v_i","v_i+", "bin", "bin+", "t32",
     "o_i", "o", "l23", "l_i", "l", "l_max", "a_i", "a"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " C:", C_SUMMAND,
      " L/N:", int(analysis_frame["lambda"].max()) / int(analysis_frame["n"].max()),
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
print("Aggregates:", "\n")
aggregated_frame = analysis_frame[analysis_frame.columns]
aggregated_frame["agg_id"] = (aggregated_frame["n"] + 1) // 2

aggregated_frame = aggregated_frame.groupby(
    ["agg_id"], as_index = False).agg(
    count=("n", "count"),
    t32=("t32", "".join), a_i=("alpha_i", "sum"),
    l23=("l23", "".join), l_i=("lambda_i", "sum"),
    o_i=("omega_i", "sum")).reset_index()

aggregated_frame = aggregated_frame[aggregated_frame["count"] > 1]
print(aggregated_frame.to_string(index=False))
```
