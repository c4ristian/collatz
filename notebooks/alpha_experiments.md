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
## Collatz alpha experiments
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses alphas (number of divisions by two)
of randomly generated Collatz sequences.
"""

# Imports
from math import log2
import matplotlib.pyplot as plt
import nbutils
from collatz import generator as gen
from collatz import commons as com

# Configuration
MAX_VALUE = 101
K_FACTOR = 3
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

analysis_frame["alpha_i"] = analysis_frame["next_collatz"].apply(com.trailing_zeros)
analysis_frame["alpha_i"] = analysis_frame["alpha_i"].astype("int64")
analysis_frame["alpha_i_max"] = log2(K_FACTOR) + analysis_frame["collatz"].apply(log2)
analysis_frame["alpha_i_max"] += (1 + 1/(K_FACTOR * analysis_frame["collatz"])).apply(log2)
# Round result here to avoid loss of precision errors
analysis_frame["alpha_i_max"] = analysis_frame["alpha_i_max"].round(9)
analysis_frame["alpha"] = analysis_frame["alpha_i"].cumsum()
analysis_frame["alpha_cycle"] = (log2(K_FACTOR) * analysis_frame["n"]).astype('int64') + 1
analysis_frame["alpha_max"] = \
    log2(START_VALUE) + (analysis_frame["n"] * log2(K_FACTOR))
analysis_frame["alpha_max"] = analysis_frame["alpha_max"].astype('int64') + 1

analysis_frame["bin_str"] = analysis_frame["collatz"].apply(com.to_binary)

# Validate alpha max & alpha pred
final_alpha = analysis_frame["alpha"].max()
final_alpha_max = analysis_frame["alpha_max"].max()

alpha_max_valid = final_alpha == final_alpha_max
alpha_i_max_valid = int((analysis_frame["alpha_i"] <= analysis_frame["alpha_i_max"]).sum())

alphas_valid = alpha_max_valid and alpha_i_max_valid

# Print results
print_frame = analysis_frame[[
    "n", "v_1", "collatz", "next_odd",
    "alpha_i", "alpha_i_max", "alpha", "alpha_cycle",
    "alpha_max", "bin_str"]]

print_frame.columns = [
    "n", "v_1", "v_i", "v_i+",
    "a_i", "a_i_max", "a", "a_cycle", "a_max",
    "bin_str"]

print_frame = print_frame.reset_index(drop=True)

print("Start value:", START_VALUE,
      " K:", K_FACTOR,
      " Alphas valid:", alpha_max_valid, "\n")

if PRINT_TABLE:
    print(print_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
# Plot results
plt.figure()
plt.title("Collatz")
plt.plot(print_frame["v_i"], "o-")


plt.figure()
plt.title("Alpha i")
plt.plot(print_frame["a_i"], "o-")

plt.figure()
plt.title("Alpha i max")
plt.plot(print_frame["a_i_max"], "o-")

plt.figure()
plt.title("Alpha max")
plt.plot(print_frame["a_max"], "o-")

plt.figure()
plt.title("Alpha cycle")
plt.plot(print_frame["a_cycle"], "o-")
plt.show()
```
