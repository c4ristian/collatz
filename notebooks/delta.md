---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"name": "#%% md\n"} -->
## Collatz delta notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses the deltas of Collatz sequences. The parameter delta is defined as follows:
delta = (3**n * v_1) * (beta - 1) where beta = 1 + 1/(3 * v_i).
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
LOG_BASE = 1
PRINT_TABLE = True

START_VALUE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Generate Collatz sequence
analysis_frame = gen.generate_odd_collatz_sequence(
    start_value=START_VALUE, k=K_FACTOR, c=1)

analysis_frame = analysis_frame[:-1]

# Derive new fields
analysis_frame["v_1"] = START_VALUE
analysis_frame["n"] = analysis_frame.index + 1
analysis_frame["kn"] = K_FACTOR ** analysis_frame["n"]
analysis_frame["kn_v_1"] = analysis_frame["kn"] * START_VALUE
analysis_frame["beta_i"] = 1 + 1 / (K_FACTOR * analysis_frame["collatz"])
analysis_frame["beta"] = analysis_frame["beta_i"].cumprod()

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()

analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

analysis_frame["beta_hyp"] = 2**analysis_frame["alpha_max"] / analysis_frame["kn_v_1"]
analysis_frame["v_i+_a"] = analysis_frame["next_odd"] * 2**analysis_frame["alpha"]

analysis_frame["delta"] = analysis_frame["v_i+_a"]- analysis_frame["kn_v_1"]
analysis_frame["delta_hyp"] = \
    (analysis_frame["kn_v_1"] * (analysis_frame["beta_hyp"] - 1)).round(0).astype("int64")

# Cut off numbers that are too big to be processed correctly
analysis_frame = analysis_frame[analysis_frame["beta_hyp"] >= 1]

# Possible set log mode
if LOG_BASE is not None and LOG_BASE > 1:
    analysis_frame["v_1"] = analysis_frame["v_1"].apply(log, args=(LOG_BASE,))
    analysis_frame["collatz"] = analysis_frame["collatz"].apply(log, args=(LOG_BASE,))
    analysis_frame["next_odd"] = analysis_frame["next_odd"].apply(log, args=(LOG_BASE,))
    analysis_frame["kn"] = analysis_frame["n"] * log(K_FACTOR, LOG_BASE)
    analysis_frame["kn_v_1"] = analysis_frame["kn"] + log(START_VALUE, LOG_BASE)
    analysis_frame["delta"] = analysis_frame["kn_v_1"] \
                              + (analysis_frame["beta"] - 1).apply(log, args=(LOG_BASE,))
    analysis_frame["delta_hyp"] = analysis_frame["kn_v_1"] \
                                  + (analysis_frame["beta_hyp"] - 1).apply(log, args=(LOG_BASE,))
    analysis_frame["beta_i"] = analysis_frame["beta_i"].apply(log, args=(LOG_BASE,))
    analysis_frame["beta"] = analysis_frame["beta"].apply(log, args=(LOG_BASE,))
    analysis_frame["alpha_i"] = analysis_frame["alpha_i"] / log2(LOG_BASE)
    analysis_frame["alpha"] = analysis_frame["alpha"] / log2(LOG_BASE)
    analysis_frame["alpha_max"] = analysis_frame["alpha_max"] / log2(LOG_BASE)
    analysis_frame["beta_hyp"] = analysis_frame["alpha_max"] - analysis_frame["kn_v_1"]
    analysis_frame["v_i+_a"] = analysis_frame["next_odd"] + analysis_frame["alpha"]

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz", "next_odd",
    "kn", "kn_v_1", "v_i+_a", "delta", "delta_hyp",
    "beta", "beta_hyp",
    "alpha_i", "alpha", "alpha_max"]]

print_frame.columns = [
    "n", "v_1", "v_i", "v_i+",
    "kn", "kn_v_1", "v_i+_a", "d", "d_hyp",
    "b", "b_hyp",
    "a_i", "a", "a_m"]

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")
```

```python pycharm={"name": "#%%\n"}
#Plot results
plt.figure()
plt.title("Beta vs. Beta hyp")
plt.plot(analysis_frame["beta_hyp"], "-o", label="beta hyp")
plt.plot(analysis_frame["beta"], "-o", label='beta')
plt.legend()

plt.figure()
plt.title("Delta")
plt.plot(analysis_frame["delta"], "-o", label="delta")
plt.plot(analysis_frame["delta_hyp"], "-o", label="delta_hyp")
plt.legend()

plt.show()
```
