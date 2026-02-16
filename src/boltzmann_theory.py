import numpy as np
from scipy import integrate

class BoltzmannTheory:
    """
    Theoretical Maxwell-Boltzmann distributions and related calculations.
    """
    
    def __init__(self, mass=1.0, temperature=300.0, dimensions=3):
        """
        Initialize theoretical distributions.
        
        Parameters:
        -----------
        mass : float
            Particle mass (kg or atomic mass units)
        temperature : float
            Temperature in Kelvin
        dimensions : int
            Number of spatial dimensions
        """
        self.mass = mass
        self.temperature = temperature
        self.dimensions = dimensions
        self.k_B = 1.380649e-23  # Boltzmann constant (J/K)
        
    def maxwell_boltzmann_speed(self, v):
        """
        Maxwell-Boltzmann speed distribution.
        
        For 3D: f(v) = 4π * (m/(2πkT))^(3/2) * v^2 * exp(-mv^2/(2kT))
        
        Parameters:
        -----------
        v : float or np.ndarray
            Speed value(s)
            
        Returns:
        --------
        probability_density : float or np.ndarray
            Probability density at given speed(s)
        """
        if self.dimensions != 3:
            raise NotImplementedError("Only 3D distribution implemented")
        
        m = self.mass
        T = self.temperature
        k = self.k_B
        
        normalization = 4 * np.pi * (m / (2 * np.pi * k * T))**(3/2)
        exponential = np.exp(-m * v**2 / (2 * k * T))
        
        return normalization * v**2 * exponential
    
    def maxwell_boltzmann_energy(self, E):
        """
        Maxwell-Boltzmann energy distribution.
        
        For 3D: f(E) = 2π * (1/(πkT))^(3/2) * sqrt(E) * exp(-E/(kT))
        
        Parameters:
        -----------
        E : float or np.ndarray
            Energy value(s)
            
        Returns:
        --------
        probability_density : float or np.ndarray
            Probability density at given energy/energies
        """
        if self.dimensions != 3:
            raise NotImplementedError("Only 3D distribution implemented")
        
        T = self.temperature
        k = self.k_B
        
        # Avoid division by zero or sqrt of negative
        E = np.maximum(E, 1e-30)
        
        normalization = 2 * np.pi * (1 / (np.pi * k * T))**(3/2)
        exponential = np.exp(-E / (k * T))
        
        return normalization * np.sqrt(E) * exponential
    
    def most_probable_speed(self):
        """
        Calculate the most probable speed (peak of distribution).
        
        v_p = sqrt(2kT/m)
        """
        return np.sqrt(2 * self.k_B * self.temperature / self.mass)
    
    def mean_speed(self):
        """
        Calculate the mean speed.
        
        <v> = sqrt(8kT/(πm))
        """
        return np.sqrt(8 * self.k_B * self.temperature / (np.pi * self.mass))
    
    def rms_speed(self):
        """
        Calculate the root-mean-square speed.
        
        v_rms = sqrt(3kT/m)
        """
        return np.sqrt(3 * self.k_B * self.temperature / self.mass)
    
    def mean_kinetic_energy(self):
        """
        Calculate mean kinetic energy.
        
        <E> = (3/2) * k_B * T  (for 3D)
        """
        return (self.dimensions / 2.0) * self.k_B * self.temperature
    
    def get_speed_percentiles(self, percentiles=[25, 50, 75]):
        """
        Calculate speed percentiles by numerical integration.
        
        Parameters:
        -----------
        percentiles : list
            List of percentiles to calculate (0-100)
            
        Returns:
        --------
        speeds : dict
            Dictionary mapping percentile to speed value
        """
        # Find speeds corresponding to cumulative probabilities
        v_max = 10 * self.rms_speed()  # Upper integration limit
        
        results = {}
        for p in percentiles:
            target_prob = p / 100.0
            
            # Binary search for speed that gives target cumulative probability
            v_low, v_high = 0, v_max
            
            for _ in range(50):  # Convergence iterations
                v_mid = (v_low + v_high) / 2
                
                # Integrate from 0 to v_mid
                cum_prob, _ = integrate.quad(
                    self.maxwell_boltzmann_speed, 0, v_mid
                )
                
                if cum_prob < target_prob:
                    v_low = v_mid
                else:
                    v_high = v_mid
            
            results[p] = (v_low + v_high) / 2
        
        return results