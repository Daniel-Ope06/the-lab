import PIL
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import imageio.v2 as iio

FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

FRAMES_DIR = FIGURES_DIR / "frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)


def draw_frames(
    positions: np.ndarray,
    labels: list,
    colors: list,
    legend: bool,
    num_frames: int,
    masses: np.ndarray | None = None,
    view_limit: float = 2.0,
    target_body_index: int | None = None,
    visual_scale: float = 1.0,
    hide_grid: bool = False
) -> None:
    print("Drawing frames...")

    # Define Visual Radii (AU)
    # We set base radii and multiply by visual_scale for visibility
    base_radii = np.array([0.05] * len(labels))  # Default 0.05 AU
    if masses is not None:
        # Stars = 0.08 AU, Planets = 0.03 AU (Base size)
        base_radii = np.array([0.08 if m > 0.01 else 0.04 for m in masses])

    # Apply the visual booster
    final_radii_au = base_radii * visual_scale

    # Total width of the graph in AU (e.g., -2 to +2 = 4 AU wide)
    plot_width_au = view_limit * 2.0

    # Calculate Figure Size in Points
    # Matplotlib standard is 72 points per inch.
    fig_size_inches = 10
    fig_width_points = fig_size_inches * 72

    # Factor to convert 1 AU to Points for this specific zoom level
    au_to_points = fig_width_points / plot_width_au

    # Pre-calculate marker sizes (area = radius^2)
    # This ensures they stay consistent throughout the animation
    marker_sizes = (final_radii_au * au_to_points) ** 2

    for n in range(num_frames):
        print(f"Progress: {n + 1} / {num_frames}", end="\r")

        # Draw the trajectory
        fig = plt.figure(figsize=(fig_size_inches, fig_size_inches))
        ax = fig.add_subplot(111, projection="3d")

        if hide_grid:
            # Option A: Clean Cinematic Look (No grid, no numbers)
            ax.grid(False)
            ax.axis('off')
        else:
            # Option B: Stable Engineering Grid
            # Force ticks to be at exact integers (0, 1, 2...)
            # This prevents them from jumping around as the camera moves.
            locator = ticker.MultipleLocator(1.0)
            ax.xaxis.set_major_locator(locator)
            ax.yaxis.set_major_locator(locator)
            ax.zaxis.set_major_locator(locator)

            # Formatting: Force 1 decimal place (e.g. "1.0")
            formatter = ticker.FormatStrFormatter('%.1f')
            ax.xaxis.set_major_formatter(formatter)
            ax.yaxis.set_major_formatter(formatter)
            ax.zaxis.set_major_formatter(formatter)

            ax.set_xlabel("$x$ (AU)")
            ax.set_ylabel("$y$ (AU)")
            ax.set_zlabel("$z$ (AU)")

        # Determine Camera Center
        center_x, center_y, center_z = 0.0, 0.0, 0.0
        if target_body_index is not None:
            # Lock camera onto the specific body's position at this frame 'n'
            center_x = positions[n, target_body_index, 0]
            center_y = positions[n, target_body_index, 1]
            center_z = positions[n, target_body_index, 2]

        for i in range(positions.shape[1]):
            traj = ax.plot(
                positions[:n, i, 0],
                positions[:n, i, 1],
                positions[:n, i, 2],
                color=colors[i],
            )
            # Plot the last position with marker
            ax.scatter(
                positions[n, i, 0],
                positions[n, i, 1],
                positions[n, i, 2],
                marker="o",
                color=traj[0].get_color(),
                label=labels[i],
                s=marker_sizes[i],
                edgecolors='black',
                linewidth=0.5
            )

        # Apply Tracking Limits
        ax.set_xlim3d(center_x - view_limit, center_x + view_limit)
        ax.set_ylim3d(center_y - view_limit, center_y + view_limit)
        ax.set_zlim3d(center_z - view_limit, center_z + view_limit)

        # Set equal aspect ratio to prevent distortion
        ax.set_aspect("equal")

        if legend:
            ax.legend(
                loc="center right", bbox_to_anchor=(0, 0.5))
            fig.subplots_adjust(right=0.7)
            fig.tight_layout()

        plt.savefig(FRAMES_DIR / f"frames_{n:05d}.png", dpi=80)
        plt.close("all")
    print("\nDone!")


def frames_generator(num_frames: int):
    for i in range(num_frames):
        yield PIL.Image.open(  # type: ignore
            FRAMES_DIR / f"frames_{i:05d}.png")


def create_gif(num_frames: int) -> None:
    print("Combining frames to gif...")
    fps = 12
    frames = frames_generator(num_frames)
    next(frames).save(
        FIGURES_DIR / "animation.gif",
        save_all=True,
        append_images=frames,
        loop=0,
        duration=(1000 // fps),
    )

    print(f"Output completed! Please check {FIGURES_DIR / 'animation.gif'}")


def create_mp4(num_frames: int) -> None:
    print("Combining frames to MP4...")
    fps = 12
    output_path = FIGURES_DIR / "animation.mp4"

    with iio.get_writer(
            output_path,
            fps=fps,
            codec='libx264',
            macro_block_size=None
    ) as writer:
        for i in range(num_frames):
            print(f"Processing frame {i+1}/{num_frames}", end="\r")
            filename = FRAMES_DIR / f"frames_{i:05d}.png"
            image = iio.imread(filename)
            writer.append_data(image)  # type: ignore

    print(f"\nOutput completed! Please check {output_path}")


def delete_frames(num_frames: int):
    for i in range(num_frames):
        (FRAMES_DIR / f"frames_{i:05d}.png").unlink()
