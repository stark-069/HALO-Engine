"""
Error mitigation modules for the HALO Engine.
Implements digital unitary folding and Lindblad exponential Zero-Noise Extrapolation (ZNE).
"""

import numpy as np
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def build_folded_circuit(H_qlm, t_evo, reps, scale_factor, num_qubits=10, initial_state_nodes=None):
    """
    Builds a globally folded circuit U (U^dagger U)^n for Zero-Noise Extrapolation.
    
    Args:
        H_qlm (SparsePauliOp): The HALO Hamiltonian.
        t_evo (float): Total time evolution.
        reps (int): Trotter depth.
        scale_factor (int): The noise scaling factor lambda (must be an odd integer: 1, 3, 5...).
        num_qubits (int): Number of qubits in the lattice.
        initial_state_nodes (list): Qubit indices to apply X gates to for state initialization.
        
    Returns:
        QuantumCircuit: The folded quantum circuit ready for measurement.
    """
    if scale_factor % 2 == 0:
        raise ValueError("Scale factor (lambda) must be an odd integer for unitary folding.")

    qc_base = QuantumCircuit(num_qubits)
    
    # 1. State Initialization
    if initial_state_nodes:
        qc_base.x(initial_state_nodes)
    
    # 2. Time Evolution
    evo_gate = PauliEvolutionGate(H_qlm, time=t_evo, synthesis=LieTrotter(reps=reps))
    qc_base.append(evo_gate, range(num_qubits))
    
    # 3. Unitary Folding
    if scale_factor == 1:
        qc_folded = qc_base.copy()
    else:
        qc_folded = qc_base.copy()
        qc_inv = qc_base.inverse()
        # Apply (U^dagger U) n times where n = (lambda - 1) / 2
        for _ in range((scale_factor - 1) // 2):
            qc_folded.compose(qc_inv, inplace=True)
            qc_folded.compose(qc_base, inplace=True)
            
    qc_folded.measure_all()
    return qc_folded


def exp_decay(x, A, k, C):
    """
    Lindblad exponential decay model for ZNE curve fitting.
    """
    return A * np.exp(-k * x) + C


def extrapolate_zero_noise(noise_scales, measured_probs, noise_floor, bounds=([0, 0, 0], [100, 5, 100])):
    """
    Executes the exponential curve fit to extract the zero-noise limit.
    
    Args:
        noise_scales (list): The applied lambda folding factors (e.g., [1, 3, 5]).
        measured_probs (list): The corresponding expectation values from the QPU.
        noise_floor (float): The maximally mixed depolarizing limit (1 / 2^N).
        bounds (tuple): Parameter bounds for [A, k, C].
        
    Returns:
        tuple: (zne_estimate, popt) where popt contains the optimized fit parameters.
    """
    try:
        popt, _ = curve_fit(
            exp_decay, 
            noise_scales, 
            measured_probs, 
            p0=[measured_probs[0], 0.2, noise_floor], 
            bounds=bounds
        )
        zne_estimate = exp_decay(0, *popt)
        return zne_estimate, popt
    except Exception as e:
        print(f"Curve fitting failed: {e}")
        return None, None