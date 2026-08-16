# ⚡ HALO Engine (Hardware-Aware Lattice Optimization)

[![arXiv](https://img.shields.io/badge/arXiv-Pending-b31b1b.svg)](https://arxiv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A highly optimized quantum compiler and simulation framework for observing Lattice Gauge Theories (LGTs) on near-term physical quantum hardware. 

The HALO framework completely bypasses the severe $\mathcal{O}(N)$ circuit depth overheads associated with standard Jordan-Wigner transformations by natively mapping composite gauge links to the hardware topology. By achieving an asymptotic circuit depth of **$\mathcal{O}(1)$ per Trotter step**, this engine enables deep-time quantum simulations and variational ground-state preparation previously inaccessible on noisy processors.

This repository contains the core compiler library and the complete suite of benchmarking scripts used to generate the physics data for the associated publication.

## 🏆 Key Scientific & Algorithmic Achievements

* **Constant-Depth Compilation:** Achieves true $\mathcal{O}(1)$ physical circuit depth per time-evolution step regardless of lattice size, vastly outperforming Jordan-Wigner mappings.
* **16-Qubit Hardware Dynamics:** Successfully simulated the real-time dynamics of heavy meson string breaking on IBM's 16-qubit heavy-hex topologies.
* **Dynamical Phase Diagrams:** Mapped the critical phase transition between the non-perturbative Confinement Regime and the Kinetic Dispersion (Free Fermion) regime.
* **Zero-Noise Extrapolation (ZNE):** Exploited the localized nature of the HALO mapped Pauli strings to achieve a noise scaling factor of $\lambda = 3$ with only a ~2.5x hardware depth penalty, recovering exact continuous-time physics.
* **20-Qubit VQE Convergence:** Validated Variational Quantum Eigensolver (VQE) for interacting vacuum state preparation at an unprecedented scale of 20 qubits.
* **2D Lattice Extensibility:** The native hardware-aware mapping is fundamentally extensible to 2D unit cells, laying the groundwork for higher-dimensional QED and QCD simulations.

## 📊 Visual Benchmarks

### 1. The Compiler Duel: $\mathcal{O}(1)$ vs $\mathcal{O}(N)$ Scaling
By bypassing non-local parity chains, HALO flatlines the critical path depth per Trotter step, allowing infinite scaling of the spatial lattice size without increasing decoherence.
<p align="center">
  <img src="figures/readme_figures/poc1_compiler_duel.png" alt="Compiler Duel: HALO vs Jordan-Wigner" width="600"/>
</p>

### 2. Physical Observation of Localized String Breaking (16-Qubit QLM)
Time-evolution of the Schwinger model tracking the decay of a heavy meson into two localized light mesons (string breaking) across the hardware array.
<p align="center">
  <img src="figures/readme_figures/phase2_string_breaking_high_res_UPDATED.png" alt="16-Qubit String Breaking Dynamics" width="600"/>
</p>

### 3. Native 2D Unit Cell Extensibility
Unlike 1D string-to-qubit mappings, the HALO framework's localized composite links natively map to 2D planar hardware topologies, paving the way for higher-dimensional gauge theories.
<p align="center">
  <img src="figures/readme_figures/halo_2d_unit_cell_architecture.png" alt="2D Unit Cell Architecture" width="600"/>
</p>

## 📂 Repository Structure

```text
HALO-Engine/
├── halo/                   # Core Python library
│   ├── hamiltonian.py      # O(1) Hamiltonian builder
│   ├── compiler.py         # Hardware-aware transpilation pipeline
│   └── zne_folding.py      # Digital Zero-Noise Extrapolation logic
├── benchmarks/             # Publication-grade execution scripts (Scaling, Dynamics, VQE)
├── notebooks/              # Interactive environments
│   └── halo_quickstart_tutorial.ipynb
├── figures/                # Auto-generated outputs for plots and architectures
├── requirements.txt        # Exact environment dependencies
└── README.md
```
## 🚀 Quickstart

**1. Clone the repository:**
```bash
git clone https://github.com/stark-069/HALO-Engine.git
cd HALO-Engine
```
**2. Set up the Python environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
**3. Run the interactive tutorial:**
```bash
jupyter notebook notebooks/halo_quickstart_tutorial.ipynb
```
## 📈 Reproducing Publication Benchmarks
To generate the exact figures, hardware scaling data, and VQE convergence sweeps from the paper, run any of the provided benchmark scripts from the root directory.

For example:

```bash
python benchmarks/01_compiler_scaling_benchmark.py
```
All resultant data and plots will automatically save to the `/figures` directory.

## 📝 Citation

If you utilize the HALO Engine, its compiler methodologies, or the physical data in your research, please cite our work:

```bibtex
@article{gohar2026halo,
  title={The HALO Engine: O(1)-Step Compilation and Localized String Rupture for Lattice Gauge Theories on Quantum Hardware},
  author={Gohar, Abhiroop},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2026}
}
```
## Author & Contact

**Abhiroop Gohar**  
*Undergraduate, Engineering Physics*  
*Indian Institute of Technology (IIT) Indore*  

For academic collaborations, discussions regarding the HALO framework, or research opportunities, feel free to reach out:

* **Email:** abhiroopgohar@gmail.com
* **GitHub:** [@stark-069](https://github.com/stark-069)
