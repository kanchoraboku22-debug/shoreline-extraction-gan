# Environment Setup (VS Code friendly) ✅

This document describes a reproducible workflow to set up the development environment for the project in VS Code on Windows (also works on Linux with small changes).

## Recommended Python & Tools
- Python: 3.8–3.10 (conda environments in `envs/` are tested with these versions)
- Anaconda / Miniconda
- VS Code with the Python extension
- (Optional) NVIDIA GPU + CUDA for acceleration

## Quick Start (Windows PowerShell)
1. Open **Anaconda PowerShell Prompt** or a PowerShell session where `conda` is available.
2. From the repo root, run:

    powershell.exe -ExecutionPolicy Bypass -File scripts/setup_env.ps1

3. This will create/activate the `shoreline_gan` environment, install some extras, and run a smoke test.

## Manual Steps (if you prefer)
1. Create conda env manually:

    conda env create --file envs/shoreline_gan.yml

2. Activate it:

    conda activate shoreline_gan

3. Install extras from conda-forge if needed:

    conda install -c conda-forge rasterio fiona geopandas shapely rtree

4. Run the smoke test:

    python scripts/run_smoke_test.py

## VS Code configuration
- Install the **Python** extension.
- Open the Command Palette (Ctrl+Shift+P) → Select Interpreter → pick `shoreline_gan` environment.
- Set the workspace `settings.json` (if desired):

```json
{
  "python.pythonPath": "${command:python.interpreterPath}",
  "python.terminal.activateEnvironment": true
}
```

## CUDA/GPU detection
- The smoke test prints `torch.cuda.is_available()` and device details.
- For CUDA-enabled PyTorch, please see: https://pytorch.org/get-started/locally/

## Next steps
- Follow the project README or run the GUI with `python shoreline_gan_gui.py`.
- To run the end-to-end pipeline for Mombasa once data is available, see `docs/usage_mombasa.md` (to be added).
