---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.2
  kernelspec:
    display_name: collatz
    language: python
    name: collatz
---

<!-- #region pycharm={"name": "#%% md\n"} -->
## Composite bits machine
<!-- #endregion -->

```python pycharm={"name": "#%%\n"}
"""
This notebook executes two finite state machines that model the transitions between the leading and
the trailing three bits of odd Collatz numbers. The machines are a nondeterministic transducers whose
states represent the bits.
"""

import pandas as pd
import nbutils
from collatz.automata import LeadingBitsMachine, TrailingBitsMachine

# Configuration
MAX_STATES = 100
PRINT_TABLE = True

nbutils.set_default_pd_options()

# Create data
leading_machine = LeadingBitsMachine()
previous_leading_states = []
current_leading_states = []
lambdas = []

trailing_machine = TrailingBitsMachine()
previous_trailing_states = []
current_trailing_states = []
omegas = []

n = range(1, MAX_STATES + 1)

for i in n:
    # Leading
    _, lambda_i = leading_machine.next_state()
    previous_leading_states.append(leading_machine.previous_state)
    current_leading_states.append(leading_machine.current_state)
    lambdas.append(lambda_i)

    # Trailing
    _, omega_i = trailing_machine.next_state(lambda_i=lambda_i)
    previous_trailing_states.append(trailing_machine.previous_state)
    current_trailing_states.append(trailing_machine.current_state)
    omegas.append(omega_i)


analysis_frame = pd.DataFrame({
    "n": n,
    "p_leading": previous_leading_states,
    "c_leading": current_leading_states,
    "p_trailing": previous_trailing_states,
    "c_trailing": current_trailing_states,
    "l_i": lambdas,
    "o_i": omegas
})

analysis_frame["a_i"] = (analysis_frame["o_i"] - analysis_frame["l_i"]).abs()
analysis_frame["l"] = analysis_frame["l_i"].cumsum()
analysis_frame["o"] = analysis_frame["o_i"].cumsum()
analysis_frame["a"] = analysis_frame["a_i"].cumsum()

a_i_mean = float(analysis_frame["a_i"].mean())
l_i_mean = float(analysis_frame["l_i"].mean())

if PRINT_TABLE:
    print("N:", MAX_STATES, "Alpha mean:",
          a_i_mean, "Lambda mean:", l_i_mean, "\n")
    print(analysis_frame.to_string(index=False), "\n")
```
