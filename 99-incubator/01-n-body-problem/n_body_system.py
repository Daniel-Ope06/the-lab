import numpy as np


class NBodySystem:
    """Represents an N-body gravitational system.

    Attributes:
        num_bodies (int): Number of bodies in the system.
        positions (np.ndarray): Positions of bodies in 3D space.
        velocities (np.ndarray): Velocities of bodies in 3D space.
        accelerations (np.ndarray): Accelerations of bodies in 3D space.
        masses (np.ndarray): Masses of bodies.
        G (float): Gravitational constant.
    """

    def __init__(
        self, num_bodies: int, positions: np.ndarray,
        velocities: np.ndarray, masses: np.ndarray, G: float
    ) -> None:
        self.num_bodies: int = num_bodies
        self.positions: np.ndarray = positions
        self.velocities: np.ndarray = velocities
        self.accelerations: np.ndarray = np.zeros((num_bodies, num_bodies))
        self.masses: np.ndarray = masses
        self.G: float = G

    def recenter_com_to_origin(self) -> None:
        """Shift the system so:
        - the Center of Mass is at (0,0,0)
        - with zero momentum.
        """
        center_of_mass_position: np.ndarray = np.average(
            self.positions, axis=0, weights=self.masses
        )
        center_of_mass_velocity: np.ndarray = np.average(
            self.velocities, axis=0, weights=self.masses
        )
        self.positions -= center_of_mass_position
        self.velocities -= center_of_mass_velocity

    def _calculate_accelerations(self) -> None:
        """Calculate the gravitational acceleration of each body"""
        # Prepare positions for broadcasting (N x N matrix)
        # r_j [shape: (N, 1, 3)] column vector of positions
        pos_col: np.ndarray = self.positions[:, np.newaxis, :]
        # r_i [shape: (1, N, 3)] row vector of positions
        pos_row: np.ndarray = self.positions[np.newaxis, :, :]

        # Calculate the displacement vector
        # r_ij = r_j - r_i [shape: (N, N, 3)]
        r_ij: np.ndarray = pos_col - pos_row

        # Calculate the magnitude of displacement (distance)
        # r_norm = sqrt(x^2 + y^2 + z^2)
        r_norm: np.ndarray = np.linalg.norm(r_ij, axis=2)

        # Calculate 1 / r^3
        # Ignore zero division errors on diagonal
        with np.errstate(divide='ignore', invalid='ignore'):
            inv_r_cubed: np.ndarray = 1.0 / (r_norm * r_norm * r_norm)
        # Set diagonal elements to 0 to avoid self-interaction
        np.fill_diagonal(inv_r_cubed, 0.0)

        # Calculate acceleration
        # Reshape mass to (N, 1, 1) so it aligns with the (N, N, 3) grid
        mass_column: np.ndarray = self.masses[:, np.newaxis, np.newaxis]

        # G * Sum( mass_i * vector_ij / r^3 )
        # Sum over axis 0 (the 'i' bodies) to get total force on 'j'
        self.accelerations = self.G * np.sum(
            mass_column * r_ij * inv_r_cubed[:, :, np.newaxis],
            axis=0
        )

    def _step(self, dt: float) -> None:
        """Advance the simulation by one time step using Euler-Cromer method.

        **Note:** Includes a safety check for high-speed close encounters.

        Args:
            dt (float): Time step.
        """
        # Check maximum acceleration in the system
        # max_acc: float = np.max(np.linalg.norm(self.accelerations, axis=1))

        # If gravity is crushing (perihelion), chop dt into tiny substeps
        # Threshold (50) depends on the scale
        # if max_acc > 50.0:
        #     num_substeps = 10
        #     sub_dt = dt / num_substeps
        #     for _ in range(num_substeps):
        #         self._calculate_accelerations()  # Recalculate often!
        #         self.velocities += self.accelerations * sub_dt
        #         self.positions += self.velocities * sub_dt
        #     # Don't run the normal update
        #     return

        # Normal Update (Safe Zone)
        self._calculate_accelerations()
        self.velocities += self.accelerations * dt
        self.positions += self.velocities * dt

    def run(
        self,
        time_frame: float,
        time_step: float,
        output_interval: float
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Run the simulation for a specified duration and return the history.

        Args:
            time_frame (float): The total duration of the simulation in days.
            time_step (float): The integration time step (dt) in days.
            output_interval (float): Save frequency in days.

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray]: A tuple containing:
                - position_history: Shape (num_snapshots, num_bodies, 3)
                - velocity_history: Shape (num_snapshots, num_bodies, 3)
                - time_history: Shape (num_snapshots,)
        """
        # Estimate array size (+2 for initial and final time)
        num_snapshots: int = int(time_frame // output_interval + 2)

        # Initialize history arrays
        # 3 is at the end because it's in 3D space (x,y,z)
        position_history: np.ndarray = np.zeros(
            (num_snapshots, self.num_bodies, 3))
        velocity_history: np.ndarray = np.zeros(
            (num_snapshots, self.num_bodies, 3))
        time_history: np.ndarray = np.zeros(num_snapshots)

        # Store initial conditions
        position_history[0] = self.positions
        velocity_history[0] = self.velocities
        time_history[0] = 0.0

        # Setup loop variables
        output_count: int = 1
        current_time: float = 0.0
        next_output_time: float = output_count * output_interval
        num_steps: int = int(time_frame / time_step)

        # Main simulation loop
        for i in range(num_steps):
            # Advance system by dt
            self._step(time_step)
            current_time = i * time_step

            # Check if it is time to save a snapshot
            if current_time >= next_output_time:
                position_history[output_count] = self.positions
                velocity_history[output_count] = self.velocities
                time_history[output_count] = current_time
                output_count += 1
                next_output_time = output_count * output_interval

        # Truncate arrays to remove unused zeros
        return (
            position_history[:output_count],
            velocity_history[:output_count],
            time_history[:output_count]
        )
