"""
Benchmark 07b: Hardware Coherence Wall Mapping (16 Qubits)
Generates Figure 3b from the manuscript: hardware_saturation_16q.pdf
"""

import os
import numpy as np
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.quantum_info import Statevector

# Import our O(1) engine from the HALO library
from halo.hamiltonian import build_halo_hamiltonian

def build_16q_circuit(H_qlm, t_evo, reps):
    N = 16
    qc = QuantumCircuit(N)
    qc.x([3, 9, 15]) # Vacuum
    qc.x([3, 12])    # Meson
    qc.x([4, 7, 10]) # Flux Tube
    
    evo_gate = PauliEvolutionGate(H_qlm, time=t_evo, synthesis=LieTrotter(reps=reps))
    qc.append(evo_gate, range(N))
    qc.measure_all()
    return qc

def get_exact_target(H_qlm, t_evo):
    N = 16
    qc_init = QuantumCircuit(N)
    qc_init.x([3, 9, 15]) 
    qc_init.x([3, 12])    
    qc_init.x([4, 7, 10]) 
    
    initial_sv = Statevector(qc_init)
    psi_0 = initial_sv.data
    initial_bitstring = list(initial_sv.probabilities_dict().keys())[0]
    
    H_matrix = H_qlm.to_matrix(sparse=True)
    psi_t = spla.expm_multiply(-1j * t_evo * H_matrix, psi_0)
    
    probs = Statevector(psi_t).probabilities_dict(decimals=6)
    exact_survival = probs.get(initial_bitstring, 0) * 100
    
    return initial_bitstring, exact_survival

def run_16q_hardware_sweep():
    print("-" * 65)
    print("BENCHMARK 7B: MAPPING THE 16-QUBIT HARDWARE COHERENCE WALL")
    print("-" * 65)
    
    N = 16
    m_bare = 0.506218
    g_bare = 1.012553
    t_evo = 0.8  # Critical crossover point
    depth_sweep = [1, 2, 3, 4, 5, 7]
    
    print("Building 16-Qubit Hamiltonian...")
    H_qlm = build_halo_hamiltonian(N, g_bare, m_bare, dt=1.0)
    
    print("Calculating Exact Analytical Target...")
    target_bitstring, exact_truth = get_exact_target(H_qlm, t_evo)
    
    circuits = [build_16q_circuit(H_qlm, t_evo, d) for d in depth_sweep]

    # === HARDWARE CONNECTION ===
    try:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=16)
        print(f"Hardware Selected: {backend.name}")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] IBM Cloud connection failed: {e}")
        return

    print("Transpiling circuits...")
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa_circuits = pm.run(circuits)

    print("Executing Depth Sweep on QPU...")
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = 4096 
    
    job = sampler.run(isa_circuits)
    result = job.result()
    
    measured_probs = []
    for i, res in enumerate(result):
        try:
            counts = res.data.meas.get_counts()
        except AttributeError:
            counts = list(res.data.values())[0].get_counts()
            
        p = counts.get(target_bitstring, 0) / sum(counts.values())
        measured_probs.append(p * 100)

    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    noise_floor = (1 / 65536) * 100
    
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(depth_sweep, measured_probs, marker='o', color='#d62728', linewidth=2.5, label=f'QPU Raw Output ({backend.name})')
    plt.axhline(y=exact_truth, color='#1f77b4', linestyle='--', linewidth=2, label=f'Exact Analytical Truth ({exact_truth:.2f}%)')
    plt.axhline(y=noise_floor, color='gray', linestyle='-.', alpha=0.5, label='Random Noise Floor (0.0015%)')
    
    plt.title(f"Hardware Saturation Sweep: 16-Qubit Localized String Rupture (t={t_evo})", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Trotter Steps (Circuit Depth)", fontsize=12, fontweight='bold')
    plt.ylabel("Heavy Meson Survival Probability (%)", fontsize=12, fontweight='bold')
    plt.xticks(depth_sweep)
    plt.legend(fontsize=11, framealpha=1.0, edgecolor='black')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'hardware_saturation_16q.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] Plot generated successfully:\n    {save_path}")

if __name__ == "__main__":
    run_16q_hardware_sweep()

