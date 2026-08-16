"""
Compilation and architectural blueprints for the HALO Engine.
"""

from qiskit import QuantumCircuit, QuantumRegister

def build_2d_unit_cell_circuit():
    """
    Generates the 2D Scaled Unit Cell Architecture for four-local magnetic plaquette interactions.
    Demonstrates the O(1) concurrent routing blueprint.
    
    Returns:
        QuantumCircuit: The synthesized 2D unit cell circuit.
    """
    # 4 Vertices (Matter) and 4 Links (Gauge)
    qr_m = QuantumRegister(4, 'matter')
    qr_g = QuantumRegister(4, 'gauge')
    qc = QuantumCircuit(qr_m, qr_g)
    
    # 1. THE ELECTRIC FIELD (Local terms)
    # Z-rotations on all gauge links
    for i in range(4):
        qc.rz(0.1, qr_g[i])
    qc.barrier()
    
    # 2. THE KINETIC HOPPING (Matter-Gauge-Matter interactions)
    # Horizontal hopping on the top edge (Matter 0 -> Gauge 0 -> Matter 1)
    qc.h(qr_m[0])
    qc.h(qr_m[1])
    qc.cx(qr_m[0], qr_g[0])
    qc.cx(qr_m[1], qr_g[0])
    qc.rz(0.2, qr_g[0])
    qc.cx(qr_m[1], qr_g[0])
    qc.cx(qr_m[0], qr_g[0])
    qc.h(qr_m[0])
    qc.h(qr_m[1])
    
    # Vertical hopping on the left edge (Matter 0 -> Gauge 3 -> Matter 2)
    qc.h(qr_m[0])
    qc.h(qr_m[2])
    qc.cx(qr_m[0], qr_g[3])
    qc.cx(qr_m[2], qr_g[3])
    qc.rz(0.2, qr_g[3])
    qc.cx(qr_m[2], qr_g[3])
    qc.cx(qr_m[0], qr_g[3])
    qc.h(qr_m[0])
    qc.h(qr_m[2])
    
    qc.barrier()
    
    # 3. THE MAGNETIC PLAQUETTE (4-Body Gauge Interaction)
    qc.h(qr_g)
    qc.cx(qr_g[0], qr_g[1])
    qc.cx(qr_g[1], qr_g[2])
    qc.cx(qr_g[2], qr_g[3])
    
    qc.rz(0.15, qr_g[3]) # Magnetic Flux Phase
    
    qc.cx(qr_g[2], qr_g[3])
    qc.cx(qr_g[1], qr_g[2])
    qc.cx(qr_g[0], qr_g[1])
    qc.h(qr_g)
    
    return qc