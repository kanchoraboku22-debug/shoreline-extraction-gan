# Contributing to Shoreline Extraction GAN

Thank you for your interest in contributing to this project! We welcome contributions from researchers, developers, and coastal scientists.

## 🎯 How to Contribute

### Reporting Issues

Found a bug or have a suggestion? Please open an issue on GitHub with:

1. **Clear title** - Describe the problem concisely
2. **Detailed description** - What did you expect vs. what happened?
3. **Steps to reproduce** - How can we replicate the issue?
4. **Environment info** - Python version, OS, conda environment
5. **Relevant code** - Code snippets or error messages

### Submitting Code

We follow a standard GitHub workflow:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/shoreline-extraction-gan.git
   cd shoreline-extraction-gan
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code style guidelines (see below)
   - Add docstrings and comments
   - Include type hints
   - Test your changes

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature X for improved Y performance"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Code Style Guidelines

### Python Standards

- **PEP 8 compliance** - Use `black` formatter
- **Type hints** - Include for all function arguments
- **Docstrings** - Google or NumPy style
- **Line length** - Max 100 characters

### Example Function

```python
def calculate_shoreline_change(
    baseline: np.ndarray,
    survey: np.ndarray,
    years: float = 10.0
) -> dict:
    """
    Calculate Net Shoreline Movement (NSM) and End Point Rate (EPR).
    
    Parameters
    ----------
    baseline : np.ndarray
        Reference shoreline positions (N,) shaped array
    survey : np.ndarray
        Survey shoreline positions (N,) shaped array
    years : float, optional
        Time span between surveys in years (default: 10.0)
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'nsm': Net shoreline movement (pixels)
        - 'epr': End point rate (pixels/year)
        - 'change_type': Classification ('Erosion', 'Stable', 'Accretion')
    
    Raises
    ------
    ValueError
        If baseline and survey have different shapes
        
    Examples
    --------
    >>> baseline = np.array([100, 101, 99, 102])
    >>> survey = np.array([95, 98, 96, 99])
    >>> result = calculate_shoreline_change(baseline, survey, years=10)
    >>> print(result['epr'])
    -0.5  # pixels/year erosion rate
    """
    if baseline.shape != survey.shape:
        raise ValueError("baseline and survey must have same shape")
    
    nsm = survey - baseline  # pixels
    epr = nsm / years  # pixels/year
    
    # Classify
    if epr < -0.1:
        change_type = "Erosion"
    elif epr > 0.1:
        change_type = "Accretion"
    else:
        change_type = "Stable"
    
    return {
        'nsm': nsm,
        'epr': epr,
        'change_type': change_type
    }
```

### Import Organization

```python
# Standard library
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Third-party
import numpy as np
import pandas as pd
from shapely.geometry import LineString

# Local
from utils.image_processing_utils import apply_median_filter
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=utils tests/

# Run specific test file
pytest tests/test_validation.py
```

### Writing Tests

Create tests in `tests/` directory:

```python
import pytest
from utils.transect_analysis import calculate_shoreline_change

def test_calculate_shoreline_change_erosion():
    """Test NSM calculation for erosion scenario"""
    baseline = np.array([100, 101, 99, 102])
    survey = np.array([95, 98, 96, 99])
    
    result = calculate_shoreline_change(baseline, survey, years=10)
    
    assert result['epr'].mean() < 0  # Erosion
    assert result['change_type'] == "Erosion"

def test_calculate_shoreline_change_shape_mismatch():
    """Test error handling for mismatched shapes"""
    baseline = np.array([100, 101, 99])
    survey = np.array([95, 98, 96, 99])  # Different length
    
    with pytest.raises(ValueError):
        calculate_shoreline_change(baseline, survey)
```

## 📚 Documentation

### Adding Documentation

- Update docstrings when modifying functions
- Include examples in docstrings
- Update README.md for new features
- Add comments for complex logic
- Create `.md` files for major features

### Example Documentation

```python
"""
Phase 3A: Transect-Based Shoreline Change Analysis

This module implements the transect-based method for analyzing historical
shoreline change. It follows the DSAS methodology (Thieler et al., 2005).

Key Functions
-------------
- generate_transects : Create perpendicular transects along baseline
- compute_change_metrics : Calculate NSM, EPR, MAC for each transect
- classify_change : Classify transects as erosion/stable/accretion

Example Usage
-------------
```python
from utils.transect_analysis import run_transect_analysis

success = run_transect_analysis(
    processed_dir='model_outputs/processed',
    output_dir='model_outputs/analysis/transects'
)
```

References
----------
Thieler, E. R., & Danforth, W. W. (1994). Historical shoreline change 
and associated coastal morphology of the Atlantic coast, U.S. Geological 
Survey Open-File Report 94-418.
"""
```

## 🔄 Development Workflow

### Setting Up Development Environment

```bash
# Create conda environment
conda env create -f envs/shoreline_gan.yml
conda activate shoreline_gan

# Install development dependencies
pip install pytest pytest-cov black flake8

# Install package in editable mode
pip install -e .
```

### Code Quality Checks

```bash
# Format with black
black utils/ scripts/ tests/

# Check style with flake8
flake8 utils/ scripts/ tests/

# Run type checking (if mypy installed)
mypy utils/

# Run tests with coverage
pytest --cov=utils tests/
```

## 🎁 Types of Contributions

### 1. Algorithm Improvements
- Better shoreline detection methods
- Improved forecasting models
- Enhanced change metrics
- GPU acceleration

### 2. New Functionality
- Support for additional satellite sensors
- Multi-country batch processing
- Real-time coastal monitoring
- Advanced visualization options

### 3. Performance Optimization
- Vectorized NumPy operations
- Memory efficiency improvements
- Parallel processing
- Faster I/O operations

### 4. Documentation
- Tutorial notebooks
- Use case examples
- API documentation
- Video tutorials

### 5. Bug Fixes
- Error handling improvements
- Cross-platform compatibility
- Data format issues
- Memory leaks

## 🏆 Review Process

All submissions undergo review:

1. **Automated checks** - Code style, tests, build status
2. **Code review** - Functionality, design, performance
3. **Testing** - Manual testing with sample data
4. **Documentation** - Clarity and completeness

## 📝 Commit Message Guidelines

Write clear, descriptive commit messages:

```
[TYPE] Brief description (50 chars max)

More detailed explanation if needed (wrap at 72 chars)

- Bullet point 1
- Bullet point 2

Fixes #123
```

**Types:**
- `[FEATURE]` - New functionality
- `[FIX]` - Bug fix
- `[DOCS]` - Documentation only
- `[REFACTOR]` - Code restructuring
- `[PERF]` - Performance improvement
- `[TEST]` - Test additions/modifications

## 🚀 Release Process

Releases follow semantic versioning:

- **MAJOR** - Breaking API changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

## 📞 Communication

- **Issues** - Bug reports and feature requests
- **Discussions** - Design decisions, questions
- **Email** - Contact project maintainers for sensitive issues

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ✨ Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

---

**Thank you for contributing to coastal science! 🌊**
