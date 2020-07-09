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
## Collatz analysis notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook uses techniques of mathematical analysis to investigate a function
that predicts the alpha (power of two) for a cycle with a specific length
for a certain k-factor.
"""

# Imports
from pathlib import Path
from math import log2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nbutils
from collatz import cycles


# Helper functions
def _predict_cycle_alpha(k_factor, cycle_lengths):
    result_list = []
    for i in cycle_lengths:
        result_list.append(cycles.predict_cycle_alpha(k_factor, i))
    return result_list


# Configuration
K_FACTOR = 3
MAX_VALUE = 15

EXPORT_DATA = True
DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "analysis.png"
CSV_PATH = DATA_PATH + "analysis.csv"

nbutils.set_default_pd_options()

# Analyse the data
FIRST_FRACTION = 1
fractions = np.array(range(FIRST_FRACTION, FIRST_FRACTION + 2 * MAX_VALUE, 2))
fractions = K_FACTOR + 1/fractions

analysis_frame = pd.DataFrame({"n": range(1, MAX_VALUE+1)})
analysis_frame['alpha_cycle'] = _predict_cycle_alpha(K_FACTOR, analysis_frame['n'])
analysis_frame['2_alpha_cycle'] = 2 ** analysis_frame['alpha_cycle']

analysis_frame['cycle_min'] = K_FACTOR ** analysis_frame['n']
analysis_frame['cycle_min_log2'] = analysis_frame['cycle_min'].apply(log2)

analysis_frame['cycle_max'] = fractions.cumprod()
analysis_frame['cycle_max_log2'] = analysis_frame['cycle_max'].apply(log2)

analysis_frame['cycle_possible'] = \
    analysis_frame['alpha_cycle'] >= analysis_frame['cycle_min_log2']

analysis_frame['cycle_possible'] &= \
    analysis_frame['alpha_cycle'] <= analysis_frame['cycle_max_log2']

# Print results
print("K:", K_FACTOR, "\n")

print_frame = analysis_frame[[
    'n', 'alpha_cycle', 'cycle_min_log2', "cycle_max_log2", "cycle_possible"]]

print(print_frame.to_string(index=False))
```

```python pycharm={"name": "#%%\n"}
# Plot results

# Predicted alpha vs cycle min and max
plt.figure()
plt.title("Alpha cycle " + "k=" + str(K_FACTOR))
plt.plot(analysis_frame["alpha_cycle"], label='alpha cycle')
plt.plot(analysis_frame["cycle_min_log2"], label="cycle min (log2)")
plt.plot(analysis_frame["cycle_max_log2"], label="cycle max (log2)")
plt.legend()

# Export results
if EXPORT_DATA:
    plt.savefig(PIC_PATH)
    print_frame.to_csv(CSV_PATH, index=False)

plt.show()
```
