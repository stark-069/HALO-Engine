"""
Benchmark 06: HALO-VQE 20-Qubit Algorithmic Recovery vs QPU Execution
Generates Figure 8 from the manuscript: phase3_comparative_vqe_20q.pdf
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import make_interp_spline

def generate_publication_plot():
    print("-" * 65)
    print("BENCHMARK 6: 20-QUBIT VQE (SIMULATION VS QPU DEPOLARIZATION)")
    print("-" * 65)
    
    # 1. EXACT DATA FROM YOUR RUNS
    exact_energy = -23.822429

    # IBM Hardware Data (20 Iterations, Depth-2 on ibm_marrakesh)
    hw_energies = [
        0.643003, 3.323992, 2.841006, 1.442035, 1.385219, 2.971473, 
        1.913103, 2.632825, 2.431676, 2.020163, 2.081212, 2.194311, 
        2.932714, 1.347103, 2.714326, 1.918802, 1.686099, 2.600734, 
        2.472741, 1.920477
    ]

    # Simulator Data Checkpoints (Depth-4, L-BFGS-B, 1000 Iterations)
    sim_checkpoints_x = np.array([1, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    sim_checkpoints_y = np.array([0.0, -9.866532, -14.245871, -16.571171, -18.878885, 
                                  -18.868842, -19.505153, -20.267844, -20.793700, 
                                  -21.147119, -21.299071])

    # Interpolate simulator checkpoints for a perfectly smooth vector curve
    spline = make_interp_spline(sim_checkpoints_x, sim_checkpoints_y, k=3)
    x_sim_smooth = np.linspace(1, 1000, 500)
    y_sim_smooth = spline(x_sim_smooth)

    # 2. PLOTTING
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    
    # Exact Analytical Baseline
    ax.axhline(y=exact_energy, color='#2ca02c', linestyle='--', linewidth=2.5, 
               label=f'Exact Analytical Ground State ($E_0 = {exact_energy:.2f}$)', zorder=1)
    
    # Local Simulator (Depth-4)
    ax.plot(x_sim_smooth, y_sim_smooth, color='#1f77b4', linewidth=2.5, 
            label=r'Ideal HALO-VQE (Depth-4, $E \approx -21.30$)', zorder=2)
            
    # IBM Hardware (Scaled across the X-axis for direct visual comparison)
    x_hw_scaled = np.linspace(1, 1000, len(hw_energies))
    ax.plot(x_hw_scaled, hw_energies, marker='o', markersize=6, 
            color='#d62728', linewidth=2, alpha=0.85, 
            label='Physical QPU Execution (ibm_marrakesh, Depth-2)', zorder=3)

    # 3. STYLING & FORMATTING
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=11)
    ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=0.8, zorder=0)

    ax.set_title("HALO Engine: Algorithmic Recovery vs. Hardware Decoherence (20 Qubits)", 
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Effective Optimizer Evaluations (Scaled)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Expectation Value (Energy)", fontsize=13, fontweight='bold')
    
    ax.set_xlim(0, 1050)
    ax.legend(loc='center right', fontsize=12, framealpha=1.0, edgecolor='black', fancybox=False)
    
    plt.tight_layout()
    
    # Absolute Path Saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'phase3_comparative_vqe_20q.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] 20-Qubit VQE graph successfully saved to:\n    {save_path}")

if __name__ == "__main__":
    generate_publication_plot()