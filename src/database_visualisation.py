"""Visualization tools for database queries."""

import matplotlib.pyplot as plt
import numpy as np
from src.boltzmann_theory import BoltzmannTheory

def plot_temperature_sweep_speeds(db, sim_ids, save_path=None):
    """
    Plot speed distributions for multiple temperatures from database.
    
    Parameters:
    -----------
    db : BoltzmannDatabase
        Database instance
    sim_ids : list
        List of simulation IDs to plot
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(sim_ids)))
    
    for i, sim_id in enumerate(sim_ids):
        # Get simulation metadata
        sim = db.get_simulation_by_id(sim_id)
        temp = sim['temperature']
        
        # Get speed distribution
        dist = db.get_speed_distribution(sim_id)
        
        # Plot histogram bars
        ax.bar(dist['bin_centers'], dist['bin_counts'], 
               width=np.diff(dist['bin_edges'])[0],
               alpha=0.4, color=colors[i], edgecolor='black', linewidth=0.5)
        
        # Plot theoretical curve
        theory = BoltzmannTheory(
            mass=sim['mass'],
            temperature=temp,
            dimensions=sim['dimensions']
        )
        v_range = np.linspace(0, dist['bin_edges'][-1], 300)
        theoretical = theory.maxwell_boltzmann_speed(v_range)
        ax.plot(v_range, theoretical, linewidth=2.5, color=colors[i],
                label=f'T = {temp:.0f} K')
    
    ax.set_xlabel('Speed (m/s)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title('Maxwell-Boltzmann Speed Distributions at Different Temperatures', 
                 fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()

def plot_statistics_vs_temperature(db, save_path=None):
    """
    Plot how various statistics change with temperature.
    
    Parameters:
    -----------
    db : BoltzmannDatabase
        Database instance
    save_path : str, optional
        Path to save figure
    """
    # Get all statistics
    all_stats = db.get_all_statistics()
    
    if not all_stats:
        print("No statistics found in database!")
        return
    
    # Extract data
    temperatures = [s['temperature'] for s in all_stats]
    mean_speeds_sim = [s['mean_speed'] for s in all_stats]
    mean_speeds_theory = [s['mean_speed_theory'] for s in all_stats]
    mean_energies_sim = [s['mean_energy'] for s in all_stats]
    mean_energies_theory = [s['mean_energy_theory'] for s in all_stats]
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot mean speed vs temperature
    ax1.scatter(temperatures, mean_speeds_sim, color='blue', s=50, 
                alpha=0.7, label='Simulation', zorder=3)
    ax1.plot(temperatures, mean_speeds_theory, 'r-', linewidth=2, 
             label='Theory', zorder=2)
    ax1.set_xlabel('Temperature (K)', fontsize=12)
    ax1.set_ylabel('Mean Speed (m/s)', fontsize=12)
    ax1.set_title('Mean Speed vs Temperature', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot mean energy vs temperature
    ax2.scatter(temperatures, mean_energies_sim, color='green', s=50,
                alpha=0.7, label='Simulation', zorder=3)
    ax2.plot(temperatures, mean_energies_theory, 'r-', linewidth=2,
             label='Theory (3kT/2)', zorder=2)
    ax2.set_xlabel('Temperature (K)', fontsize=12)
    ax2.set_ylabel('Mean Energy (J)', fontsize=12)
    ax2.set_title('Mean Kinetic Energy vs Temperature', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()

def plot_percent_error_analysis(db, save_path=None):
    """
    Plot percent error between simulation and theory.
    
    Parameters:
    -----------
    db : BoltzmannDatabase
        Database instance
    save_path : str, optional
        Path to save figure
    """
    all_stats = db.get_all_statistics()
    
    if not all_stats:
        print("No statistics found in database!")
        return
    
    temperatures = []
    speed_errors = []
    energy_errors = []
    
    for s in all_stats:
        temperatures.append(s['temperature'])
        
        # Calculate percent errors
        speed_error = 100 * (s['mean_speed'] - s['mean_speed_theory']) / s['mean_speed_theory']
        energy_error = 100 * (s['mean_energy'] - s['mean_energy_theory']) / s['mean_energy_theory']
        
        speed_errors.append(speed_error)
        energy_errors.append(energy_error)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(temperatures, speed_errors, color='blue', s=60, alpha=0.7,
               label='Mean Speed Error', marker='o')
    ax.scatter(temperatures, energy_errors, color='green', s=60, alpha=0.7,
               label='Mean Energy Error', marker='s')
    
    # Add reference lines
    ax.axhline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax.axhline(1, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(-1, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('Temperature (K)', fontsize=12)
    ax.set_ylabel('Percent Error (%)', fontsize=12)
    ax.set_title('Simulation Accuracy: Percent Error vs Theory', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()