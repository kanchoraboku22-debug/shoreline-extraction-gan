# =====================================================
# auto_shoreline_pipeline.ps1
# Shoreline GAN full setup + GPU execution (Windows)
# =====================================================

Write-Host "Checking project root..."

$projectRoot = Get-Location
if (-not (Test-Path "$projectRoot\scripts\run_pipeline_mombasa.py")) {
    Write-Host "ERROR: Run this from Shoreline_Extraction_GAN-main"
    exit 1
}

# -----------------------------------------------------
# Activate conda environment
# -----------------------------------------------------
Write-Host "Activating conda environment shoreline_gan"

$condaBase = (& conda info --base).Trim()
& "$condaBase\shell\condabin\conda-hook.ps1"
conda activate shoreline_gan

# -----------------------------------------------------
# Fix PYTHONPATH
# -----------------------------------------------------
Write-Host "Setting PYTHONPATH"
$env:PYTHONPATH = "$projectRoot"

# -----------------------------------------------------
# Install dependencies
# -----------------------------------------------------
Write-Host "Installing dependencies"

conda install -y -c conda-forge `
 numpy pandas scipy matplotlib scikit-image scikit-learn `
 shapely pyproj rasterio geopandas gdal opencv `
 tqdm pillow fiona affine imageio h5py

# -----------------------------------------------------
# Verify CUDA
# -----------------------------------------------------
Write-Host "Checking PyTorch CUDA"

python -c "import torch; print('torch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPUs:', torch.cuda.device_count()); assert torch.cuda.is_available()"

# -----------------------------------------------------
# Patch SDS_preprocess import
# -----------------------------------------------------
Write-Host "Patching SDS_preprocess.py"

$preprocessFile = "$projectRoot\utils\coastsat\SDS_preprocess.py"

(Get-Content $preprocessFile) `
-replace 'from coastsat import SDS_tools', 'from utils.coastsat import SDS_tools' |
Set-Content $preprocessFile

# -----------------------------------------------------
# Sanity imports (Python only)
# -----------------------------------------------------
Write-Host "Running import checks"

python -c "from utils.coastsat import SDS_tools, SDS_preprocess; import cv2, pandas; print('Imports OK')"

# -----------------------------------------------------
# Run pipeline
# -----------------------------------------------------
Write-Host "Running Shoreline GAN pipeline (GPU)"

cd scripts
python run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest
