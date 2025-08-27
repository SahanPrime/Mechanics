# Ball Bouncing Simulation with Pygame

This project is a Python simulation of a ball bouncing under different gravity conditions, built using the [Pygame](https://www.pygame.org/news) library. It provides a visually rich and interactive way to explore how gravity affects the motion of a bouncing ball. The simulation features velocity control, a gravity slider, and live stats for an educational and engaging experience.

## Features

- **Customizable Gravity:** Simulate ball bouncing under various gravity values (Earth, Moon, Jupiter, or custom) using a slider.
- **Drag to Set Initial Velocity:** Click and drag the ball to set its initial velocity and direction.
- **Physics-Based Motion:** Realistic motion using kinematic equations and energy loss on bounce.
- **Live Statistics:** View bounce count, maximum bounce height, velocity magnitude & angle, and elapsed simulation time.
- **Pause/Play Controls:** Toggle simulation with a button or keyboard.
- **Reset Function:** Instantly reset ball and stats to initial state.
- **Random Velocity:** Press Space to give the ball a random velocity.
- **Interactive UI:** Slider, buttons, and visual feedback for user actions.
- **Animated Trail & Velocity Vector:** See the ball’s velocity as an arrow and its bounce path as a fading trail.
- **Opening Screen:** A friendly welcome screen with instructions and animated preview.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SahanPrime/Mechanics.git
   cd Mechanics
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame
   ```

## Usage

Run the simulation:

```bash
python gravitysimulation.py
```

### Controls

- **Pause/Play:** `P` key or Pause button
- **Reset:** `R` key
- **Random Velocity:** `Space` key
- **Gravity Slider:** Drag the slider handle at the bottom
- **Increase/Decrease Gravity:** Up/Down arrow keys
- **Set Initial Velocity:** Pause the simulation and drag the ball to set velocity
- **Quit:** Close window

## How It Works

The simulation uses kinematic equations of motion under constant acceleration, with gravity adjustable in real time. When the ball hits the ground or a wall, it bounces with reduced energy (elasticity), and statistics are updated live. The user can interactively set the ball’s velocity, change gravity, and observe the effects instantly.

## Screenshots

*(To add: Run the simulation and capture screenshots of the main interface, drag-to-set velocity, and stats panel)*

## Requirements

- Python 3.7+
- Pygame

## File Structure

- `gravitysimulation.py` — Main simulation code.
- `README.md` — This documentation.

## License

This project is licensed under the MIT License.

## Author

[Sahan Rashmika (SahanPrime)](https://github.com/SahanPrime)

---

**Enjoy exploring the physics of bouncing balls!**
