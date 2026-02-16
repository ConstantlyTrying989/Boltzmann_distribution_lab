import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2

def plot_speed_distribution(speeds, theory, bins=50, save_path=None):
    """
    Plot simulated speed distribution vs theoretical prediction.
    
    Parameters:
    -----------
    speeds : np.ndarray
        Array of particle speeds from simulation
    theory : BoltzmannTheory
        Theory object for theoretical predictions
    bins : int
        Number of histogram bins
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram of simulated speeds
    counts, bin_edges, _ = ax.hist(
        speeds, 
        bins=bins, 
        density=True, 
        alpha=0.6, 
        color='blue',
        edgecolor='black',
        label='Simulation'
    )
    
    # Plot theoretical distribution
    v_range = np.linspace(0, np.max(speeds) * 1.2, 500)
    theoretical = theory.maxwell_boltzmann_speed(v_range)
    ax.plot(v_range, theoretical, 'r-', linewidth=2, label='Maxwell-Boltzmann Theory')
    
    # Mark characteristic speeds
    v_p = theory.most_probable_speed()
    v_mean = theory.mean_speed()
    v_rms = theory.rms_speed()
    
    ax.axvline(v_p, color='green', linestyle='--', alpha=0.7, 
               label=f'Most Probable: {v_p:.2e} m/s')
    ax.axvline(v_mean, color='orange', linestyle='--', alpha=0.7,
               label=f'Mean: {v_mean:.2e} m/s')
    ax.axvline(v_rms, color='purple', linestyle='--', alpha=0.7,
               label=f'RMS: {v_rms:.2e} m/s')
    
    ax.set_xlabel('Speed (m/s)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title(f'Maxwell-Boltzmann Speed Distribution (T = {theory.temperature:.0f} K)', 
                 fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()

def plot_energy_distribution(energies, theory, bins=50, save_path=None):
    """
    Plot simulated energy distribution vs theoretical prediction.
    
    Parameters:
    -----------
    energies : np.ndarray
        Array of particle kinetic energies from simulation
    theory : BoltzmannTheory
        Theory object for theoretical predictions
    bins : int
        Number of histogram bins
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram of simulated energies
    ax.hist(
        energies,
        bins=bins,
        density=True,
        alpha=0.6,
        color='green',
        edgecolor='black',
        label='Simulation'
    )
    
    # Plot theoretical distribution
    E_range = np.linspace(0, np.max(energies) * 1.2, 500)
    theoretical = theory.maxwell_boltzmann_energy(E_range)
    ax.plot(E_range, theoretical, 'r-', linewidth=2, label='Maxwell-Boltzmann Theory')
    
    # Mark mean energy
    E_mean = theory.mean_kinetic_energy()
    ax.axvline(E_mean, color='blue', linestyle='--', alpha=0.7,
               label=f'Mean Energy: {E_mean:.2e} J')
    
    ax.set_xlabel('Kinetic Energy (J)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title(f'Energy Distribution (T = {theory.temperature:.0f} K)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()

def plot_temperature_comparison(temperatures, systems_data, save_path=None):
    """
    Compare speed distributions at different temperatures.
    
    Parameters:
    -----------
    temperatures : list
        List of temperatures
    systems_data : list
        List of (speeds, theory) tuples for each temperature
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(temperatures)))
    
    for i, (temp, (speeds, theory)) in enumerate(zip(temperatures, systems_data)):
        # Plot histogram
        ax.hist(speeds, bins=40, density=True, alpha=0.3, 
                color=colors[i], edgecolor='black', linewidth=0.5)
        
        # Plot theoretical curve
        v_range = np.linspace(0, np.max(speeds) * 1.1, 300)
        theoretical = theory.maxwell_boltzmann_speed(v_range)
        ax.plot(v_range, theoretical, linewidth=2, color=colors[i],
                label=f'T = {temp:.0f} K')
    
    ax.set_xlabel('Speed (m/s)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title('Maxwell-Boltzmann Distribution at Different Temperatures', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()

def plot_statistics_comparison(sim_stats, theory_stats, save_path=None):
    """
    Create bar chart comparing simulation vs theory statistics.
    
    Parameters:
    -----------
    sim_stats : dict
        Statistics from simulation
    theory_stats : dict
        Theoretical statistics
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['mean_speed', 'mean_energy', 'temperature']
    labels = ['Mean Speed\n(m/s)', 'Mean Energy\n(J)', 'Temperature\n(K)']
    
    x = np.arange(len(metrics))
    width = 0.35
    
    sim_values = [sim_stats[m] for m in metrics]
    theory_values = [theory_stats[m] for m in metrics]
    
    bars1 = ax.bar(x - width/2, sim_values, width, label='Simulation', 
                   alpha=0.8, color='blue')
    bars2 = ax.bar(x + width/2, theory_values, width, label='Theory',
                   alpha=0.8, color='red')
    
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Simulation vs Theory: Statistical Comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add percentage difference labels
    for i, (sim, theo) in enumerate(zip(sim_values, theory_values)):
        diff_pct = 100 * (sim - theo) / theo
        ax.text(i, max(sim, theo) * 1.05, f'{diff_pct:+.2f}%', 
                ha='center', fontsize=9)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()