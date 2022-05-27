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
## Collatz cycle validation
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses cycles in Collatz sequences for the generalised
variant *kn+c*.

The cycle data are stored in the CSV-file *data/cycles_c_31.csv*.
The file can be created using the following command:

>>> python run_cycle_finder.py --k 201 --c 31 --v 1001 --f "data/cycles_c_31.csv"
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import nbutils

# Configuration
DATA_PATH = "../data/"
INPUT_PATH = DATA_PATH + "cycles_c_31.csv"

nbutils.set_default_pd_options()

# Read CSV file
print("Reading file from ", INPUT_PATH, "\n")

analysis_frame = pd.read_csv(INPUT_PATH)
print(analysis_frame.head().to_string(index=False))
```

### Analyse k

```python pycharm={"name": "#%%\n"}
# Analyse k

k_frame = analysis_frame.groupby('k').agg(
    Count=('c', 'count'), Max_Length=('length', 'max'),
    Mean_Length=('length', 'mean')).round(2)

print(k_frame.to_string(), "\n")
```

```python pycharm={"name": "#%%\n"}
# Plot k

plt.figure()
plt.title("Counts by k")
plt.bar(k_frame.index, k_frame["Count"])
plt.show()

plt.figure()
plt.title("Max length by k")
plt.bar(k_frame.index, k_frame["Max_Length"])
plt.show()
```

### Analyse c

```python pycharm={"name": "#%%\n"}
c_frame = analysis_frame.groupby('c').agg(
    Count=('c', 'count'), Max_Length=('length', 'max'),
    Mean_Length=('length', 'mean')).round(2)

print(c_frame.to_string(), "\n")
```

```python pycharm={"name": "#%%\n"}
# Plot c

plt.figure()
plt.title("Counts by c")
plt.bar(c_frame.index, c_frame["Count"])
plt.show()

plt.figure()
plt.title("Max length by c")
plt.bar(c_frame.index, c_frame["Max_Length"])
plt.show()


```

### Analyse k,c

```python pycharm={"name": "#%%\n"}
kc_frame = analysis_frame.groupby(['k', 'c']).agg(
    Count=('c', 'count'), Max_Length=('length', 'max'),
    Mean_Length=('length', 'mean')).round(2)

print(kc_frame.to_string())
```
