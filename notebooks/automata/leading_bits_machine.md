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
## Leading bits machine
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook executes a finite state machine that models the transitions between the leading three
bits of odd Collatz numbers. The machine is a nondeterministic transducer whose states
represent the bits.
"""

from math import log2
import pandas as pd
import nbutils
from collatz.automata import LeadingBitsMachine

# Configuration
MAX_STATES = 20
PRINT_TABLE = True

nbutils.set_default_pd_options()

# Create data
machine = LeadingBitsMachine()
previous_states = []
current_states = []
lambdas = []

n = range(1, MAX_STATES + 1)

for i in n:
    _, lambda_i = machine.next_state()
    previous_states.append(machine.previous_state)
    current_states.append(machine.current_state)
    lambdas.append(lambda_i)

analysis_frame = pd.DataFrame({
    "n": n,
    "previous": previous_states,
    "current": current_states,
    "l_i": lambdas
})

analysis_frame["l"] = analysis_frame["l_i"].cumsum()
analysis_frame["l_cycle"] = (analysis_frame["n"] * log2(3)).astype('int64') + 1
analysis_frame["l_max"] = (analysis_frame["n"] * log2(3)).astype('int64') + 2
analysis_frame["l_valid"] = analysis_frame["l"] <= analysis_frame["l_max"]

l_max_valid = int((analysis_frame["l_valid"] == False).sum()) == 0

print("N:", MAX_STATES, " Lambda max valid:", l_max_valid, "\n")

if PRINT_TABLE:
    print(analysis_frame.to_string(index=False), "\n")
```
