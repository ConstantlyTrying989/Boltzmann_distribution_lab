import numpy as np

class ParticleSystem:
    """
    Simulate an ideal gas with particles in thermal equilibrium.
    
    This system allows particles to exchange kinetic energy through 
    elastic collisions, eventually reaching a Maxwell-Boltzmann 
    velocity distribution.
    """
    
    def __init__(self, n_particles, temperature, mass=1.0, dimensions=3):
        """
        Initialize the particle system.
        
        Parameters:
        -----------
        n_particles : int
            Number of particles in the system
        temperature : float
            Temperature in Kelvin
        mass : float
            Particle mass (atomic mass units, default=1.0)
        dimensions : int
            Number of spatial dimensions (1, 2, or 3)
        """
        self.n_particles = n_particles
        self.temperature = temperature
        self.mass = mass
        self.dimensions = dimensions
        self.k_B = 1.380649e-23  # Boltzmann constant (J/K)
        
        # Initialize velocities
        self.velocities = self._initialize_velocities()
        
    def _initialize_velocities(self):
        """
        Initialize particle velocities from Maxwell-Boltzmann distribution.
        
        Returns:
        --------
        velocities : np.ndarray
            Array of shape (n_particles, dimensions) with velocity components
        """
        # Standard deviation for each velocity component
        # From equipartition: <(1/2)m*v_i^2> = (1/2)k_B*T
        sigma = np.sqrt(self.k_B * self.temperature / self.mass)
        
        # Generate velocities from Gaussian distribution
        velocities = np.random.normal(
            loc=0.0,
            scale=sigma,
            size=(self.n_particles, self.dimensions)
        )
        
        return velocities
    
    def get_speeds(self):
        """
        Calculate speed (magnitude of velocity) for each particle.
        
        Returns:
        --------
        speeds : np.ndarray
            Array of particle speeds
        """
        return np.linalg.norm(self.velocities, axis=1)
    
    def get_kinetic_energies(self):
        """
        Calculate kinetic energy for each particle.
        
        Returns:
        --------
        energies : np.ndarray
            Array of kinetic energies
        """
        speeds = self.get_speeds()
        return 0.5 * self.mass * speeds**2
    
    def simulate_collisions(self, n_collisions):
        """
        Simulate random elastic collisions between particles.
        
        This helps demonstrate that the Maxwell-Boltzmann distribution
        is maintained through collisions (thermal equilibrium).
        
        Parameters:
        -----------
        n_collisions : int
            Number of collision events to simulate
        """
        for _ in range(n_collisions):
            # Pick two random particles
            i, j = np.random.choice(self.n_particles, size=2, replace=False)
            
            # Get velocities
            v_i = self.velocities[i].copy()
            v_j = self.velocities[j].copy()
            
            # For simplicity, exchange velocity components randomly
            # (This is a simplified collision model that conserves energy)
            # In reality, you'd solve collision dynamics properly
            
            # Random collision axis
            axis = np.random.randint(0, self.dimensions)
            
            # Exchange velocity component along collision axis
            self.velocities[i, axis], self.velocities[j, axis] = \
                self.velocities[j, axis], self.velocities[i, axis]
    
    def get_temperature_from_velocities(self):
        """
        Calculate temperature from current velocity distribution.
        Uses equipartition theorem: <E_kinetic> = (d/2) * k_B * T
        
        Returns:
        --------
        temperature : float
            Temperature calculated from kinetic energy
        """
        avg_kinetic_energy = np.mean(self.get_kinetic_energies())
        temperature = (2.0 * avg_kinetic_energy) / (self.dimensions * self.k_B)
        return temperature
    
    def set_temperature(self, new_temperature):
        """
        Rescale velocities to achieve a new temperature.
        
        Parameters:
        -----------
        new_temperature : float
            Target temperature in Kelvin
        """
        current_temp = self.get_temperature_from_velocities()
        scale_factor = np.sqrt(new_temperature / current_temp)
        self.velocities *= scale_factor
        self.temperature = new_temperature
    
    def get_statistics(self):
        """
        Calculate various statistical properties of the system.
        
        Returns:
        --------
        stats : dict
            Dictionary with statistical measurements
        """
        speeds = self.get_speeds()
        energies = self.get_kinetic_energies()
        
        stats = {
            'mean_speed': np.mean(speeds),
            'std_speed': np.std(speeds),
            'mean_energy': np.mean(energies),
            'std_energy': np.std(energies),
            'temperature': self.get_temperature_from_velocities(),
            'min_speed': np.min(speeds),
            'max_speed': np.max(speeds),
        }
        
        return stats