"""
Variational Quantum Eigensolver (VQE) modules for the HALO Engine.
Prepares the interacting vacuum state using a localized physics-informed ansatz.
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

def build_halo_vqe_ansatz(num_qubits, reps=4):
    """
    Constructs a moderate-depth, physics-informed parameterized ansatz for 
    interacting vacuum state preparation.
    
    Args:
        num_qubits (int): Total number of lattice qubits.
        reps (int): Depth of the parameterized blocks.
        
    Returns:
        QuantumCircuit: The parameterized HALO-VQE circuit.
    """
    qc = QuantumCircuit(num_qubits)
    num_links = (num_qubits - 1) // 3
    
    theta_ry = ParameterVector('θ_ry', num_qubits * reps)
    theta_E = ParameterVector('θ_E', num_links * reps)
    theta_K = ParameterVector('θ_K', num_links * reps)
    
    p_ry, p_E, p_K = 0, 0, 0
    
    for r in range(reps):
        # 1. Single-qubit rotations
        for q in range(num_qubits):
            qc.ry(theta_ry[p_ry], q)
            p_ry += 1
            
        # 2. Electric Field (String Tension) interactions
        for l in range(num_links):
            q_L, q_R = 3*l + 1, 3*l + 2
            qc.rzz(theta_E[p_E], q_L, q_R)
            p_E += 1
            
        # 3. Kinetic Hopping (Matter-Gauge-Matter) localized routing
        for n in range(num_links):
            f_A, q_R, q_L, f_B = 3*n, 3*n+1, 3*n+2, 3*n+3
            
            qc.h([f_A, f_B])
            qc.cx(f_A, q_L)
            qc.cx(f_B, q_R)
            
            qc.rz(theta_K[p_K], q_L)
            qc.rz(theta_K[p_K], q_R)
            
            qc.cx(f_B, q_R)
            qc.cx(f_A, q_L)
            qc.h([f_A, f_B])
            
            p_K += 1
            
    return qc