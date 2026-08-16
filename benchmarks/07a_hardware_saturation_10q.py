"""
Benchmark 07a: Hardware Coherence Wall Mapping (10 Qubits)
Generates Figure 3a from the manuscript: hardware_saturation_10q.pdf
"""

import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Import our O(1) engine from the HALO library
from halo.hamiltonian import build_halo_hamiltonian

def build_circuit(H_qlm, t_evo, reps):
    N = 10
    qc = QuantumCircuit(N)
    # Initialize the 10-Qubit Meson
    qc.x([3, 9, 0, 3, 2]) 
    
    evo_gate = PauliEvolutionGate(H_qlm, time=t_evo, synthesis=LieTrotter(reps=reps))
    qc.append(evo_gate, range(N))
    qc.measure_all()
    return qc

def run_hardware_sweep():
    print("-" * 65)
    print("BENCHMARK 7A: MAPPING THE 10-QUBIT HARDWARE COHERENCE WALL")
    print("-" * 65)
    
    N = 10
    m_bare = 0.506218
    g_bare = 1.012553
    t_evo = 2.0
    
    depth_sweep = [1, 2, 3, 4, 5, 7, 10]
    
    H_qlm = build_halo_hamiltonian(N, g_bare, m_bare, dt=1.0)
    circuits = [build_circuit(H_qlm, t_evo, d) for d in depth_sweep]

    # === HARDWARE CONNECTION ===
    try:
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=10)
        print(f"Hardware Selected: {backend.name}")
    except Exception as e:
        print(f"Cloud connection failed: {e}")
        return

    print("Transpiling circuits...")
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa_circuits = pm.run(circuits)

    print("Executing Depth Sweep on QPU...")
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = 2048 
    
    job = sampler.run(isa_circuits)
    print(f"Job submitted! ID: {job.job_id()}")
    
    result = job.result()
    print("\n--- SWEEP RESULTS ---")
    
    target = '1000000101'
    measured_probs = []
    
    for i, res in enumerate(result):
        try:
            counts = res.data.meas.get_counts()
        except AttributeError:
            counts = list(res.data.values())[0].get_counts()
            
        p = counts.get(target, 0) / sum(counts.values())
        measured_probs.append(p * 100)
        print(f"Trotter Depth {depth_sweep[i]}: {p*100:.3f}%")

    # === PUBLICATION-GRADE PLOTTING ===
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(depth_sweep, measured_probs, marker='o', color='#d62728', linewidth=2.5, label='QPU Raw Output')
    plt.axhline(y=10.2282, color='#1f77b4', linestyle='--', linewidth=2, label='Exact Analytical Truth (10.22%)')
    plt.axhline(y=(1/1024)*100, color='gray', linestyle='-.', alpha=0.5, label='Random Noise Floor (0.09%)')
    
    plt.title("Hardware Saturation Sweep: QLM Coherence vs. Circuit Depth", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Trotter Steps (Circuit Depth)", fontsize=12, fontweight='bold')
    plt.ylabel("Meson Survival Probability (%)", fontsize=12, fontweight='bold')
    plt.xticks(depth_sweep)
    plt.legend(fontsize=11, framealpha=1.0, edgecolor='black')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    # Absolute Path Saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    
    os.makedirs(figures_dir, exist_ok=True) 
    save_path = os.path.join(figures_dir, 'hardware_saturation_10q.pdf')
    
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"\n[+] Plot generated successfully:\n    {save_path}")

if __name__ == "__main__":
    run_hardware_sweep()
