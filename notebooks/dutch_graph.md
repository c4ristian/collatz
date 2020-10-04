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
## Dutch graph
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses Collatz sequences from a graph-theoretic perspective.
For this purpose it creates a reverse binary tree as described in
[Pruning the binary tree, proving the Collatz conjecture](https://arxiv.org/abs/2008.13643).
"""

# Imports
import warnings
from pathlib import Path
from matplotlib import pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import nbutils
from collatz import commons, graph

# Configuration
nbutils.set_default_pd_options()

ROOT_NODE = 1
K_FACTOR = 3
CHILD_COUNT = 4
ITERATION_COUNT = 4
SHOW_LABELS = True

EXPORT_DATA = True
DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "dutch_graph.png"
CSV_PATH = DATA_PATH + "dutch_graph.csv"

# Create dutch graph
graph_frame = graph.create_dutch_graph(
        ROOT_NODE, successor_count=CHILD_COUNT,
        iteration_count=ITERATION_COUNT)

graph_frame["p_binary"] = graph_frame["predecessor"].apply(commons.to_binary)
graph_frame["s_mod_k"] = graph_frame["successor"] % K_FACTOR
graph_frame["alpha_i"] = graph_frame["predecessor"] * K_FACTOR + 1
graph_frame["alpha_i"] = graph_frame["alpha_i"].apply(commons.trailing_zeros)

print("Start value:", ROOT_NODE, " K:", K_FACTOR, "\n")
print(graph_frame.to_string(index=False))
```

```python pycharm={"name": "#%%\n"}
# Create graph
plt.figure(figsize=(20, 10))
plt.title("k=" + str(K_FACTOR))

network = nx.convert_matrix.from_pandas_edgelist(
    graph_frame, source="predecessor", target="successor",
    create_using=nx.DiGraph())

pos = graphviz_layout(network, prog='dot')
nx.draw(network, pos, node_size=200, with_labels=SHOW_LABELS, arrows=True)

# Export data
if EXPORT_DATA:
    plt.savefig(PIC_PATH)
    graph_frame.to_csv(CSV_PATH, index=False)
    print("Graph saved:" + PIC_PATH)


# Plot graph
plt.show()
```
