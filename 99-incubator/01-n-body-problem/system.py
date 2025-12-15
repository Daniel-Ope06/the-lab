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
