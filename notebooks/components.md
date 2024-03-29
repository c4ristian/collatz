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
from math import log, log2
import matplotlib.pyplot as plt
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
C_SUMMAND = 5
LOG_BASE = None
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
analysis_frame["beta_i"] = 1 + C_SUMMAND / (K_FACTOR * analysis_frame["collatz"])
analysis_frame["beta"] = analysis_frame["beta_i"].cumprod()

analysis_frame["bin"] = analysis_frame["collatz"].apply(com.to_binary)

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

analysis_frame["sigma_i"] = K_FACTOR + (C_SUMMAND / analysis_frame["collatz"])
analysis_frame["sigma"] = analysis_frame["sigma_i"].cumprod()

# CAUTION: These predicted values are only valid for c=1
analysis_frame["alpha_cycle"] = (log2(K_FACTOR) * analysis_frame["n"]).astype('int64') + 1
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

# Possible set log mode
if LOG_BASE is not None and LOG_BASE > 1:
    analysis_frame["v_1"] = analysis_frame["v_1"].apply(log, args=(LOG_BASE,))
    analysis_frame["collatz"] = analysis_frame["collatz"].apply(log, args=(LOG_BASE,))
    analysis_frame["next_odd"] = analysis_frame["next_odd"].apply(log, args=(LOG_BASE,))
    analysis_frame["beta_i"] = analysis_frame["beta_i"].apply(log, args=(LOG_BASE,))
    analysis_frame["beta"] = analysis_frame["beta"].apply(log, args=(LOG_BASE,))
    analysis_frame["sigma_i"] = analysis_frame["sigma_i"].apply(log, args=(LOG_BASE,))
    analysis_frame["sigma"] = analysis_frame["sigma"].apply(log, args=(LOG_BASE,))

    analysis_frame["alpha_i"] = analysis_frame["alpha_i"] / log2(LOG_BASE)
    analysis_frame["alpha"] = analysis_frame["alpha"] / log2(LOG_BASE)
    analysis_frame["alpha_cycle"] = analysis_frame["alpha_cycle"] / log2(LOG_BASE)
    analysis_frame["alpha_max"] = analysis_frame["alpha_max"] / log2(LOG_BASE)

# Get max beta
beta_max = analysis_frame["beta"].max()

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz", "bin", "next_odd",
    "alpha_i", "alpha", "alpha_cycle", "alpha_max",
    "beta_i", "beta", "sigma_i", "sigma"]]

print_frame.columns = [
    "n", "v_1", "v_i", "bin", "v_i+",
    "a_i", "a", "a_c", "a_m",
    "b_i", "b", "s_i", "s"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " C:", C_SUMMAND,
      " Beta max: ", round(beta_max, 4),
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
#Plot results
# Decimal
plt.figure()
plt.title("Sigma")
plt.plot(analysis_frame["sigma"], "-o")
plt.show()
```
