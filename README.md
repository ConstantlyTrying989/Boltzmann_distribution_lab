# Boltzmann Distribution Lab

Interactive laboratory to verify Maxwell-Boltzmann statistics through particle velocity simulations with SQL database integration.

## Physics Background

The Maxwell-Boltzmann distribution describes the velocity/speed distribution of particles in an ideal gas at thermal equilibrium. It's a fundamental result in statistical mechanics that connects microscopic particle motion to macroscopic temperature.

**Key Results:**
- Speed distribution: f(v) ∝ v² exp(-mv²/2kT)
- Most probable speed: v_p = √(2kT/m)
- Mean speed: <v> = √(8kT/πm)
- RMS speed: v_rms = √(3kT/m)

## Progress

### Day 1 ✓
- ✓ Implemented particle system with velocity initialization
- ✓ Theoretical Maxwell-Boltzmann distributions (speed & energy)
- ✓ Visualization comparing simulation vs theory
- ✓ Statistical analysis tools

### Day 2 ✓
- ✓ Complete SQLite database schema
- ✓ Database integration with particle system
- ✓ Storage of distributions, statistics, and metadata
- ✓ Advanced query capabilities
- ✓ Database visualization tools
- ✓ Temperature sweep functionality

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run single test
python test_simulation.py

# Run database test (multiple temperatures)
python test_database.py

# Or use Jupyter notebook
jupyter notebook notebooks/demo.ipynb
```

## Database Schema

**Tables:**
- `simulations`: Metadata (temperature, particles, timestamp)
- `speed_distributions`: Histogram data for speeds
- `energy_distributions`: Histogram data for energies
- `statistics`: Summary statistics (simulation vs theory)
- `particles`: Optional individual particle data

**Example Queries:**
```python
from src.database import BoltzmannDatabase

with BoltzmannDatabase() as db:
    # Get all temperatures
    temps = db.get_all_temperatures()
    
    # Query by temperature range
    sims = db.get_simulations_by_temperature(250, 400)
    
    # Compare multiple temperatures
    comparison = db.compare_temperatures([300, 500, 1000])
```

## Features

- ✓ Generate particle ensembles at any temperature
- ✓ Compare simulation with analytical theory
- ✓ Visualize speed and energy distributions
- ✓ Store unlimited simulation runs in SQLite database
- ✓ Query and compare different temperatures
- ✓ Statistical validation and error analysis
- ✓ Temperature sweep automation

## Project Structure
```
boltzmann-distribution-lab/
├── src/
│   ├── particle_system.py        # Particle simulation
│   ├── boltzmann_theory.py       # Theoretical distributions
│   ├── visualization.py          # Basic plotting
│   ├── database.py              # SQLite database class
│   ├── simulation_runner.py     # High-level runner
│   └── database_visualization.py # Database-specific plots
├── data/
│   └── boltzmann.db             # SQLite database (created on first run)
├── notebooks/
│   └── demo.ipynb               # Interactive demo
├── test_simulation.py           # Single simulation test
└── test_database.py            # Database integration test
```

## Next Steps

- Day 3: Interactive queries, chi-squared goodness-of-fit tests
- Day 4: Advanced analysis, phase space visualization
- Day 5: Documentation polish, final visualizations

## Example Output

After running `test_database.py`, you'll have:
- A database with 6 temperature points (100K - 1000K)
- Beautiful overlaid distributions showing temperature dependence
- Statistical validation plots
- All data queryable via SQL

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- SciPy