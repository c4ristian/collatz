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
## Trailing bits machine
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook executes a finite state machine that models the transitions between the trailing three
bits of odd Collatz numbers. The machine is a nondeterministic transducer whose states
represent the bits.
"""

import pandas as pd
import matplotlib.pyplot as plt
import nbutils
from collatz.automata import TrailingBitsMachine

# Configuration
MAX_STATES = 20
PRINT_TABLE = True

nbutils.set_default_pd_options()

# Create data
machine = TrailingBitsMachine()
previous_states = []
current_states = []
omegas = []

n = range(1, MAX_STATES + 1)

for i in n:
    _, omega_i = machine.next_state()
    previous_states.append(machine.previous_state)
    current_states.append(machine.current_state)
    omegas.append(omega_i)

analysis_frame = pd.DataFrame({
    "n": n,
    "previous": previous_states,
    "current": current_states,
    "o_i": omegas
})

analysis_frame["o"] = analysis_frame["o_i"].cumsum()

if PRINT_TABLE:
    print("N:", MAX_STATES, "\n")
    print(analysis_frame.to_string(index=False), "\n")

```

```python pycharm={"name": "#%%\n"}
# Plot results
plt.figure()
plt.title("Omega_i")
plt.hlines(0, 0, len(analysis_frame), colors="red", linestyles="dashed")
plt.plot(analysis_frame["o_i"], "o-")
plt.show()

plt.figure()
plt.title("Omega")
plt.hlines(0, 0, len(analysis_frame), colors="red", linestyles="dashed")
plt.plot(analysis_frame["o"], "o-")
plt.show()
```
