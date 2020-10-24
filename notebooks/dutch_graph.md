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
## Dutch graph
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook creates a pruned binary tree as described in
*Pruning the binary tree, proving the Collatz conjecture* (https://arxiv.org/abs/2008.13643).
"""

# Imports
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import nbutils
from collatz import graph

# Configuration
nbutils.set_default_pd_options()

PRUNING_LEVEL = 0
ITERATION_COUNT = 4
REVERSE = False
SHOW_LABELS = True
SHOW_ARROWS = False
PLOT_SIZE = (20, 10)
PRINT_TABLE = True
EXPORT_DATA = True

DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "dutch_graph.png"
CSV_PATH = DATA_PATH + "dutch_graph.csv"

# Create graph
graph_frame = graph.create_pruned_dutch_graph(
    pruning_level=PRUNING_LEVEL, iteration_count=ITERATION_COUNT)

graph_frame["prunable"] = graph_frame.index % 2 == 1

if REVERSE:
    nbutils.swap_column_names(("successor", "predecessor"), graph_frame)

print("T>=" + str(PRUNING_LEVEL), "\n")

if PRINT_TABLE:
    print(graph_frame.to_string(index=False))
```

```python pycharm={"name": "#%%\n"}
# Plot graph
plt.figure(figsize=PLOT_SIZE)
plt.title("T>=" + str(PRUNING_LEVEL))

network = nx.convert_matrix.from_pandas_edgelist(
    graph_frame, source="predecessor", target="successor",
    create_using=nx.DiGraph())

pos = graphviz_layout(network, prog='dot')
node_color = np.where(graph_frame["prunable"], "#f5b3cc", "#80f1b9")

nx.draw(
    network, pos, with_labels=SHOW_LABELS,
    arrows=SHOW_ARROWS, node_color=node_color)

# Export data
if EXPORT_DATA:
    plt.savefig(PIC_PATH)
    graph_frame.to_csv(CSV_PATH, index=False)
    print("Graph saved:" + PIC_PATH)

# Show graph
plt.show()
```
