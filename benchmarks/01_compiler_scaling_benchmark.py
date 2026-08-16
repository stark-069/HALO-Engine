"""
Benchmark 01: Hardware Entanglement and Depth Scaling
Generates Figure 1 from the manuscript: poc1_compiler_duel.pdf
"""

import sys
import os

# Point Python to the project root so it recognizes the 'halo' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from qiskit.circuit.library import PauliEvolutionGate
from qiskit import transpile

# Now this will import perfectly without IDE warnings
from halo.hamiltonian import build_standard_jw_paulis, build_halo_paulis

def run_compiler_duel():
    print("-" * 65)
    print("BENCHMARK 1: JORDAN-WIGNER VS. HALO ENGINE COMPILER SCALING")
    print("-" * 65)
    print(f"{'Qubits (N)':<12} | {'JW CNOTs':<10} | {'HALO CNOTs':<12} | {'Reduction (%)':<15}")
    print("-" * 65)
    
    # Qubit scales to test (From small prototypes up to the 16-qubit limit)
    qubit_scales = [4, 6, 8, 10, 12, 14, 16]
    
    jw_cnots, halo_cnots = [], []
    jw_depths, halo_depths = [], []
    
    for N in qubit_scales:
        # 1. Generate the Hamiltonian operators via the core library
        jw_op = build_standard_jw_paulis(N)
        halo_op = build_halo_paulis(N)
        
        # 2. Convert to Time Evolution circuits (1 Trotter Step)
        qc_jw = PauliEvolutionGate(jw_op, time=0.1).definition
        qc_halo = PauliEvolutionGate(halo_op, time=0.1).definition
        
        # 3. Simulate physical IBM hardware constraints (Linear nearest-neighbor topology)
        coupling_map = [[i, i+1] for i in range(N-1)] + [[i+1, i] for i in range(N-1)]
        
        # 4. Transpile to hardware native gates
        trans_jw = transpile(qc_jw, basis_gates=['cx', 'rz', 'sx', 'x'], 
                             coupling_map=coupling_map, optimization_level=1, seed_transpiler=42)
        trans_halo = transpile(qc_halo, basis_gates=['cx', 'rz', 'sx', 'x'], 
                               coupling_map=coupling_map, optimization_level=1, seed_transpiler=42)
        
        # 5. Extract metrics
        cnot_jw = trans_jw.count_ops().get('cx', 0)
        cnot_halo = trans_halo.count_ops().get('cx', 0)
        
        jw_cnots.append(cnot_jw)
        halo_cnots.append(cnot_halo)
        jw_depths.append(trans_jw.depth())
        halo_depths.append(trans_halo.depth())
        
        reduction = ((cnot_jw - cnot_halo) / cnot_jw) * 100
        print(f"{N:<12} | {cnot_jw:<10} | {cnot_halo:<12} | {reduction:.2f}%")

    print("-" * 65)
    print("\nGenerating Publication-Grade Statistic Graph...")
    
    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False # Ensures minus signs render correctly
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # Plot 1: Total CNOT Count
    ax1.plot(qubit_scales, jw_cnots, marker='o', markersize=8, label='Standard Jordan-Wigner', color='#d62728', linewidth=2.5)
    ax1.plot(qubit_scales, halo_cnots, marker='s', markersize=8, label='HALO Engine Pipeline', color='#1f77b4', linewidth=2.5)
    
    ax1.set_title("Hardware Entanglement Overhead per Step", fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel("Total CNOT Gates", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Lattice Size (Qubits)", fontsize=12, fontweight='bold')
    
    # Plot 2: Total Circuit Depth
    ax2.plot(qubit_scales, jw_depths, marker='o', markersize=8, label='Standard Jordan-Wigner', color='#d62728', linewidth=2.5)
    ax2.plot(qubit_scales, halo_depths, marker='s', markersize=8, label='HALO Engine Pipeline', color='#1f77b4', linewidth=2.5)
    
    ax2.set_title("Quantum Circuit Depth per Step", fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel("Critical Path Depth", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Lattice Size (Qubits)", fontsize=12, fontweight='bold')

    # Universal Styling for both axes
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_locator(MultipleLocator(2))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        
        ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=11)
        ax.tick_params(which='major', length=6, width=1.2)
        ax.tick_params(which='minor', length=3, width=0.8)
        
        ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=0.8, zorder=0)
        ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8, zorder=0)
        ax.legend(fontsize=11, loc='upper left', framealpha=1.0, edgecolor='black')

    plt.tight_layout()
    
    # 1. Get the absolute path of the 'benchmarks' folder where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go one level up to your main project folder ('Prototype_2') and create 'figures'
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'poc1_compiler_duel.pdf')
    
    # 3. Save the file securely
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] Statistical graph successfully saved to:\n    {save_path}")

if __name__ == "__main__":
    run_compiler_duel()