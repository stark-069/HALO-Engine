# ⚡ HALO Engine (Hardware-Aware Lattice Optimization)

A highly optimized, constant-depth ($\mathcal{O}(1)$) quantum compiler for simulating Lattice Gauge Theories (LGTs) on near-term physical quantum hardware. 

The HALO framework bypasses the severe $\mathcal{O}(N)$ circuit depth overheads associated with standard Jordan-Wigner transformations by natively mapping composite gauge links to the hardware topology. This repository contains the core compiler library and the exact benchmarking scripts used to generate the data for the associated publication.

## 📂 Repository Structure

* `halo/`: The core python library containing the $\mathcal{O}(1)$ Hamiltonian builder, compiler pipeline, and digital Zero-Noise Extrapolation (ZNE) folding logic.
* `benchmarks/`: Publication-grade execution scripts that reproduce the exact figures, hardware scaling data, and VQE convergence sweeps from the manuscript.
* `notebooks/`: Interactive Jupyter notebooks, including a lightweight quickstart tutorial for generating and compiling HALO circuits.
* `figures/`: The output directory for all generated PDF plots and circuit architectures.

## 🚀 Quickstart

**1. Clone the repository:**
```bash
git clone [https://github.com/stark-069/HALO-Engine.git](https://github.com/stark-069/HALO-Engine.git)
cd HALO-Engine

```

**2. Set up the environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

**3. Run the interactive tutorial:**

```bash
jupyter notebook notebooks/halo_quickstart_tutorial.ipynb

```

## 📊 Reproducing Publication Benchmarks

To generate the exact figures from the paper, run the benchmark scripts from the root directory. For example, to generate the compiler scaling duel:

```bash
python benchmarks/01_compiler_scaling_benchmark.py

```

Outputs will be automatically saved to the `/figures` directory.

```

### 4. Setting up the `figures/` Folder for Git
Git does not track empty folders. To ensure the `figures/` folder actually gets pushed to GitHub so the benchmark scripts have a place to save their PDFs when someone else clones it, we have to put a hidden placeholder file inside it.

Run these exact commands in your terminal:

```bash
mkdir figures
touch figures/.keep

```

---

### 5. The Final Git Push

Your repository is now completely built, secured, and documented. Run these commands in your terminal from the root `HALO-Engine` folder to ship it to GitHub:

```bash
# 1. Initialize the local repository
git init

# 2. Add all your files (The .gitignore will automatically block the .env and .venv files)
git add .

# 3. Commit the codebase
git commit -m "Initial commit: HALO Engine core library, benchmarks, and interactive tutorial"

# 4. Link it to your GitHub repository 
# (Replace 'your-repo-link' with the actual HTTPS link from your empty GitHub repo)
git remote add origin https://github.com/stark-069/HALO-Engine.git

# 5. Push the code to the main branch
git branch -M main
git push -u origin main

```