"""High-level interface for running simulations and storing results."""

from src.particle_system import ParticleSystem
from src.boltzmann_theory import BoltzmannTheory
from src.database import BoltzmannDatabase

class SimulationRunner:
    """
    Convenience class for running simulations and storing to database.
    """
    
    def __init__(self, db_path='data/boltzmann.db'):
        """
        Initialize simulation runner.
        
        Parameters:
        -----------
        db_path : str
            Path to database file
        """
        self.db = BoltzmannDatabase(db_path)
    
    def run_and_store(self, n_particles, temperature, mass, dimensions=3,
                     description=None, store_particles=False):
        """
        Run a simulation and store all results in the database.
        
        Parameters:
        -----------
        n_particles : int
            Number of particles
        temperature : float
            Temperature in Kelvin
        mass : float
            Particle mass
        dimensions : int
            Number of dimensions (default=3)
        description : str, optional
            Description of the run
        store_particles : bool
            Whether to store individual particle data (default=False)
            
        Returns:
        --------
        sim_id : int
            Simulation ID in database
        """
        print(f"Running simulation: T={temperature}K, N={n_particles}...")
        
        # Create particle system
        system = ParticleSystem(
            n_particles=n_particles,
            temperature=temperature,
            mass=mass,
            dimensions=dimensions
        )
        
        # Create theory object
        theory = BoltzmannTheory(
            mass=mass,
            temperature=temperature,
            dimensions=dimensions
        )
        
        # Insert simulation metadata
        sim_id = self.db.insert_simulation(
            n_particles=n_particles,
            temperature=temperature,
            mass=mass,
            dimensions=dimensions,
            description=description
        )
        
        # Get data from simulation
        speeds = system.get_speeds()
        energies = system.get_kinetic_energies()
        velocities = system.velocities
        
        # Store distributions
        print(f"  Storing distributions...")
        self.db.insert_speed_distribution(sim_id, speeds)
        self.db.insert_energy_distribution(sim_id, energies)
        
        # Store statistics
        print(f"  Storing statistics...")
        sim_stats = system.get_statistics()
        theory_stats = {
            'most_probable_speed': theory.most_probable_speed(),
            'mean_speed': theory.mean_speed(),
            'rms_speed': theory.rms_speed(),
            'mean_energy': theory.mean_kinetic_energy()
        }
        self.db.insert_statistics(sim_id, sim_stats, theory_stats)
        
        # Optionally store individual particles
        if store_particles:
            print(f"  Storing individual particle data...")
            self.db.insert_particles(sim_id, velocities, speeds, energies)
        
        print(f"  ✓ Simulation stored with ID: {sim_id}")
        
        return sim_id
    
    def run_temperature_sweep(self, temperatures, n_particles, mass, 
                            dimensions=3):
        """
        Run simulations across multiple temperatures.
        
        Parameters:
        -----------
        temperatures : list
            List of temperatures to simulate
        n_particles : int
            Number of particles per simulation
        mass : float
            Particle mass
        dimensions : int
            Number of dimensions
            
        Returns:
        --------
        sim_ids : list
            List of simulation IDs
        """
        sim_ids = []
        
        print(f"Running temperature sweep: {len(temperatures)} temperatures")
        print(f"Temperature range: {min(temperatures):.1f}K - {max(temperatures):.1f}K")
        print("=" * 60)
        
        for i, temp in enumerate(temperatures, 1):
            description = f"Temperature sweep {i}/{len(temperatures)}"
            sim_id = self.run_and_store(
                n_particles=n_particles,
                temperature=temp,
                mass=mass,
                dimensions=dimensions,
                description=description
            )
            sim_ids.append(sim_id)
            print()
        
        print("=" * 60)
        print(f"✓ Temperature sweep complete! {len(sim_ids)} simulations stored.")
        
        return sim_ids
    
    def close(self):
        """Close database connection."""
        self.db.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()