import numpy as np
import random
from typing import Tuple, List
from n_body_system import NBodySystem


class LevelGenerator:
    """
    Generates N-Body simulation states for the game.
    Can handle both named 'Scenarios' (hardcoded scientific setups)
    and numbered 'Levels' (procedural generation).
    """

    def __init__(self):
        # Physical Constants (AU, Days, Solar Mass)
        self.G = 0.00029591220828
        self.EARTH_MASS = 3.003e-6
        self.SUN_MASS = 1.0

    def generate_level(
        self, level_id: str | int
    ) -> Tuple[NBodySystem, List[str | None], List[str | None], bool]:
        """
        Pass a string (e.g. "false_stability") for a specific scenario.
        Pass an int (e.g. 5) for a procedurally generated level.

        Returns:
            (system, labels, colors, legend_visible)
        """

        if type(level_id) is str:
            return self._get_named_scenario(level_id)
        elif type(level_id) is int:
            return self._generate_procedural_level(level_id)
        else:
            raise ValueError(
                "Level ID must be a string (scenario) or int (level number)."
            )

    def _get_named_scenario(
        self, name: str
    ) -> Tuple[NBodySystem, List[str | None], List[str | None], bool]:
        """Returns initial conditions for 3-Body Problem scenarios

        **Scenarios:**
        1. always_stable
        2. false_stability
        """

        labels: List[str | None] = ["Sun 1", "Sun 2", "Sun 3", "Planet 1"]
        colors: List[str | None] = ["orange", "yellow", "coral", "cyan"]

        if name == "always_stable":
            # --- SCENARIO 1: The "Sandbox" ---
            binary_sep = 0.2
            dist_C = 4.0

            # Velocities (Circular approximation)
            v_bin = np.sqrt(self.G * (2 * self.SUN_MASS) / binary_sep)
            v_C = np.sqrt(self.G * (2 * self.SUN_MASS) / dist_C)
            v_planet = np.sqrt(self.G * (0.5 * self.SUN_MASS) / 0.1)

            positions = np.array([
                [binary_sep/2, 0, 0], [-binary_sep/2, 0, 0],
                [0, dist_C, 0], [0.1, dist_C, 0]
            ])
            velocities = np.array([
                [0, v_bin/2, 0], [0, -v_bin/2, 0],
                [-v_C, 0, 0], [-v_C, v_planet, 0]
            ])
            masses = np.array([self.SUN_MASS, self.SUN_MASS,
                              0.5 * self.SUN_MASS, self.EARTH_MASS])

        elif name == "false_stability":
            # --- SCENARIO 2: The "False Hope" ---
            binary_sep = 0.2
            start_dist_C = 6.0
            perihelion_C = 1.2

            v_bin = np.sqrt(self.G * (2 * self.SUN_MASS) / binary_sep)

            # Vis-Viva for Elliptical Orbit of Sun C
            semi_major_axis = (perihelion_C + start_dist_C) / 2
            v_aphelion_C = np.sqrt(
                self.G * (2 * self.SUN_MASS) * (
                    2/start_dist_C - 1/semi_major_axis))

            v_planet = np.sqrt(self.G * (0.5 * self.SUN_MASS) / 0.1)

            positions = np.array([
                [binary_sep/2, 0, 0], [-binary_sep/2, 0, 0],
                [0, start_dist_C, 0], [0.1, start_dist_C, 0]
            ])
            velocities = np.array([
                [0, v_bin/2, 0], [0, -v_bin/2, 0],
                [-v_aphelion_C, 0, 0], [-v_aphelion_C, v_planet, 0]
            ])
            masses = np.array([self.SUN_MASS, self.SUN_MASS,
                              0.5 * self.SUN_MASS, self.EARTH_MASS,])

        else:
            raise ValueError(f"Unknown scenario name: {name}")

        system = NBodySystem(
            len(masses), positions, velocities, masses, G=self.G)
        system.recenter_com_to_origin()

        return (system, labels, colors, True)

    def _generate_procedural_level(
        self, level: int
    ) -> Tuple[NBodySystem, List[str | None], List[str | None], bool]:
        """
        Generates a random system based on difficulty level.
        Level 1-5: Single Star
        Level 6-10: Binary Star
        """

        num_stars = 2 if level > 5 else 1
        num_planets = min(level + 2, 8)

        masses: List[float] = []
        positions: List = []
        velocities: List = []
        labels: List[str | None] = []
        colors: List[str | None] = []

        # Create Stars
        if num_stars == 1:
            # Single Star at (0,0,0)
            mass: float = random.uniform(1.0, 1.2)
            masses.append(mass)
            positions.append([0, 0, 0])
            velocities.append([0, 0, 0])
            labels.append("Sun")
            colors.append("gold")

        elif num_stars == 2:
            # Binary Stars orbiting Center of Mass (0,0,0)
            m1: float = random.uniform(1.0, 1.5)
            m2: float = random.uniform(0.8, 1.0)
            sep: float = random.uniform(0.3, 0.6)  # Separation in AU

            # Distance from COM
            r1: float = sep * m2 / (m1 + m2)
            r2: float = sep * m1 / (m1 + m2)

            # Orbital Velocity (Circular)
            period = np.sqrt(4 * np.pi**2 * sep**3 / (self.G * (m1 + m2)))
            v1 = 2 * np.pi * r1 / period
            v2 = 2 * np.pi * r2 / period

            # Sun 1 (Left)
            masses.append(m1)
            positions.append([-r1, 0, 0])
            velocities.append([0, -v1, 0])  # Moving Down
            labels.append("Sun 1")
            colors.append("darkorange")

            # Sun 2 (Right)
            masses.append(m2)
            positions.append([r2, 0, 0])
            velocities.append([0, v2, 0])  # Moving Up
            labels.append("Sun 2")
            colors.append("orangered")

        # Total mass of stars (for calculating planet orbits)
        total_star_mass = sum(masses)

        # Create Planets (The Obstacles)
        for i in range(num_planets):
            # A. Random Orbital Parameters
            # Dist: 2.0 to 10.0 AU
            a = random.uniform(2.0, 6.0 + (level * 0.5))

            # Eccentricity (Shape):
            # 50% Circular (e=0), 30% Elliptical (e=0.3), 20% Extreme (e=0.6)
            roll_e = random.random()
            if roll_e < 0.5:
                e = 0.0
            elif roll_e < 0.8:
                e = random.uniform(0.1, 0.3)
            else:
                e = random.uniform(0.4, 0.7)

            # Inclination (Tilt Z-axis):
            # 70% Flat (i=0), 30% Tilted (i up to 45 degrees)
            roll_i = random.random()
            inclination = 0.0
            if roll_i > 0.7:
                inclination = np.radians(random.uniform(10, 45))

            # Random rotation of orbit
            w = random.uniform(0, 2*np.pi)  # Argument of periapsis

            # B. Convert to Cartesian State Vectors
            # Calculate position/velocity relative to
            # the Star System Center (0,0,0)
            pos_vec, vel_vec = self._get_keplerian_state(
                total_star_mass, a, e, inclination, w)

            # C. Add to Lists
            masses.append(random.uniform(1e-5, 1e-4))  # Earth to Neptune size
            positions.append(pos_vec)
            velocities.append(vel_vec)
            labels.append(f"Planet {i+1}")

            # D. Varied Colors (Shades of Cyan/Blue/Green)
            # Mix base Cyan (#00FFFF) with random amounts of Green/Blue
            r = 0
            g = int(random.uniform(100, 255))
            b = int(random.uniform(200, 255))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            colors.append(hex_color)

        # Create Player Probe (Mass ~ 0)
        # Enters from left (-X)
        # masses.append(1e-10)
        # positions.append([-8.0, 2.0, 0])
        # velocities.append([3.0, -0.5, 0])  # Moving Right
        # labels.append("Rocket")
        # colors.append("magenta")

        # Convert to Arrays & Build System
        masses_arr = np.array(masses)
        pos_arr = np.array(positions)
        vel_arr = np.array(velocities)

        system = NBodySystem(
            len(masses), pos_arr, vel_arr, masses_arr, G=self.G)
        system.recenter_com_to_origin()

        return (system, labels, colors, True)

    def _get_keplerian_state(self, M_star, a, e, i, w):
        """
        Converts orbital elements to Position/Velocity vectors.
        M_star: Mass of central body
        a: Semi-major axis
        e: Eccentricity
        i: Inclination (radians)
        w: Argument of periapsis (radians)
        """
        # 1. Solve at Periapsis (closest point) for simplicity
        # At periapsis, true anomaly (nu) = 0
        r = a * (1 - e)
        v = np.sqrt(self.G * M_star * (2/r - 1/a))

        # In orbital plane (P, Q frame):
        # Position is along x-axis at periapsis
        r_orb = np.array([r, 0, 0])
        # Velocity is purely along y-axis at periapsis
        v_orb = np.array([0, v, 0])

        # 2. Rotation Matrices
        # Rotate by Argument of Periapsis (w) around Z
        R_w = np.array([
            [np.cos(w), -np.sin(w), 0],
            [np.sin(w),  np.cos(w), 0],
            [0,          0,         1]
        ])

        # Rotate by Inclination (i) around X
        R_i = np.array([
            [1, 0,          0],
            [0, np.cos(i), -np.sin(i)],
            [0, np.sin(i),  np.cos(i)]
        ])

        # Combine Rotations: Apply w then i
        # (We skip Longitude of Ascending Node for simplicity,
        # usually just another Z rotation)
        R = R_i @ R_w

        pos_vec = R @ r_orb
        vel_vec = R @ v_orb

        return pos_vec, vel_vec
