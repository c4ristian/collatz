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
## Collatz graph notebook
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook analyses Collatz sequences from a graph-theoretic perspective. The script
starts with a specific number and calculates its predecessors in a Collatz sequence
using a deterministic algorithm. As a result the constructed tree is plotted.
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
warnings.filterwarnings('ignore')

START_VALUE = 13
K_FACTOR = 3
PREDECESSOR_COUNT = 3
ITERATION_COUNT = 3
SHOW_LABELS = True

EXPORT_DATA = False
DATA_PATH = Path.cwd().parent.as_posix() + "/data/"
PIC_PATH = DATA_PATH + "graph.png"
CSV_PATH = DATA_PATH + "graph.csv"

# Create collatz graph
graph_frame = graph.create_collatz_graph(
    START_VALUE, k=K_FACTOR, predecessor_count=PREDECESSOR_COUNT, 
    iteration_count=ITERATION_COUNT)

graph_frame["p_binary"] = graph_frame["predecessor"].apply(commons.to_binary)
graph_frame["s_mod_k"] = graph_frame["successor"] % K_FACTOR
graph_frame["alpha_i"] = graph_frame["predecessor"] * K_FACTOR + 1
graph_frame["alpha_i"] = graph_frame["alpha_i"].apply(commons.trailing_zeros)

print("Start value:", START_VALUE, " K:", K_FACTOR, "\n")
print(graph_frame.to_string(index=False))
```

```python pycharm={"name": "#%%\n"}
# Create graph
plt.figure(figsize=(20,10))
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
