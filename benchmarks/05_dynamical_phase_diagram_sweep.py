"""
Benchmark 05: Dynamical Phase Diagram Sweep (16 Qubits)
Generates Figure 7 from the manuscript: phase2_PRL_g_sweep.pdf
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import scipy.sparse.linalg as spla

# Import the core QLM matrix builder from the HALO library
from halo.hamiltonian import build_halo_hamiltonian

def run_coupling_sweep():
    print("-" * 65)
    print("BENCHMARK 5: CONTINUOUS COUPLING (g) SWEEP AT t=0.8")
    print("-" * 65)
    
    N = 16
    m_bare = 0.506218
    target_time = 0.8
    
    # Sweep g from 0.1 (Free Fermions) to 5.0 (Rigid String)
    g_values = np.linspace(0.1, 5.0, 50)
    survival_probs = []
    breaking_probs = []
    
    qc_init = QuantumCircuit(N)
    qc_init.x([3, 9, 15]) # Vacuum
    qc_init.x([3, 12])    # Meson
    qc_init.x([4, 7, 10]) # Flux Tube
    
    initial_sv = Statevector(qc_init)
    psi_0 = initial_sv.data
    initial_bitstring = list(initial_sv.probabilities_dict().keys())[0]

    print(f"Scanning {len(g_values)} coupling constants. Generating Dynamical Phase Diagram...")

    for g in g_values:
        H_qlm = build_halo_hamiltonian(N, g, m_bare, dt=1.0)
        H_matrix = H_qlm.to_matrix(sparse=True)
        
        # Exact evolution to t=0.8
        psi_t = spla.expm_multiply(-1j * target_time * H_matrix, psi_0)
        probs = Statevector(psi_t).probabilities_dict(decimals=6)
        
        survival_probs.append(probs.get(initial_bitstring, 0.0) * 100)
        
        broken_prob = 0.0
        for state, p in probs.items():
            if state[7] == '0' and state[8] == '0' and state != initial_bitstring:
                broken_prob += p
        breaking_probs.append(broken_prob * 100)

    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    ax.plot(g_values, survival_probs, label='Heavy Meson Survival', color='#d62728', linewidth=2.5, zorder=3)
    ax.plot(g_values, breaking_probs, label='Broken String (Tracker Output)', color='#1f77b4', linewidth=2.5, zorder=3)
    
    # Annotating the physics regimes
    ax.axvline(x=1.01, color='k', linestyle='--', alpha=0.6, zorder=4)
    ax.text(1.05, 80, 'Non-Perturbative\nLocalized String Rupture', fontsize=11, style='italic', fontfamily='serif', zorder=5)
    
    ax.axvspan(0.1, 0.5, color='gray', alpha=0.1, zorder=1)
    ax.text(0.15, 80, 'Kinetic Dispersion\n(Free Fermions)', fontsize=11, style='italic', fontfamily='serif', zorder=5)

    # --- HIGH-RESOLUTION GRID STYLING ---
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(MultipleLocator(0.1)) 
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=11)
    ax.tick_params(which='major', length=6, width=1.2)
    ax.tick_params(which='minor', length=3, width=0.8)

    ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=0.8, zorder=0)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8, zorder=0)

    ax.set_title(f"Dynamical Phase Diagram of the Schwinger Model at $t={target_time}$", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Coupling Constant (g)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Probability (%)", fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 5.1)
    ax.set_ylim(-2, 102)
    ax.legend(loc='center right', fontsize=11, framealpha=1.0, edgecolor='black', fancybox=False)
    
    plt.tight_layout()
    
    # Absolute Path Saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'phase2_PRL_g_sweep.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] Dynamical Phase Diagram generated:\n    {save_path}")

if __name__ == "__main__":
    run_coupling_sweep()