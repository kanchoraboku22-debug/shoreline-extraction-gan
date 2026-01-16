# Shoreline Extraction GAN

## 🌊 Deep Learning-Based Shoreline Detection & Forecasting

A complete Python pipeline for extracting shoreline features from satellite imagery, analyzing temporal change rates, and generating predictions using LSTM neural networks.

**🚀 Quick Launch:**
- **Windows:** Double-click `LAUNCH_GUI.bat`
- **macOS/Linux:** Run `bash launch_gui.sh`
- **Python:** `python shoreline_gui_advanced.py`

## 📖 Complete Documentation

- **[GUI User Guide](GUI_USER_GUIDE.md)** - All 4 applications explained
- **[GitHub Setup](../GITHUB_REPOSITORY_SETUP.md)** - Project configuration
- **[Contributing](../CONTRIBUTING.md)** - Developer guidelines
- **[Manuscript Template](../MANUSCRIPT_TEMPLATE.md)** - Publication template

---

## 📊 Project Highlights

### Phases Completed

| Phase | Completion | Output |
|-------|-----------|--------|
| **Phase 1** | ✅ Complete | 3,204 shoreline contours extracted |
| **Phase 2** | ✅ Complete | 28 GIS-compatible vector files |
| **Phase 3A** | ✅ Complete | 62 transect-based change metrics |
| **Phase 3B** | ✅ Complete | 248 time-series observations |
| **Phase 3C** | ✅ Complete | 124 forecast predictions (2034, 2044) |

### Key Statistics

- **Temporal Coverage:** 30 years (1994-2024)
- **Study Area:** Mombasa, Kenya
- **Shoreline Contours:** 3,204 extracted
- **Mean Change Rate:** -0.2 ± 2.1 m/year
- **Coastal Stability:** 87.1% stable sections
- **Forecast Accuracy (R²):** 0.81+ for 20-year horizon

---

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/kanchoraboku22-debug/shoreline-extraction-gan.git
cd shoreline-extraction-gan

# Create conda environment
conda env create -f envs/shoreline_gan.yml
conda activate shoreline_gan

# Install additional dependencies
pip install -r requirements.txt
```

### Quick Start

```python
from scripts.run_phase3_full import execute_full_pipeline

# Run complete analysis
results = execute_full_pipeline(
    study_area='mombasa',
    start_year=1994,
    end_year=2024,
    forecast_to_year=2044
)

print(f"Shorelines extracted: {results['shoreline_count']}")
print(f"Change rate: {results['mean_rate']:.2f} m/year")
print(f"Forecast R²: {results['forecast_r2']:.3f}")
```

---

## 📈 Results Overview

### Shoreline Extraction

Automated extraction of shoreline contours from Landsat satellite imagery using U-Net segmentation:

- **1994:** 801 contours, 2,847m mean length
- **2004:** 801 contours, 2,856m mean length
- **2014:** 801 contours, 2,841m mean length
- **2024:** 801 contours, 2,852m mean length

### Coastal Change Analysis

Transect-based analysis reveals:

- **Eastern Beach:** +0.5 m/year accretion
- **Harbor Area:** +2.1 m/year (dredging)
- **Rocky Coast:** -0.1 m/year (stable)
- **Southern Beach:** +0.3 m/year accretion

### Forecasts (2034 & 2044)

LSTM neural network predictions:

- **2034 Forecast:** -0.15m mean change (10-year)
- **2044 Forecast:** -0.31m mean change (20-year)
- **Confidence:** 84.7% (10yr), 81.2% (20yr)

---

## 📚 Documentation

### User Guide

- [Installation & Setup](docs/installation.md)
- [Running the Pipeline](docs/usage.md)
- [Interpreting Results](docs/results.md)
- [Configuration Options](docs/configuration.md)

### Technical Documentation

- [Architecture Overview](docs/architecture.md)
- [Algorithm Details](docs/algorithms.md)
- [Data Specifications](docs/data.md)
- [Performance Metrics](docs/performance.md)

### API Reference

- [Python Modules](docs/api.md)
- [Functions Reference](docs/api-functions.md)
- [Class Reference](docs/api-classes.md)

---

## 🔬 Methods Summary

### Phase 1: Shoreline Extraction

Deep learning-based automated extraction:
- **Input:** Landsat satellite scenes (30m resolution)
- **Model:** U-Net semantic segmentation
- **Output:** Binary water/land masks → shoreline contours
- **Accuracy:** 93.7% validation accuracy

### Phase 2: Vector Export & GIS Integration

Conversion to geospatial formats:
- **Formats:** Shapefile, GeoJSON, KML
- **Attributes:** Year, length, confidence scores
- **Validation:** Topology checking, artifact removal
- **Deliverable:** 28 GIS-ready files

### Phase 3A: Transect-Based Change Analysis

Quantification of coastal dynamics:
- **Method:** Perpendicular transects to shoreline (500m spacing)
- **Metrics:** Distance, velocity, acceleration
- **Output:** 62 transects with multi-temporal observations
- **Result:** Change rates for each coastal section

### Phase 3B: Time-Series Assembly

Assembly of temporal sequences:
- **Structure:** 248 time-series (62 transects × 4 years)
- **Features:** Distance, velocity, acceleration
- **Format:** 3D tensor (62, 31, 3) for neural networks
- **Interpolation:** Linear interpolation for intermediate years

### Phase 3C: LSTM Forecasting

Neural network-based predictions:
- **Architecture:** Stacked LSTM with dropout
- **Training:** 100 epochs, MAE loss
- **Validation:** 20% holdout, R² scoring
- **Forecasts:** 2034 (10yr) and 2044 (20yr)

---

## 📊 Visualizations

All results include publication-ready visualizations at 300 DPI:

1. **shoreline_comparison_all_years.png** - Multi-year overlay
2. **erosion_accretion_map.png** - Spatial change patterns
3. **change_metrics_distribution.png** - Statistical distributions
4. **lstm_forecast_samples.png** - Representative forecasts
5. **shoreline_overlay_[year].png** - Year-specific maps (4 files)
6. **summary_statistics.png** - Key statistics summary

---

## 🔗 Resources

- **[GitHub Repository](https://github.com/kanchoraboku22-debug/shoreline-extraction-gan)**
- **[Publication](MANUSCRIPT_FINAL.md)** - Full technical manuscript
- **[Datasets](data/)** - Input satellite imagery and outputs
- **[Code Examples](examples/)** - Usage scripts and tutorials

---

## 📝 Citation

If you use this project in research, please cite:

```bibtex
@software{shoreline_gan_2026,
  title={Shoreline Extraction GAN: Automated Shoreline Extraction and Forecasting},
  author={Shoreline GAN Development Team},
  year={2026},
  url={https://github.com/kanchoraboku22-debug/shoreline-extraction-gan},
  version={1.0.0}
}
```

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## ❓ FAQ

**Q: Can I use this on a different coastal region?**  
A: Yes! The framework is designed to be region-agnostic. See [docs/adaptation.md](docs/adaptation.md).

**Q: What satellite data is required?**  
A: Landsat 5/7/8 Level-1 Surface Reflectance. See [docs/data-requirements.md](docs/data-requirements.md).

**Q: How accurate are the forecasts?**  
A: R² = 0.81+ for 20-year horizons. See [docs/validation.md](docs/validation.md).

**Q: Can I run this without a GPU?**  
A: Yes, but training is slower. CPU execution is fully supported.

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/kanchoraboku22-debug/shoreline-extraction-gan/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kanchoraboku22-debug/shoreline-extraction-gan/discussions)
- **Documentation:** This site

---

## 🎓 Academic Use

This project is designed to support:
- **Thesis Research** - Coastal change analysis and forecasting
- **Journal Publication** - Methods and results ready for peer review
- **Conference Presentations** - Complete visualizations and data
- **Grant Proposals** - Reproducible methodology and results

See [MANUSCRIPT_FINAL.md](MANUSCRIPT_FINAL.md) for full technical details.

---

**Last Updated:** January 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅

---

_Shoreline Extraction GAN: Automated Coastal Monitoring for Sustainable Development_
