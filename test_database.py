"""Test database integration with simulations."""

from src.simulation_runner import SimulationRunner
from src.database import BoltzmannDatabase
from src.database_visualisation import (
    plot_temperature_sweep_speeds,
    plot_statistics_vs_temperature,
    plot_percent_error_analysis
)
import numpy as np

def main():
    print("=" * 70)
    print("Testing Database Integration")
    print("=" * 70)
    print()
    
    # Parameters
    n_particles = 10000
    mass = 4.65e-26  # Nitrogen molecule
    temperatures = [100, 200, 300, 500, 800, 1000]  # Kelvin
    
    # Run simulations and store in database
    with SimulationRunner(db_path='data/boltzmann.db') as runner:
        print(f"Running {len(temperatures)} simulations...")
        print(f"Particles per simulation: {n_particles}")
        print(f"Temperatures: {temperatures}")
        print()
        
        sim_ids = runner.run_temperature_sweep(
            temperatures=temperatures,
            n_particles=n_particles,
            mass=mass,
            dimensions=3
        )
    
    print()
    print("=" * 70)
    print("Database Operations and Queries")
    print("=" * 70)
    print()
    
    # Open database for queries
    with BoltzmannDatabase('data/boltzmann.db') as db:
        # Get database summary
        print("Database Summary:")
        print("-" * 70)
        summary = db.get_database_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        print()
        
        # Query by temperature range
        print("Query: Simulations between 250K and 600K:")
        print("-" * 70)
        mid_temp_sims = db.get_simulations_by_temperature(250, 600)
        for sim in mid_temp_sims:
            print(f"  ID: {sim['sim_id']}, T: {sim['temperature']}K, "
                  f"N: {sim['n_particles']}, Time: {sim['timestamp']}")
        print()
        
        # Get all unique temperatures
        print("All temperatures in database:")
        print("-" * 70)
        all_temps = db.get_all_temperatures()
        print(f"  {all_temps}")
        print()
        
        # Query specific simulation
        print(f"Detailed view of simulation ID {sim_ids[2]}:")
        print("-" * 70)
        sim_data = db.get_simulation_by_id(sim_ids[2])
        for key, value in sim_data.items():
            print(f"  {key}: {value}")
        print()
        
        # Get statistics for a simulation
        print(f"Statistics for simulation ID {sim_ids[2]}:")
        print("-" * 70)
        stats = db.get_statistics(sim_ids[2])
        if stats:
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.6e}")
                else:
                    print(f"  {key}: {value}")
        print()
        
        # Compare multiple temperatures
        print("Comparing temperatures [300K, 500K, 1000K]:")
        print("-" * 70)
        comparison = db.compare_temperatures([300, 500, 1000])
        for temp, data in comparison.items():
            print(f"  T = {temp}K:")
            stats = data['statistics']
            print(f"    Mean speed (sim): {stats['mean_speed']:.4e} m/s")
            print(f"    Mean speed (theory): {stats['mean_speed_theory']:.4e} m/s")
            print(f"    Percent error: {100*(stats['mean_speed']-stats['mean_speed_theory'])/stats['mean_speed_theory']:.2f}%")
        print()
        
        # Visualisations
        print("=" * 70)
        print("Generating Visualisations from Database")
        print("=" * 70)
        print()
        
        print("1. Speed distributions at all temperatures...")
        plot_temperature_sweep_speeds(db, sim_ids)
        
        print("2. Statistics vs temperature...")
        plot_statistics_vs_temperature(db)
        
        print("3. Percent error analysis...")
        plot_percent_error_analysis(db)
    
    print()
    print("=" * 70)
    print("✓ Database test complete!")
    print(f"  Database location: data/boltzmann.db")
    print(f"  Total simulations stored: {len(sim_ids)}")
    print("=" * 70)

if __name__ == "__main__":
    main()