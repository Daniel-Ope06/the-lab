# %% [markdown]
# # N-Body Gravity Prototype
# **Length:** AU (Astronomical Unit)\
# **Mass:** Solar mass\
# **Time:** days

# %%
from math_utils import (get_initial_conditions, plot_initial_conditions)

INITIAL_CONDITION = "solar_system"
system, labels, colors, legend = get_initial_conditions(INITIAL_CONDITION)
plot_initial_conditions(
    system=system,
    labels=labels,
    colors=colors,
    legend=legend,
)

# %%
