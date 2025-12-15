import numpy as np


class System:
    """Represents the N-body system.

    Attributes:
        num_bodies (int): Number of bodies in the system.
        positions (np.ndarray): Positions of bodies in 3D space.
        velocities (np.ndarray): Velocities of bodies in 3D space.
        masses (np.ndarray): Masses of bodies.
        G (float): Gravitational constant
    """

    def __init__(
        self, num_bodies: int, positions: np.ndarray,
        velocities: np.ndarray, masses: np.ndarray, G: float
    ) -> None:
        self.num_bodies = num_bodies
        self.positions = positions
        self.velocities = velocities
        self.masses = masses
        self.G = G
