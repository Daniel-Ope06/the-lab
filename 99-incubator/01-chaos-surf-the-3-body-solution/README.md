# 🌊 Chaos Surf: The 3 Body Solution

> **Civilization doesn't live on a rock anymore. It lives on the Wave.**

## 🔭 The Concept

**Chaos Surf** is a survival simulation game based on the terrifying physics of the Three-Body Problem. You are the AI guidance system for an Ark Ship trapped in a solar system with **three suns**.

Your goal is to **surf the gravity tunnels** (invariant manifolds) between the stars to keep humanity alive for one more day.

## 🎮 The Gameplay

> **Don't Fight the Current**

Most space simulators are about **Thrust** (Power). This game is about **Drift** (Efficiency).

- **The Problem:** You have limited fuel. If you try to fly against the gravity of three suns, you will run out and die.
- **The Solution:** You must find the invisible "Ridges" in space (Lagrange Points) where gravity cancels out.
- **The Mechanic:**
  - **Scan:** Use your AI to visualize the hidden "Green Tunnels" (safe zones) opening in the chaos.
  - **Surf:** Launch the Ark into the tunnel at the exact right second.
  - **Glide:** Ride the gravitational wave between the suns for free, conserving fuel for the next jump.

## 🛠 Under the Hood

This project is a hybrid of physics and game design.

- **The Brain (Python):** A custom N-Body Physics Engine that calculates the real-time interaction of stars.

- **The Face (Godot):** A visual layer that renders the chaos and allows player interaction.

- **The Oracle (AI/PINN):** A Physics-Informed Neural Network to solve the chaos in real-time, generating "Stability Heatmaps" so players can see the safe paths.
