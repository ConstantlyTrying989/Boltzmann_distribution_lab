import sqlite3
import json
import numpy as np
from datetime import datetime
from pathlib import Path

class BoltzmannDatabase:
    """
    SQLite database for storing particle simulation results.
    
    Tables:
    - simulations: metadata for each simulation run
    - distributions: histogram data for speed/energy distributions
    - statistics: summary statistics for each run
    - particles: individual particle data (optional, for detailed analysis)
    """
    
    def __init__(self, db_path='data/boltzmann.db'):
        """
        Initialize database connection and create tables.
        
        Parameters:
        -----------
        db_path : str
            Path to SQLite database file
        """
        self.db_path = db_path
        
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables if they don't exist."""
        
        # Simulations metadata table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulations (
                sim_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                n_particles INTEGER NOT NULL,
                temperature REAL NOT NULL,
                mass REAL NOT NULL,
                dimensions INTEGER NOT NULL,
                description TEXT,
                UNIQUE(timestamp)
            )
        ''')
        
        # Speed distribution table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS speed_distributions (
                dist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sim_id INTEGER NOT NULL,
                bin_edges TEXT NOT NULL,
                bin_counts TEXT NOT NULL,
                bin_centers TEXT NOT NULL,
                FOREIGN KEY (sim_id) REFERENCES simulations(sim_id),
                UNIQUE(sim_id)
            )
        ''')
        
        # Energy distribution table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_distributions (
                dist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sim_id INTEGER NOT NULL,
                bin_edges TEXT NOT NULL,
                bin_counts TEXT NOT NULL,
                bin_centers TEXT NOT NULL,
                FOREIGN KEY (sim_id) REFERENCES simulations(sim_id),
                UNIQUE(sim_id)
            )
        ''')
        
        # Statistics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sim_id INTEGER NOT NULL,
                mean_speed REAL NOT NULL,
                std_speed REAL NOT NULL,
                mean_energy REAL NOT NULL,
                std_energy REAL NOT NULL,
                measured_temperature REAL NOT NULL,
                most_probable_speed_sim REAL,
                most_probable_speed_theory REAL,
                mean_speed_theory REAL,
                rms_speed_theory REAL,
                mean_energy_theory REAL,
                FOREIGN KEY (sim_id) REFERENCES simulations(sim_id),
                UNIQUE(sim_id)
            )
        ''')
        
        # Optional: Individual particles table (for detailed analysis)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS particles (
                particle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sim_id INTEGER NOT NULL,
                speed REAL NOT NULL,
                energy REAL NOT NULL,
                vx REAL,
                vy REAL,
                vz REAL,
                FOREIGN KEY (sim_id) REFERENCES simulations(sim_id)
            )
        ''')
        
        # Create indices for faster queries
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sim_temperature 
            ON simulations(temperature)
        ''')
        
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sim_timestamp 
            ON simulations(timestamp)
        ''')
        
        self.conn.commit()
    
    def insert_simulation(self, n_particles, temperature, mass, dimensions, 
                         description=None):
        """
        Insert a new simulation run into the database.
        
        Parameters:
        -----------
        n_particles : int
            Number of particles
        temperature : float
            Temperature in Kelvin
        mass : float
            Particle mass
        dimensions : int
            Number of dimensions
        description : str, optional
            Description of the simulation
            
        Returns:
        --------
        sim_id : int
            ID of the inserted simulation
        """
        timestamp = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO simulations 
            (timestamp, n_particles, temperature, mass, dimensions, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, n_particles, temperature, mass, dimensions, description))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def insert_speed_distribution(self, sim_id, speeds, n_bins=50):
        """
        Calculate and insert speed distribution histogram.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
        speeds : np.ndarray
            Array of particle speeds
        n_bins : int
            Number of histogram bins
        """
        counts, bin_edges = np.histogram(speeds, bins=n_bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Convert to JSON strings for storage
        bin_edges_json = json.dumps(bin_edges.tolist())
        counts_json = json.dumps(counts.tolist())
        centers_json = json.dumps(bin_centers.tolist())
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO speed_distributions 
            (sim_id, bin_edges, bin_counts, bin_centers)
            VALUES (?, ?, ?, ?)
        ''', (sim_id, bin_edges_json, counts_json, centers_json))
        
        self.conn.commit()
    
    def insert_energy_distribution(self, sim_id, energies, n_bins=50):
        """
        Calculate and insert energy distribution histogram.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
        energies : np.ndarray
            Array of particle energies
        n_bins : int
            Number of histogram bins
        """
        counts, bin_edges = np.histogram(energies, bins=n_bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Convert to JSON strings for storage
        bin_edges_json = json.dumps(bin_edges.tolist())
        counts_json = json.dumps(counts.tolist())
        centers_json = json.dumps(bin_centers.tolist())
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO energy_distributions 
            (sim_id, bin_edges, bin_counts, bin_centers)
            VALUES (?, ?, ?, ?)
        ''', (sim_id, bin_edges_json, counts_json, centers_json))
        
        self.conn.commit()
    
    def insert_statistics(self, sim_id, sim_stats, theory_stats):
        """
        Insert simulation and theoretical statistics.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
        sim_stats : dict
            Statistics from simulation
        theory_stats : dict
            Theoretical statistics
        """
        self.cursor.execute('''
            INSERT OR REPLACE INTO statistics 
            (sim_id, mean_speed, std_speed, mean_energy, std_energy, 
             measured_temperature, most_probable_speed_theory, 
             mean_speed_theory, rms_speed_theory, mean_energy_theory)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sim_id,
            sim_stats['mean_speed'],
            sim_stats['std_speed'],
            sim_stats['mean_energy'],
            sim_stats['std_energy'],
            sim_stats['temperature'],
            theory_stats['most_probable_speed'],
            theory_stats['mean_speed'],
            theory_stats['rms_speed'],
            theory_stats['mean_energy']
        ))
        
        self.conn.commit()
    
    def insert_particles(self, sim_id, velocities, speeds, energies):
        """
        Insert individual particle data (optional, for detailed analysis).
        
        Warning: This can create large databases for many particles.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
        velocities : np.ndarray
            Velocity vectors (n_particles, 3)
        speeds : np.ndarray
            Particle speeds
        energies : np.ndarray
            Particle energies
        """
        data = []
        for i in range(len(speeds)):
            vx = velocities[i, 0] if velocities.shape[1] > 0 else None
            vy = velocities[i, 1] if velocities.shape[1] > 1 else None
            vz = velocities[i, 2] if velocities.shape[1] > 2 else None
            
            data.append((sim_id, speeds[i], energies[i], vx, vy, vz))
        
        self.cursor.executemany('''
            INSERT INTO particles (sim_id, speed, energy, vx, vy, vz)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        
        self.conn.commit()
    
    def get_simulation_by_id(self, sim_id):
        """
        Retrieve simulation metadata by ID.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
            
        Returns:
        --------
        sim_data : dict
            Simulation metadata
        """
        self.cursor.execute('''
            SELECT * FROM simulations WHERE sim_id = ?
        ''', (sim_id,))
        
        row = self.cursor.fetchone()
        if row is None:
            return None
        
        columns = [desc[0] for desc in self.cursor.description]
        return dict(zip(columns, row))
    
    def get_simulations_by_temperature(self, temp_min, temp_max):
        """
        Retrieve all simulations within a temperature range.
        
        Parameters:
        -----------
        temp_min : float
            Minimum temperature
        temp_max : float
            Maximum temperature
            
        Returns:
        --------
        simulations : list of dict
            List of simulation metadata dictionaries
        """
        self.cursor.execute('''
            SELECT * FROM simulations 
            WHERE temperature >= ? AND temperature <= ?
            ORDER BY temperature
        ''', (temp_min, temp_max))
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_all_temperatures(self):
        """
        Get list of all unique temperatures in database.
        
        Returns:
        --------
        temperatures : list
            Sorted list of temperatures
        """
        self.cursor.execute('''
            SELECT DISTINCT temperature FROM simulations 
            ORDER BY temperature
        ''')
        
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_speed_distribution(self, sim_id):
        """
        Retrieve speed distribution for a simulation.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
            
        Returns:
        --------
        distribution : dict
            Dictionary with 'bin_edges', 'bin_counts', 'bin_centers'
        """
        self.cursor.execute('''
            SELECT bin_edges, bin_counts, bin_centers 
            FROM speed_distributions 
            WHERE sim_id = ?
        ''', (sim_id,))
        
        row = self.cursor.fetchone()
        if row is None:
            return None
        
        return {
            'bin_edges': np.array(json.loads(row[0])),
            'bin_counts': np.array(json.loads(row[1])),
            'bin_centers': np.array(json.loads(row[2]))
        }
    
    def get_energy_distribution(self, sim_id):
        """
        Retrieve energy distribution for a simulation.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
            
        Returns:
        --------
        distribution : dict
            Dictionary with 'bin_edges', 'bin_counts', 'bin_centers'
        """
        self.cursor.execute('''
            SELECT bin_edges, bin_counts, bin_centers 
            FROM energy_distributions 
            WHERE sim_id = ?
        ''', (sim_id,))
        
        row = self.cursor.fetchone()
        if row is None:
            return None
        
        return {
            'bin_edges': np.array(json.loads(row[0])),
            'bin_counts': np.array(json.loads(row[1])),
            'bin_centers': np.array(json.loads(row[2]))
        }
    
    def get_statistics(self, sim_id):
        """
        Retrieve statistics for a simulation.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID
            
        Returns:
        --------
        stats : dict
            Statistics dictionary
        """
        self.cursor.execute('''
            SELECT * FROM statistics WHERE sim_id = ?
        ''', (sim_id,))
        
        row = self.cursor.fetchone()
        if row is None:
            return None
        
        columns = [desc[0] for desc in self.cursor.description]
        return dict(zip(columns, row))
    
    def get_all_statistics(self):
        """
        Retrieve statistics for all simulations.
        
        Returns:
        --------
        stats : list of dict
            List of statistics dictionaries
        """
        self.cursor.execute('''
            SELECT s.*, sim.temperature, sim.n_particles 
            FROM statistics s
            JOIN simulations sim ON s.sim_id = sim.sim_id
            ORDER BY sim.temperature
        ''')
        
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        
        return [dict(zip(columns, row)) for row in rows]
    
    def compare_temperatures(self, temp_list):
        """
        Get comparison data for multiple temperatures.
        
        Parameters:
        -----------
        temp_list : list
            List of temperatures to compare
            
        Returns:
        --------
        comparison : dict
            Dictionary mapping temperatures to their data
        """
        comparison = {}
        
        for temp in temp_list:
            self.cursor.execute('''
                SELECT sim_id FROM simulations 
                WHERE ABS(temperature - ?) < 0.01
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (temp,))
            
            row = self.cursor.fetchone()
            if row:
                sim_id = row[0]
                comparison[temp] = {
                    'sim_id': sim_id,
                    'metadata': self.get_simulation_by_id(sim_id),
                    'statistics': self.get_statistics(sim_id),
                    'speed_dist': self.get_speed_distribution(sim_id),
                    'energy_dist': self.get_energy_distribution(sim_id)
                }
        
        return comparison
    
    def delete_simulation(self, sim_id):
        """
        Delete a simulation and all associated data.
        
        Parameters:
        -----------
        sim_id : int
            Simulation ID to delete
        """
        # Delete from all tables
        tables = ['particles', 'statistics', 'energy_distributions', 
                  'speed_distributions', 'simulations']
        
        for table in tables:
            self.cursor.execute(f'DELETE FROM {table} WHERE sim_id = ?', (sim_id,))
        
        self.conn.commit()
    
    def get_database_summary(self):
        """
        Get summary statistics about the database.
        
        Returns:
        --------
        summary : dict
            Summary information
        """
        summary = {}
        
        # Count simulations
        self.cursor.execute('SELECT COUNT(*) FROM simulations')
        summary['total_simulations'] = self.cursor.fetchone()[0]
        
        # Temperature range
        self.cursor.execute('SELECT MIN(temperature), MAX(temperature) FROM simulations')
        temp_range = self.cursor.fetchone()
        summary['temperature_range'] = temp_range if temp_range[0] else (None, None)
        
        # Count particles
        self.cursor.execute('SELECT COUNT(*) FROM particles')
        summary['total_particles_stored'] = self.cursor.fetchone()[0]
        
        # Database size
        summary['database_path'] = self.db_path
        if Path(self.db_path).exists():
            size_bytes = Path(self.db_path).stat().st_size
            summary['database_size_mb'] = size_bytes / (1024 * 1024)
        
        return summary
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()