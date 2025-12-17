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

from anim_utils import (
    draw_frames,
    create_gif,
    create_mp4,
    delete_frames
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

num_frames = len(time_history)

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
# God's eye view
draw_frames(
    positions=pos_history,
    labels=labels,
    colors=colors,
    legend=legend,
    num_frames=num_frames,
    masses=n_body_system.masses,
    view_limit=4.0,       # Zoom out to see everything
    visual_scale=1.5
)

# %%
# Following Sun C
draw_frames(
    positions=pos_history,
    labels=labels,
    colors=colors,
    legend=legend,
    num_frames=num_frames,
    masses=n_body_system.masses,
    view_limit=1.0,
    target_body_index=2,  # Track Sun C
    visual_scale=1.5,
    hide_grid=True
)

# %%
create_gif(num_frames)

# %%
create_mp4(num_frames)

# %%
delete_frames(num_frames)

# %%
