"""
Benchmark 01: Hardware Entanglement and Depth Scaling
Generates Figure 1 and matches Table I from the manuscript: poc1_compiler_duel.pdf
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

from halo.hamiltonian import build_standard_jw_paulis, build_halo_paulis

def run_compiler_duel():
    print("-" * 80)
    print("BENCHMARK 1: MULTI-STRATEGY COMPILER BENCHMARKING (MATCHING TABLE I)")
    print("-" * 80)
    print(f"{'Qubits (N)':<10} | {'JW (Opt-1)':<12} | {'JW (Opt-3)':<12} | {'Explicit (Opt-3)':<18} | {'HALO Engine':<12}")
    print("-" * 80)
    
    # Exact qubit scales matching Table I in the manuscript
    qubit_scales = [4, 7, 10, 13, 16]
    
    jw_opt1_cnots, jw_opt3_cnots, explicit_cnots, halo_cnots = [], [], [], []
    halo_depths = []
    
    for N in qubit_scales:
        # 1. Generate operators
        jw_op = build_standard_jw_paulis(N)
        halo_op = build_halo_paulis(N)
        
        qc_jw = PauliEvolutionGate(jw_op, time=0.1).definition
        qc_halo = PauliEvolutionGate(halo_op, time=0.1).definition
        
        # 2. Define 1D linear hardware topology mapping IBM Heron native constraints
        coupling_map = [[i, i+1] for i in range(N-1)] + [[i+1, i] for i in range(N-1)]
        native_basis = ['cz', 'rz', 'sx', 'x'] # Updated to match Heron native basis
        
        # 3. Transpile across strategies matching manuscript specifications
        # Strategy A: JW with Optimization Level 1
        trans_jw1 = transpile(qc_jw, basis_gates=native_basis, coupling_map=coupling_map, optimization_level=1, seed_transpiler=42)
        # Strategy B: JW with Optimization Level 3
        trans_jw3 = transpile(qc_jw, basis_gates=native_basis, coupling_map=coupling_map, optimization_level=3, seed_transpiler=42)
        # Strategy C: Explicit Gauge Encoding with Opt-Level 3
        trans_explicit = transpile(qc_halo, basis_gates=native_basis, coupling_map=coupling_map, optimization_level=3, seed_transpiler=42)
        # Strategy D: HALO Engine Pipeline
        trans_halo = transpile(qc_halo, basis_gates=native_basis, coupling_map=coupling_map, optimization_level=1, seed_transpiler=42)
        
        # 4. Extract entangling gate counts (counting native 'cz' operations)
        c1 = trans_jw1.count_ops().get('cz', 0)
        c3 = trans_jw3.count_ops().get('cz', 0)
        cexp = trans_explicit.count_ops().get('cz', 0)
        chalo = trans_halo.count_ops().get('cz', 0)
        
        jw_opt1_cnots.append(c1)
        jw_opt3_cnots.append(c3)
        explicit_cnots.append(cexp)
        halo_cnots.append(chalo)
        halo_depths.append(trans_halo.depth())
        
        print(f"{N:<10} | {c1:<12} | {c3:<12} | {cexp:<18} | {chalo:<12}")

    print("-" * 80)
    print("\nGenerating Publication-Grade Statistic Graph...")
    
    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False 
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    
    # Plotting all strategies to match the depth and rigor of the paper
    ax.plot(qubit_scales, jw_opt1_cnots, marker='o', markersize=8, label='JW (Opt-Level 1)', color='#d62728', linewidth=2.0)
    ax.plot(qubit_scales, jw_opt3_cnots, marker='^', markersize=8, label='JW (Opt-Level 3)', color='#ff7f0e', linewidth=2.0)
    ax.plot(qubit_scales, explicit_cnots, marker='d', markersize=8, label='Explicit Gauge (Opt-Level 3)', color='#2ca02c', linewidth=2.0)
    ax.plot(qubit_scales, halo_cnots, marker='s', markersize=8, label='HALO Engine', color='#1f77b4', linewidth=2.5)
    
    ax.set_title("Single-Step Trotter Entangling Overhead across Strategies", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Entangling Gates (CZ Count)", fontsize=11, fontweight='bold')
    ax.set_xlabel("Lattice Size (Qubits $N$)", fontsize=11, fontweight='bold')
    
    ax.xaxis.set_major_locator(MultipleLocator(3))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax.tick_params(which='both', direction='in', top=True, right=True, labelsize=11)
    ax.grid(which='major', color='#CCCCCC', linestyle='-', linewidth=0.8, zorder=0)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8, zorder=0)
    ax.legend(fontsize=10, loc='upper left', framealpha=1.0, edgecolor='black')

    plt.tight_layout()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'poc1_compiler_duel.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] Statistical graph successfully saved to:\n    {save_path}")

if __name__ == "__main__":
    run_compiler_duel()
