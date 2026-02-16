"""Quick test of the Boltzmann Distribution Lab."""

from src.particle_system import ParticleSystem
from src.boltzmann_theory import BoltzmannTheory
from src.visualisation import (
    plot_speed_distribution,
    plot_energy_distribution,
    plot_statistics_comparison
)

def main():
    print("Testing Boltzmann Distribution Lab...")
    print("=" * 60)
    
    # Parameters
    n_particles = 10000
    temperature = 300.0  # Room temperature in Kelvin
    mass = 4.65e-26  # Mass of nitrogen molecule (kg)
    
    print(f"Number of particles: {n_particles}")
    print(f"Temperature: {temperature} K")
    print(f"Particle mass: {mass:.2e} kg (N2 molecule)")
    print()
    
    # Create particle system
    print("Initializing particle system...")
    system = ParticleSystem(
        n_particles=n_particles,
        temperature=temperature,
        mass=mass,
        dimensions=3
    )
    
    # Create theory object
    theory = BoltzmannTheory(
        mass=mass,
        temperature=temperature,
        dimensions=3
    )
    
    # Get speeds and energies
    speeds = system.get_speeds()
    energies = system.get_kinetic_energies()
    
    # Print simulation statistics
    print("Simulation Statistics:")
    print("-" * 60)
    sim_stats = system.get_statistics()
    for key, value in sim_stats.items():
        print(f"  {key}: {value:.4e}")
    
    print()
    print("Theoretical Predictions:")
    print("-" * 60)
    print(f"  Most probable speed: {theory.most_probable_speed():.4e} m/s")
    print(f"  Mean speed: {theory.mean_speed():.4e} m/s")
    print(f"  RMS speed: {theory.rms_speed():.4e} m/s")
    print(f"  Mean kinetic energy: {theory.mean_kinetic_energy():.4e} J")
    
    # Calculate percent differences
    print()
    print("Comparison (Simulation vs Theory):")
    print("-" * 60)
    theory_mean_speed = theory.mean_speed()
    diff_speed = 100 * (sim_stats['mean_speed'] - theory_mean_speed) / theory_mean_speed
    print(f"  Mean speed difference: {diff_speed:+.2f}%")
    
    theory_mean_energy = theory.mean_kinetic_energy()
    diff_energy = 100 * (sim_stats['mean_energy'] - theory_mean_energy) / theory_mean_energy
    print(f"  Mean energy difference: {diff_energy:+.2f}%")
    
    # Visualizations
    print()
    print("Generating visualizations...")
    
    print("  1. Speed distribution...")
    plot_speed_distribution(speeds, theory)
    
    print("  2. Energy distribution...")
    plot_energy_distribution(energies, theory)
    
    print("  3. Statistics comparison...")
    theory_stats = {
        'mean_speed': theory.mean_speed(),
        'mean_energy': theory.mean_kinetic_energy(),
        'temperature': temperature
    }
    plot_statistics_comparison(sim_stats, theory_stats)
    
    print()
    print("=" * 60)
    print("✓ Test complete! The distributions should match theory closely.")
    print("  Small differences (<5%) are expected due to finite sampling.")

if __name__ == "__main__":
    main()