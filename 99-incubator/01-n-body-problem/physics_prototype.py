# %% [markdown]
# # N-Body Gravity Prototype
# **Length:** AU (Astronomical Unit)\
# **Mass:** Solar mass\
# **Time:** days

# %%
from math_utils import (
    get_initial_conditions,
    plot_initial_conditions,
    plot_trajectory
)

# %%
INITIAL_CONDITION: str = "solar_system"
n_body_system, labels, colors, legend = get_initial_conditions(
    INITIAL_CONDITION)
plot_initial_conditions(
    system=n_body_system,
    labels=labels,
    colors=colors,
    legend=legend,
)

# %%
TIME_FRAME: float = 200.0 * 365.24  # 200 years to days
TIME_STEP: float = 1.0
OUTPUT_INTERVAL: float = 0.1 * 365.24

# Launch Simulation
pos_history, vel_history, time_history = n_body_system.run(
    time_frame=TIME_FRAME,
    time_step=TIME_STEP,
    output_interval=OUTPUT_INTERVAL
)

# %%
plot_trajectory(
    sol_x=pos_history,
    labels=labels,
    colors=colors,
    legend=legend
)

# %%
