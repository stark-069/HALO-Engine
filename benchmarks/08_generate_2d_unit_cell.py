"""
Benchmark 08: 2D Unit-Cell Architecture Blueprint
Generates Figure 9 from the manuscript: halo_2d_unit_cell_architecture.pdf
"""

import os
import matplotlib.pyplot as plt
from halo.compiler import build_2d_unit_cell_circuit

def draw_2d_unit_cell():
    print("-" * 65)
    print("BENCHMARK 8: GENERATING 2D SCALED UNIT CELL ARCHITECTURE")
    print("-" * 65)
    
    # 1. Fetch the architecture from our compiler library
    qc = build_2d_unit_cell_circuit()
    
    # 2. Setup absolute paths for saving
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    figures_dir = os.path.join(project_root, 'figures')
    os.makedirs(figures_dir, exist_ok=True) 
    
    save_path = os.path.join(figures_dir, 'halo_2d_unit_cell_architecture.pdf')
    
    # 3. Export with adjusted scaling for high density
    qc.draw(output='mpl', filename=save_path, 
            style={'fontsize': 11, 'subfontsize': 9}, plot_barriers=True, scale=0.85)
            
    print(f"[+] 2D Unit Cell Graphic successfully exported to:\n    {save_path}")

if __name__ == "__main__":
    draw_2d_unit_cell()

