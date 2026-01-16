# PowerShell script to create recommended conda environment and run a smoke test
# Usage: Open Anaconda PowerShell Prompt or a PowerShell session where 'conda' is available

$envName = "shoreline_gan"
$envFile = "envs/shoreline_gan.yml"

Write-Host "Checking for conda..."
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Conda not found in PATH. Please open Anaconda Prompt or run 'conda init powershell' and restart the shell." -ForegroundColor Red
    exit 1
}

Write-Host "Creating conda environment '$envName' from $envFile (if not exists)..."
conda env list | Select-String -Pattern "^$envName\s" -Quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Environment not found. Creating..."
    conda env create --file $envFile --name $envName
} else {
    Write-Host "Environment '$envName' already exists. To recreate run: conda env remove -n $envName; then run this script again." -ForegroundColor Yellow
}

Write-Host "Activating environment..."
conda activate $envName

Write-Host "Installing any optional extras (rasterio, fiona, geopandas) via conda-forge..."
conda install -y -c conda-forge rasterio fiona geopandas shapely rtree

Write-Host "Running smoke test..."
python scripts/run_smoke_test.py

Write-Host "Done. If the smoke test passed, follow the instructions in docs/environment_setup.md for VS Code configuration and next steps." -ForegroundColor Green
