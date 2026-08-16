"""
Core Hamiltonian generation modules for the HALO Engine.
Constructs Quantum Link Model (QLM) operators for Lattice Gauge Theories.
"""

from qiskit.quantum_info import SparsePauliOp

def build_halo_hamiltonian(num_qubits, g_coupling, mass, dt):
    """
    Constructs the Universal O(1) QLM Engine Hamiltonian.
    Maintains exact Gauss's Law symmetries while enabling localized string rupture dynamics.
    
    Args:
        num_qubits (int): Total number of physical qubits (must be 3*L + 1).
        g_coupling (float): The bare coupling constant (g).
        mass (float): The bare fermion mass.
        dt (float): Time step precision.
        
    Returns:
        SparsePauliOp: The evaluated Hamiltonian matrix.
    """
    if (num_qubits - 1) % 3 != 0:
        raise ValueError("Invalid number of qubits! Must be 3*L + 1 to support composite links.")
        
    num_links = (num_qubits - 1) // 3
    num_fermions = num_links + 1
    pauli_list = []
    
    def make_pauli_string(ops_dict):
        string = ['I'] * num_qubits
        for idx, op in ops_dict.items():
            string[num_qubits - 1 - idx] = op 
        return "".join(string)

    # 1. Mass Matrix (Staggered Fermions)
    for n in range(num_fermions):
        sign = (-1)**n  
        pauli_list.append((make_pauli_string({3 * n: 'Z'}), mass * sign * dt))
        
    # 2. Electric Field (String Tension)
    for l in range(num_links):
        q_R, q_L = 3 * l + 1, 3 * l + 2
        pauli_list.append((make_pauli_string({q_R: 'Z', q_L: 'Z'}), -0.25 * (g_coupling**2) * 0.5 * dt))

    # 3. Kinetic Hopping (Matter-Gauge-Matter)
    for n in range(num_links):
        f_A, q_R, q_L, f_B = 3 * n, 3 * n + 1, 3 * n + 2, 3 * n + 3      
        hop_1 = make_pauli_string({f_A: 'X', q_L: 'I', q_R: 'X', f_B: 'X'})
        hop_2 = make_pauli_string({f_A: 'Y', q_L: 'Z', q_R: 'Y', f_B: 'Y'})
        pauli_list.append((hop_1, 0.5 * dt))
        pauli_list.append((hop_2, 0.5 * dt))

    return SparsePauliOp.from_list(pauli_list)


def build_standard_jw_paulis(num_qubits):
    """
    Simulates the standard Jordan-Wigner formulation of the Schwinger Model.
    Produces the O(N^2) depth-scaling bottleneck due to all-to-all Coulomb interactions.
    Used exclusively for compiler benchmarking.
    """
    paulis = []
    # All-to-all Coulomb Interaction (Depth-scaling bottleneck)
    for i in range(num_qubits):
        for j in range(i+1, num_qubits):
            op = ['I'] * num_qubits
            op[i], op[j] = 'Z', 'Z'
            paulis.append(("".join(op[::-1]), 1.0))
            
    # Nearest-neighbor kinetic hopping
    for i in range(num_qubits-1):
        op1, op2 = ['I'] * num_qubits, ['I'] * num_qubits
        op1[i], op1[i+1] = 'X', 'X'
        op2[i], op2[i+1] = 'Y', 'Y'
        paulis.append(("".join(op1[::-1]), 1.0))
        paulis.append(("".join(op2[::-1]), 1.0))
        
    return SparsePauliOp.from_list(paulis)


def build_halo_paulis(num_qubits):
    """
    Simplified pure-Pauli generator for the HALO engine.
    Maintains gauge links to ensure purely localized 3-body interactions.
    """
    paulis = []
    # Local Gauge field energy
    for i in range(num_qubits):
        op = ['I'] * num_qubits
        op[i] = 'Z'
        paulis.append(("".join(op[::-1]), 1.0))
        
    # Local 3-body Matter-Gauge-Matter kinetic interactions
    for i in range(0, num_qubits-2, 2):
        op1, op2 = ['I'] * num_qubits, ['I'] * num_qubits
        op1[i], op1[i+1], op1[i+2] = 'X', 'Z', 'X'
        op2[i], op2[i+1], op2[i+2] = 'Y', 'Z', 'Y'
        paulis.append(("".join(op1[::-1]), 1.0))
        paulis.append(("".join(op2[::-1]), 1.0))
        
    return SparsePauliOp.from_list(paulis)