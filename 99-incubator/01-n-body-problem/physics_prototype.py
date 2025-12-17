# %% [markdown]
# # N-Body Gravity Prototype
# **Length:** AU (Astronomical Unit)\
# **Mass:** Solar mass\
# **Time:** days

# %%
from math_utils import (
    get_3_body_problem,
    plot_initial_conditions,
    plot_trajectory,
    plot_3d_trajectory
)

# %%
n_body_system, labels, colors, legend = get_3_body_problem("false_stability")

plot_initial_conditions(
    system=n_body_system,
    labels=labels,
    colors=colors,
    legend=legend,
)

# %%
TIME_FRAME: float = 3 * 365.24  # years to days
TIME_STEP: float = 0.01
OUTPUT_INTERVAL: float = 0.01 * 365.24

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

plot_3d_trajectory(
    sol_x=pos_history,
    labels=labels,
    colors=colors,
    legend=legend
)

# %%
