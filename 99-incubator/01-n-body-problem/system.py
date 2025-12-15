import numpy as np


class System:
    """Represents the N-body system.

    Attributes:
        num_bodies (int): Number of bodies in the system.
        positions (np.ndarray): Positions of bodies in 3D space.
        velocities (np.ndarray): Velocities of bodies in 3D space.
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
        self.G: float = G
        self.masses: np.ndarray = masses
        self.accelerations: np.ndarray = np.zeros((num_bodies, num_bodies))

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

    def calculate_accelerations(self) -> None:
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
