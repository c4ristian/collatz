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
## Collatz graph
This notebook analyses Collatz sequences from a graph-theoretic perspective. The script creates a Collatz graph starting with a given root node and plots it. The graph can be created in regular or in reverse order.
<!-- #endregion -->

<!-- #region pycharm={"name": "#%% md\n"} -->
### Configuration
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
# Imports
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
ITERATION_COUNT = 3
REVERSE = False
SHOW_LABELS = True

EXPORT_DATA = True
DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "collatz_graph.png"
CSV_PATH = DATA_PATH + "collatz_graph.csv"
```

<!-- #region pycharm={"name": "#%% md\n"} -->
### Create graph
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
# Create collatz graph
graph_frame = graph.create_collatz_graph(
        ROOT_NODE, k=K_FACTOR, predecessor_count=CHILD_COUNT,
        iteration_count=ITERATION_COUNT)

if REVERSE:
    nbutils.swap_column_names(("successor", "predecessor"), graph_frame)

# Derive additional columns
graph_frame["p_binary"] = graph_frame["predecessor"].apply(commons.to_binary)
graph_frame["s_binary"] = graph_frame["successor"].apply(commons.to_binary)
graph_frame["p_mod_k"] = graph_frame["predecessor"] % K_FACTOR
graph_frame["s_mod_k"] = graph_frame["successor"] % K_FACTOR
graph_frame["alpha_i"] = graph_frame["predecessor"] * K_FACTOR + 1
graph_frame["alpha_i"] = graph_frame["alpha_i"].apply(commons.trailing_zeros)

# Define labels to plot
graph_frame["label"] = graph_frame["predecessor"]

# Print data
print("Start value:", ROOT_NODE, " K:", K_FACTOR, "\n")
print(graph_frame.to_string(index=False))
```

<!-- #region pycharm={"name": "#%% md\n"} -->
### Plot graph
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
# Create graph
plt.figure(figsize=(20, 10))
plt.title("k=" + str(K_FACTOR))

network = nx.convert_matrix.from_pandas_edgelist(
    graph_frame, source="predecessor", target="successor",
    create_using=nx.DiGraph())

pos = graphviz_layout(network, prog='dot')

nx.draw(
    network, pos, node_size=200, node_color="#99ccff",
    with_labels=False, arrows=True)

if SHOW_LABELS:
    labels = dict(zip(graph_frame["predecessor"], graph_frame["label"]))
    nx.draw_networkx_labels(network, pos, labels=labels)

# Export data
if EXPORT_DATA:
    plt.savefig(PIC_PATH)
    graph_frame.to_csv(CSV_PATH, index=False)
    print("Graph saved:" + PIC_PATH)

# Plot graph
plt.show()
```

```python pycharm={"name": "#%%\n"}

```
