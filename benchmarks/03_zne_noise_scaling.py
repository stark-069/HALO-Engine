"""
Benchmark 03: Zero-Noise Extrapolation (ZNE) Analysis
Generates Figure 4 from the manuscript: phase1_zne_final_labeled.pdf
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Import the standardized Lindblad model from the HALO library
from halo.mitigation import exp_decay

def generate_zne_plot():
    print("-" * 65)
    print("BENCHMARK 3: ZERO-NOISE EXTRAPOLATION RECOVERY (10 QUBITS)")
    print("-" * 65)

    # 1. Exact QPU Readout Inputs (ibm_marrakesh)
    lambda_scales = np.array([1, 3, 5])
    qpu_probs = np.array([23.438, 2.588, 0.293])

    exact_truth = 69.0309     # Continuous Time Target (t = 0.5)
    trotter_target = 68.9646  # Depth-2 Algorithmic Ceiling
    zne_recovered = 70.626    # Extrapolated ZNE value at lambda = 0
    noise_floor = 0.09        # 10-qubit Hilbert space noise floor (~1/1024)

    # 2. Fit to Lindblad Exponential Decay
    popt, _ = curve_fit(exp_decay, lambda_scales, qpu_probs, p0=[80, 1, 0.1], maxfev=10000)
    x_fit = np.linspace(0, 5.2, 300)
    y_fit = exp_decay(x_fit, *popt)

    # 3. Figure Setup & Styling
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    ax.grid(True, which='both', linestyle=':', color='#cccccc', alpha=0.6, zorder=0)

    # Reference Baselines
    ax.axhline(exact_truth, color='#1f77b4', linestyle='--', linewidth=1.2, alpha=0.85,
               label=f'Continuous Physics Truth ({exact_truth:.2f}%)', zorder=1)
    ax.axhline(trotter_target, color='#8c564b', linestyle=':', linewidth=1.2, alpha=0.85,
               label=f'Trotter Depth 2 Target ({trotter_target:.2f}%)', zorder=1)
    ax.axhline(noise_floor, color='gray', linestyle='-.', linewidth=1.0, alpha=0.5,
               label=f'White Noise Floor ({noise_floor:.2f}%)', zorder=1)

    # Data Plots
    ax.plot(x_fit, y_fit, color='#444444', linestyle='--', linewidth=1.4, alpha=0.75,
            label='Lindblad Exponential Fit', zorder=2)
    ax.plot(lambda_scales, qpu_probs, 'o-', color='#d62728', markersize=6, linewidth=1.5,
            label='Unmitigated QPU Readouts (ibm_marrakesh)', zorder=4)
    ax.plot(0, zne_recovered, 'o', color='#2ca02c', markersize=6, markeredgecolor='#1b611b',
            markeredgewidth=1.0, label=f'ZNE Extrapolated ({zne_recovered:.2f}%)', zorder=5)

    # Annotations
    for lam, prob in zip(lambda_scales, qpu_probs):
        ax.annotate(f'{prob:.2f}%', xy=(lam, prob), xytext=(lam, prob + 3.2),
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#900c3f', zorder=6)

    ax.annotate(
        f'ZNE Extrapolated: {zne_recovered:.2f}%\nContinuous Truth: {exact_truth:.2f}%\nTrotter Target:    {trotter_target:.2f}%',
        xy=(0, zne_recovered), xytext=(0.6, 56.0),
        arrowprops=dict(arrowstyle='->', color='#333333', lw=0.9, connectionstyle="arc3,rad=-0.12"),
        fontsize=8.5, family='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#cccccc', alpha=0.95), zorder=6
    )

    ax.set_xlabel(r'Hardware Noise Scale ($\lambda$)', fontsize=11, labelpad=8)
    ax.set_ylabel('Meson Survival Probability (%)', fontsize=11, labelpad=8)
    ax.set_title(r'HALO Zero-Noise Extrapolation (10-Qubit QLM, $t=0.5$)', fontsize=12, fontweight='bold', pad=12)

    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlim(-0.3, 5.3)
    ax.set_ylim(-3, 82)
    ax.legend(loc='upper right', fontsize=8.5, frameon=True, facecolor='white', edgecolor='#cccccc', framealpha=0.95)

    plt.tight_layout()

    # Save to figures/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    save_path = os.path.join(figures_dir, 'phase1_zne_final_labeled.pdf')

    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"[+] ZNE recovery plot successfully saved to:\n    {save_path}")

if __name__ == "__main__":
    generate_zne_plot()
  