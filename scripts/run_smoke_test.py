"""Run a quick smoke test to validate core Python dependencies and GPU availability."""
import sys
import importlib

print("Python:", sys.version.replace('\n', ' '))

def check_module(name):
    try:
        mod = importlib.import_module(name)
        ver = getattr(mod, '__version__', 'unknown')
        print(f"Imported {name} (version: {ver})")
        return True
    except Exception as e:
        print(f"ERROR importing {name}: {e}")
        return False

# Core libs
check_module('numpy')
check_module('rasterio')
check_module('fiona')
check_module('shapely')
check_module('geopandas')
check_module('torch')

# Torch GPU check
try:
    import torch
    print('Torch version:', torch.__version__)
    print('CUDA available:', torch.cuda.is_available())
    if torch.cuda.is_available():
        print('CUDA device count:', torch.cuda.device_count())
        print('Current device:', torch.cuda.current_device())
except Exception as e:
    print('Torch GPU check failed:', e)

# Repo import tests
check_module('pix2pix_modules')
check_module('utils.image_processing_utils')

print('\nSmoke test finished. If any imports failed, install missing packages or check the active environment.')
