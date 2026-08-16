"""
Benchmark 02: Variational Ground State Preparation (8 Qubits)
Generates Figure 2 from the manuscript.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from qiskit.circuit.library import real_amplitudes
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize
import scipy.sparse.linalg as spla

# Import the exact matrix generator from our clean HALO library
from halo.hamiltonian import build_halo_paulis

def run_halo_vqe():
    print("-" * 65)
    print("BENCHMARK 2: VQE INTERACTING VACUUM STATE (HALO ENGINE)")
    print("-" * 65)
    
    N = 8  
    H_op = build_halo_paulis(N)
    
    print("1. Calculating Exact Analytical Ground State...")
    H_matrix = H_op.to_matrix(sparse=True)
    exact_energy, _ = spla.eigsh(H_matrix, k=1, which='SA')
    exact_energy = exact_energy[0]
    print(f"   Exact Vacuum Energy: {exact_energy:.6f}")

    print("2. Constructing Quantum Ansatz...")
    ansatz = real_amplitudes(num_qubits=N, reps=5)
    
    estimator = StatevectorEstimator()
    iteration_energies = []
    
    def cost_function(theta):
        pub = (ansatz, H_op, theta)
        job = estimator.run([pub])
        energy = float(job.result()[0].data.evs)
        
        iteration_energies.append(energy)
        if len(iteration_energies) % 10 == 0:
            print(f"   Iteration {len(iteration_energies):<3} | Current Energy: {energy:.6f}")
            
        return energy

    np.random.seed(42)
    initial_theta = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
    
    print("3. Executing Quantum Machine Learning Optimization Loop...")
    result = minimize(cost_function, initial_theta, method='COBYLA', options={'maxiter': 1900})
    
    print("\n--- OPTIMIZATION COMPLETE ---")
    print(f"Final VQE Energy:   {result.fun:.6f}")
    print(f"Exact Truth Energy: {exact_energy:.6f}")
    error_margin = abs((result.fun - exact_energy) / exact_energy) * 100
    print(f"Convergence Error:  {error_margin:.3f}%\n")
    
    print("Generating Publication-Grade Convergence Plot...")
    
    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    iterations = range(1, len(iteration_energies) + 1)
    
    ax.plot(iterations, iteration_energies, marker='o', markersize=3, linestyle='-', 
            label='VQE Optimization Trajectory', color='#1f77b4', linewidth=1.5, zorder=3)
    
    # Terminology explicitly corrected to "Exact Analytical Ground State"
    ax.axhline(y=exact_energy, color='#d62728', linestyle='--', linewidth=2.5, 
               label=f'Exact Analytical Ground State ($E_0 = {exact_energy:.3f}$)', zorder=2)
    
    ax.xaxis.set_major_locator(MultipleLocator(250))
    ax.xaxis.set_minor_locator(MultipleLocator(50)) 
    
    ax.yaxis.set_major_locator(MultipleLocator(2.0))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=11)
    ax.tick_params(which='major', length=6, width=1.2)
    ax.tick_params(which='minor', length=3, width=0.8)

    ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=0.8, zorder=0)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8, zorder=0)

    ax.set_title("HALO Engine: Variational Ground State Preparation (8 Qubits)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Optimizer Iterations", fontsize=12, fontweight='bold')
    ax.set_ylabel("Expectation Value (Energy)", fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, len(iteration_energies) + 50)
    ax.legend(loc='upper right', fontsize=11, framealpha=1.0, edgecolor='black', fancybox=False)
    
    plt.tight_layout()
    
    # OS-Independent Absolute Path Saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'poc2_vqe_convergence_fixed.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"[+] Fixed convergence graph successfully saved to:\n    {save_path}")

if __name__ == "__main__":
    run_halo_vqe()