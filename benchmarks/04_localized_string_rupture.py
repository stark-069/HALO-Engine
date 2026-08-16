"""
Benchmark 04: Real-Time Localized String Rupture Dynamics (16 Qubits)
Generates Figures 5 and 6 from the manuscript:
  - phase2_string_breaking_high_res.pdf (t = 0.790 crossover)
  - phase2_dynamics_g5.pdf (g = 5 deep confinement oscillations)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import scipy.sparse.linalg as spla

# Import the core QLM matrix builder from the HALO library
from halo.hamiltonian import build_halo_hamiltonian

def simulate_localized_string_rupture(g_bare=1.012553, m_bare=0.506218, output_filename='phase2_string_breaking_high_res.pdf'):
    print("-" * 65)
    print(f"BENCHMARK 4: LOCALIZED STRING RUPTURE DYNAMICS (16 QUBITS, g = {g_bare})")
    print("-" * 65)

    N = 16
    time_steps = np.linspace(0, 3.0, 500)
    survival_probs = []
    breaking_probs = []

    print("Building 16-Qubit Hamiltonian Matrix...")
    H_qlm = build_halo_hamiltonian(N, g_bare, m_bare, dt=1.0)
    H_matrix = H_qlm.to_matrix(sparse=True)

    # Staggered Vacuum & Stretched Meson State
    qc_init = QuantumCircuit(N)
    qc_init.x([3, 9, 15]) # Dirac Vacuum
    qc_init.x([3, 12])    # Heavy Meson Stretched
    qc_init.x([4, 7, 10]) # Negative Flux Field

    initial_sv = Statevector(qc_init)
    psi_0 = initial_sv.data
    initial_bitstring = list(initial_sv.probabilities_dict().keys())[0]

    print(f"Tracking Original Heavy Meson State: |{initial_bitstring}⟩")
    print("Executing Real-Time Dynamics (500 Steps)...")

    for t in time_steps:
        if t == 0:
            psi_t = psi_0
        else:
            psi_t = spla.expm_multiply(-1j * t * H_matrix, psi_0)

        probs = Statevector(psi_t).probabilities_dict(decimals=6)
        survival_probs.append(probs.get(initial_bitstring, 0.0) * 100)

        broken_prob = 0.0
        for state, p in probs.items():
            if state[7] == '0' and state[8] == '0' and state != initial_bitstring:
                broken_prob += p
        breaking_probs.append(broken_prob * 100)

    surv_arr = np.array(survival_probs)
    brk_arr = np.array(breaking_probs)

    # Plotting
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(11, 7), dpi=300)

    plt.plot(time_steps, surv_arr, label='Original Heavy Meson (Survival)', color='#d62728', linewidth=2.5)
    plt.plot(time_steps, brk_arr, label='Broken String (Two Light Mesons)', color='#1f77b4', linewidth=2.5)

    # Locate Intersection
    cross_indices = np.argwhere(np.diff(np.sign(surv_arr - brk_arr))).flatten()
    if len(cross_indices) > 0:
        cross_idx = cross_indices[0]
        t1, t2 = time_steps[cross_idx], time_steps[cross_idx+1]
        y1_s, y2_s = surv_arr[cross_idx], surv_arr[cross_idx+1]
        y1_b, y2_b = brk_arr[cross_idx], brk_arr[cross_idx+1]

        slope_s = (y2_s - y1_s) / (t2 - t1)
        slope_b = (y2_b - y1_b) / (t2 - t1)

        t_int = t1 + (y1_s - y1_b) / (slope_b - slope_s)
        p_int = y1_s + slope_s * (t_int - t1)

        print(f"\n[+] Localized String Rupture Point: t = {t_int:.6f}, P = {p_int:.6f}%")

        plt.scatter([t_int], [p_int], color='black', s=80, zorder=5, label='Phase Transition Point')
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1.5, alpha=0.9)
        plt.annotate(f"Intersection:\nt = {t_int:.3f}\nP = {p_int:.2f}%", 
                     (t_int, p_int), textcoords="offset points", xytext=(15, 15), 
                     ha='left', fontsize=11, fontweight='bold', bbox=bbox_props)
        plt.fill_between(time_steps, brk_arr, surv_arr, where=(brk_arr > surv_arr), color='#1f77b4', alpha=0.1)
    else:
        print("\n[+] Deep Confinement: Rigid Flux Tube Oscillations (No Rupture).")

    plt.title(f"HALO Engine: Localized Pair Creation via Quantum Quench (g = {g_bare})", fontsize=14, fontweight='bold')
    plt.xlabel("Time Evolution (Lattice Units)", fontsize=12)
    plt.ylabel("Quantum State Probability (%)", fontsize=12)
    plt.minorticks_on()
    plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.7)
    plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)
    plt.legend(fontsize=11, loc='upper right')
    plt.tight_layout()

    # Save to figures/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    save_path = os.path.join(figures_dir, output_filename)

    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"[+] Output figure saved to:\n    {save_path}\n")

if __name__ == "__main__":
    # 1. Generate High-Resolution Localized String Rupture (Figure 5)
    simulate_localized_string_rupture(g_bare=1.012553, output_filename='phase2_string_breaking_high_res.pdf')
    # 2. Generate Deep Confinement Limit Dynamics (Figure 6)
    simulate_localized_string_rupture(g_bare=5.0, output_filename='phase2_dynamics_g5.pdf')