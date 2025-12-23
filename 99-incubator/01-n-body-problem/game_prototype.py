# %%
from level_gen import LevelGenerator
from math_utils import (
    plot_initial_conditions,
    plot_trajectory,
    plot_3d_trajectory
)
# from anim_utils import (
#     draw_frames,
#     create_gif,
#     create_mp4,
#     delete_frames
# )

# %%
generator = LevelGenerator()

TIME_FRAME: float = 3 * 365.24  # years to days
TIME_STEP: float = 0.01
OUTPUT_INTERVAL: float = 0.01 * 365.24

# %%
# system, labels, colors, legend = generator.generate_level("false_stability")
system, labels, colors, legend = generator.generate_level(7)

plot_initial_conditions(
    system=system,
    labels=labels,
    colors=colors,
    legend=legend,
)


# %%
pos_history, vel_history, time_history = system.run(
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
