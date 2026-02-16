# Boltzmann Distribution Lab

Interactive laboratory to verify Maxwell-Boltzmann statistics through particle velocity simulations with SQL database integration.

## Physics Background

The Maxwell-Boltzmann distribution describes the velocity/speed distribution of particles in an ideal gas at thermal equilibrium. It's a fundamental result in statistical mechanics that connects microscopic particle motion to macroscopic temperature.

**Key Results:**
- Speed distribution: f(v) ∝ v² exp(-mv²/2kT)
- Most probable speed: v_p = √(2kT/m)
- Mean speed: <v> = √(8kT/πm)
- RMS speed: v_rms = √(3kT/m)

## Day 1 Progress
- ✓ Implemented particle system with velocity initialization
- ✓ Theoretical Maxwell-Boltzmann distributions (speed & energy)
- ✓ Visualization comparing simulation vs theory
- ✓ Statistical analysis tools

## Quick Start
```bash
pip install -r requirements.txt
python test_simulation.py
```

## Features
- Generate particle ensembles at any temperature
- Compare simulation with analytical theory
- Visualize speed and energy distributions
- Calculate characteristic speeds (v_p, v_mean, v_rms)
- Statistical validation tools

## Project Structure
- `src/particle_system.py` - Particle simulation engine
- `src/boltzmann_theory.py` - Theoretical distributions
- `src/visualization.py` - Plotting and analysis
- `test_simulation.py` - Quick test demonstration

## Next Steps
- Day 2: SQL database for storing distributions at multiple temperatures
- Day 3: Interactive temperature queries and comparisons
- Day 4: Advanced analysis (chi-squared tests, phase space visualization)