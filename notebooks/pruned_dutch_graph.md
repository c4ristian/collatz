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
## Pruned dutch graph
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses Collatz sequences from a graph-theoretic perspective.
For this purpose it creates a pruned binary tree as described in
[Pruning the binary tree, proving the Collatz conjecture](https://arxiv.org/abs/2008.13643).
"""

# Imports
from pathlib import Path
from matplotlib import pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import nbutils
from collatz import graph

# Configuration
nbutils.set_default_pd_options()

PRUNING_LEVEL = 3
ITERATION_COUNT = 4
SHOW_LABELS = True

EXPORT_DATA = True
DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "pruned_dutch_graph.png"
CSV_PATH = DATA_PATH + "pruned_dutch_graph.csv"

# Create dutch graph
graph_frame = graph.create_pruned_dutch_graph(
    pruning_level=PRUNING_LEVEL, iteration_count=ITERATION_COUNT)

print("Pruning level:", PRUNING_LEVEL, "\n")
print(graph_frame.to_string(index=False))
```

```python pycharm={"name": "#%%\n"}
# Create graph
plt.figure(figsize=(20, 10))
plt.title("T>=" + str(PRUNING_LEVEL))

network = nx.convert_matrix.from_pandas_edgelist(
    graph_frame, source="predecessor", target="successor",
    create_using=nx.DiGraph())

pos = graphviz_layout(network, prog='dot')
nx.draw(network, pos, with_labels=SHOW_LABELS, arrows=True)

# Export data
if EXPORT_DATA:
    plt.savefig(PIC_PATH)
    graph_frame.to_csv(CSV_PATH, index=False)
    print("Graph saved:" + PIC_PATH)


# Plot graph
plt.show()
```
