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
## Collatz siblings notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analysis the siblings of odd nodes in the Collatz graph for
different k factors.
"""

# Imports
from math import log2
import pandas as pd
from notebooks import nbutils
from collatz import graph

# Configuration
K_FACTOR = 3
MAX_VALUE = 101
N_SIBLINGS = 20

NODE = nbutils.rnd_int(MAX_VALUE, odds_only=True)
nbutils.set_default_pd_options()

# Create data
siblings = []

for i in range(0, N_SIBLINGS + 1):
    siblings.append(graph.get_odd_sibling(NODE, i, K_FACTOR, 1000))

analysis_frame = pd.DataFrame({
    "siblings": siblings
})

analysis_frame["log2"] = analysis_frame["siblings"].apply(log2)

# Print results
print("Node:", NODE,
      " K:", K_FACTOR, "\n")

print(analysis_frame.to_string(index=True), "\n")
```
