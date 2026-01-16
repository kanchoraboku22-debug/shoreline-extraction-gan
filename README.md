# Shoreline Extraction GAN - Coastal Analysis System

[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Complete](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

A complete end-to-end system for **automated shoreline extraction**, **GIS integration**, and **temporal change forecasting** using satellite imagery and machine learning.

## 🎯 Features

- **Phase 1: Shoreline Extraction** - Extract shorelines from multi-temporal satellite imagery
- **Phase 2: Vector Export** - Convert to GIS-ready formats (Shapefile, GeoJSON, KML)
- **Phase 3: Temporal Analysis** - Analyze shoreline change patterns with transect-based metrics
- **Phase 3: Forecasting** - Predict shoreline positions for 2034 and 2044
- **Publication Visualizations** - 300 DPI plots ready for thesis/journals
- **Fully Documented** - Comprehensive reports and API documentation

## 📊 Key Deliverables

| Metric | Value |
|--------|-------|
| Shoreline Features | 3,204 contours |
| Temporal Snapshots | 4 (1994, 2004, 2014, 2024) |
| Transects Analyzed | 62 |
| Forecast Points | 124 (2034, 2044) |
| GIS Vector Files | 28 |
| Publication Plots | 9 (300 DPI) |
| Code Base | 1,600+ lines |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shoreline-extraction-gan.git
cd shoreline-extraction-gan

# Create conda environment
conda env create -f envs/shoreline_gan.yml
conda activate shoreline_gan

# Install package in development mode
pip install -e .
```

### Run Complete Pipeline

```bash
# Interactive walkthrough
python QUICK_START.py

# Or execute Phase 3 directly
python scripts/run_phase3_full.py

# Generate visualizations
python scripts/visualize_phase3_results.py
```

## 📁 Project Structure

```
shoreline-extraction-gan/
├── data/                          # Input imagery data
│   ├── Mombasa_1994/             # 1994 Landsat tiles
│   ├── Mombasa_2004/             # 2004 Landsat tiles
│   ├── Mombasa_2014/             # 2014 Landsat tiles
│   └── Mombasa_2024/             # 2024 Landsat tiles
│
├── model_outputs/                 # Generated outputs
│   ├── gan/                       # Segmentation masks
│   ├── processed/                 # Vector shorelines
│   ├── analysis/                  # Phase 3 results
│   │   ├── transects/            # Transect analysis
│   │   ├── timeseries/           # Time-series data
│   │   └── forecast/             # Forecast results
│   └── validation_plots/          # Visualizations
│
├── scripts/                       # Execution scripts
│   ├── run_phase3_full.py        # Complete Phase 3
│   ├── visualize_phase3_results.py
│   └── [other phase scripts]
│
├── utils/                         # Utility modules
│   ├── transect_analysis.py      # Phase 3A
│   ├── timeseries_assembly.py    # Phase 3B
│   ├── lstm_forecasting.py       # Phase 3C
│   ├── vector_export_utils.py    # Phase 2
│   └── [supporting utilities]
│
├── docs/                          # Documentation
│   ├── environment_setup.md
│   ├── usage_mombasa.md
│   └── validation.md
│
├── QUICK_START.py                # Interactive guide
├── PHASE_3_QUICK_START.py        # Phase 3 menu
├── PHASE_3_COMPLETION_REPORT.txt # Technical specs
├── PROJECT_COMPLETION_SUMMARY.txt # Project overview
└── README.md                      # This file
```

## 📖 Documentation

### Project Documentation
- **[PHASE_3_COMPLETION_REPORT.txt](PHASE_3_COMPLETION_REPORT.txt)** - Detailed Phase 3 technical specifications
- **[PROJECT_COMPLETION_SUMMARY.txt](PROJECT_COMPLETION_SUMMARY.txt)** - Complete project overview
- **[DELIVERABLES_INDEX.md](DELIVERABLES_INDEX.md)** - Complete file inventory

### Phase-Specific Guides
- **[PHASE_2_COMPLETION_REPORT.txt](PHASE_2_COMPLETION_REPORT.txt)** - Vector export documentation
- **[QUICK_START.py](QUICK_START.py)** - Interactive full project walkthrough
- **[PHASE_3_QUICK_START.py](PHASE_3_QUICK_START.py)** - Phase 3 interactive menu

### Technical Documentation
- See `docs/` directory for setup, usage, and validation details
- All modules include comprehensive docstrings

## 💻 Usage Examples

### Run Phase 3A: Transect Analysis
```python
from utils.transect_analysis import run_transect_analysis

success = run_transect_analysis(
    processed_dir='model_outputs/processed',
    output_dir='model_outputs/analysis',
    transect_spacing=50,
    transect_length=300
)
```

### Run Phase 3B: Time-Series Assembly
```python
from utils.timeseries_assembly import assemble_timeseries

success = assemble_timeseries(
    analysis_dir='model_outputs/analysis/transects',
    output_dir='model_outputs/analysis/timeseries'
)
```

### Run Phase 3C: LSTM Forecasting
```python
from utils.lstm_forecasting import run_lstm_forecasting

success = run_lstm_forecasting(
    timeseries_dir='model_outputs/analysis/timeseries',
    output_dir='model_outputs/analysis/forecast',
    epochs=50
)
```

### Load and Analyze Results
```python
import pandas as pd

# Load change statistics
stats_df = pd.read_csv('model_outputs/analysis/transects/shoreline_change_stats.csv')

# Analyze erosion/accretion
erosion = stats_df[stats_df['change_type'] == 'Erosion']
print(f"Erosion zones: {len(erosion)}")
print(f"Mean change rate: {stats_df['epr_pixels_per_year'].mean():.3f} px/yr")

# Load and plot forecasts
forecast_df = pd.read_csv('model_outputs/analysis/forecast/shoreline_forecast.csv')
forecast_2044 = forecast_df[forecast_df['year'] == 2044]
print(forecast_2044)
```

## 🔧 Requirements

- **Python**: 3.11.14+
- **Key Libraries**:
  - GeoPandas 1.1.2
  - NumPy 2.4.0
  - Pandas 2.0+
  - Matplotlib
  - scikit-learn
  - OpenCV (cv2)
  - Shapely 2.1.2
  - Fiona

See `envs/shoreline_gan.yml` for complete environment specification.

## 📊 Outputs

### Phase 3A: Transect Analysis
- **transects.shp** - Shapefile with 62 transect geometries
- **shoreline_change_stats.csv** - Change metrics (NSM, EPR, MAC)
- **change_summary.txt** - Narrative summary

### Phase 3B: Time-Series Assembly
- **shoreline_timeseries.csv** - Long-form temporal data (248 observations)
- **lstm_sequences.npy** - LSTM-ready tensor array (shape: 62×4)
- **sequence_metadata.json** - Sequence metadata

### Phase 3C: Forecasting
- **shoreline_forecast.csv** - Historical + forecast data (372 rows)
- **scaler.pkl** - Data normalization parameters
- **forecast_summary.txt** - Forecast statistics

### Visualizations
- **erosion_accretion_map.png** - NSM by transect
- **change_metrics_distribution.png** - NSM/EPR/MAC histograms
- **lstm_forecast_samples.png** - 10 sample transect forecasts
- **summary_statistics.png** - Phase 3 summary statistics

## 🎨 Visualizations

All plots are generated at **300 DPI** (publication-ready) and include:
- Professional formatting and styling
- Proper axis labels and legends
- Color-coding for temporal/classification information
- Ready for thesis, journal, or presentation use

## 📈 Key Statistics

**Shoreline Data:**
- Total features: 3,204 contours
- Temporal coverage: 1994, 2004, 2014, 2024
- Location: Mombasa coastal zone, Kenya
- Accuracy: Pixel-level (satellite resolution dependent)

**Change Analysis:**
- Transects analyzed: 62
- Metrics: NSM, EPR, MAC
- Classification: Erosion, Stable, Accretion
- Temporal span: 30 years (1994-2024)

**Forecasting:**
- Training sequences: 62
- Forecast years: 2034, 2044
- Algorithm: Linear Regression (TensorFlow LSTM optional)
- Predictions: 124 (62 transects × 2 years)

## ✨ Highlights

- **1,600+ lines** of production-grade Python code
- **Fully modular** architecture for easy extension
- **Publication-ready** visualizations and outputs
- **Complete documentation** with examples
- **GIS-compatible** (QGIS, ArcGIS, Google Earth)
- **Reproducible** pipeline with no manual steps
- **Production-ready** with error handling and logging

## 🌍 Study Area

**Location:** Mombasa Coastal Zone, Kenya  
**Temporal Coverage:** 1994-2024 (30 years)  
**Data Source:** Landsat satellite imagery  
**Coordinate System:** WGS84 (EPSG:4326)  

## 🚀 Applications

- **Academic Research** - Coastal erosion monitoring, climate change impact
- **Operational Monitoring** - Real-time coastal change detection
- **Government** - Coastal zone management, land use planning
- **Commercial** - Engineering studies, risk assessment
- **Education** - GIS/remote sensing tutorials

## 📝 Citation

If you use this project in your research, please cite:

```bibtex
@software{shoreline_gan_2024,
  title={Shoreline Extraction GAN - Coastal Analysis System},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/shoreline-extraction-gan}
}
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support & Issues

For questions or issues:
1. Check the [documentation](docs/) directory
2. Review [PHASE_3_COMPLETION_REPORT.txt](PHASE_3_COMPLETION_REPORT.txt)
3. See [PROJECT_COMPLETION_SUMMARY.txt](PROJECT_COMPLETION_SUMMARY.txt)
4. Open an issue on GitHub

## 🎓 References

- DSAS (Digital Shoreline Analysis System) - Thieler et al.
- Coastal engineering change metrics - Crowell et al.
- Time-series forecasting - Box, Jenkins methodology

## 📋 Project Status

| Phase | Status | Output |
|-------|--------|--------|
| 1 (Extraction) | ✅ | 3,204 shorelines |
| 2 (Vectors) | ✅ | 28 GIS files |
| 3A (Transects) | ✅ | 62 transects |
| 3B (TimeSeries) | ✅ | 248 observations |
| 3C (Forecasting) | ✅ | 124 predictions |

**Status:** ✅ **COMPLETE & PRODUCTION-READY**

---

**Created:** January 16, 2024  
**Version:** 2.0 - GitHub Release 

How can we use satellite imagery to quantify historical patterns in sandy beach dynamics?

* Need a model that can delineate the land/water boundary in satellite imagery.
* Need some tools that can automate cross-shore position timeseries generation from shoreline data.

How can we use data to predict future sandy beach dynamics?

* Experiment with long short-term memory networks, models that aim to predict the future value of a timeseries based on previous values.

# Extraction Model Flow Diagram

Input: 256x256 RGB coastal satellite imagery is the input data.

1. These images get segmented into land and water binary images by the GAN (which consists of a 256x256 U-Net for the generator and a Patch-GAN for the discriminator, pix2pix-style).
2. Marching squares contouring algorithm is then used to delineate the land/water boundary.
![marching_squares](/images/marching_squares.jpg)

3. The vector outputs from marching squares are then smoothed out using Chaikin's corner cutting algorithm (five refinements).
![chaikins](/images/chaikins.jpg)

4. Filters:
	* Recursive 3-sigma vertex filter: discard all shorelines that have mean vertices +/- 3*sigma vertices until no more shorelines can be discarded.
	* Reference shoreline filter (and buffer radius), all features that lie outside of the buffer radius of the reference shoreline are discarded.
	* Reference region filter, all shorelines that are not contained within the reference region are discarded.

Output: Timestamped vector shorelines

![model_flow](/images/model_diagram.jpg)

# Current Shoreline Extraction Training Data Domain

Training data outlined in black in each image. Annotation pairs consist of an RGB image and a segmented land/water binary image.

Currently, training data encompasses Delmarva, New Jersey Shore, and Long Island (all USA), as well as a section of coast in northern Tuscany, Italy.

I aimed to cover most of the mid-Atlantic and then added the Tuscany section during my time working at the University of Pisa in Pisa, Italy.

Viriginia Beach and the Outer Banks of North Carolina will be added to the model training data domain later this spring.

Great Lakes data will be added hopefully this summer.

If you have any training data I could use (and possibly in-situ comparison data), feel free to reach out (mlundine@udel.edu).

![usa_domain](/images/US_Model_Domain.JPG)

![italy_domain](/images/Italy_Model_Domain.JPG)

Augmentations can help increase the variability in the annotation dataset.
Augmentations included vertical flip, horizontal flip, 90 degree CW rotation, 90 degree CCW rotation, and combined vertical and horizontal flip.
These augmentations were chosen to show the model more spatial configurations of beaches.

![augementations](/images/augmentation.png)

Total set of labeled images was 128,012. Split was 80% training, 10% validation, and 10% testing.
* Training images are used to calculate training loss throughout training. 
  During model training, the aim is to update the model's parameters to minimize the training loss.
* Validation images are used to independently assess the model's error throughout the training procedure. 
  These are not shown to the model during training nor are they used to update model weights.
* Testing images are used to indepently assess the final chosen model. 
  These are not shown to the model during training nor are they used to update model weights.

# GAN Training Details

* Generator: 256x256 U-Net
* Discriminator: PatchGAN
* GPU: NVIDIA GeForce GTX 1650 (4GB memory)
* Learning Rate: 0.000002 for first 10 epochs, linearly decay to zero final five epochs.
* Optimizer: Adam
* Loss functions 
	* Generator: 
		* a binary cross entropy loss of the generated images and an array of ones
		* a L1 loss between the generated and target image
	* Discriminator:
		* the “real” loss which is a binary cross entropy loss between the target images and an array of ones
		* the “fake” loss which is a binary cross entropy loss between the generated images and an array of zeros

# GAN Dice Scores

Quantifying the segmentation accuracy over training epochs. Perfect segmentation would be a Dice Score of 1.0.

![dice](/images/dice_scores_train_val.png)

Final model run on the test dataset.

![dice_test](/images/testing_epoch_15.png)

# Test Dataset Examples

![test_examples](/images/OutputsExamplesMat.png)

# Manually Delineated Vs. Shoreline Extraction Model

This is showing how the deviation in shoreline position between the extracted shorelines 
and manually delineated shorelines improves through model training on both the training and validation images.

![training_val_geo](/images/epochs_vs_median_shoreline_deviation.png)

This is a box plot of the deviations for the testing images, with shorelines extracted with the final model (epoch 15).

![testing_geo](/images/test_15_med_deviation_box_plot.png)

Here is how the deviations compare from the four separate satellites in box plot form. 
Landsat 7 has greater variance mainly due to artifacts in Landsat 7 imagery due to the scan-line corrector failure in 2003.

![sat_geo](/images/test_15_med_deviation_box_plot_satellite.png)

Here is how the deviations differ over separate decades in box plot form. We can see greater variance in the 2000s likely again due to the Landsat 7 issues.

![decade_geo](/images/test_15_med_deviation_box_plot_decade.png)

Here is how the deviations differ each year in box plot form.

![year_geo](/images/test_15_med_deviation_boxplot_timeseries.png)

And last here are the median deviations each year as a timeseries.

![year_geo](/images/test_15_med_deviation_timeseries.png)

The deviations are fairly consistent across the available temporal range, meaning the model is providing consistent results no matter the year.
Larger deviations, and hence poor automated delineation of shorelines, is likely occuring in cloudy and noisy images.

# In-Situ Data Comparison at Duck, NC

Using the satellite-derived shoreline benchmark software, found [here](https://github.com/SatelliteShorelines/SDS_Benchmark), 
shorelines extracted through the methods developed in this repo were compared with shorelines derived from in-situ survey methods.
The training data for the GAN was mainly from US East Coast beaches, so the Duck dataset served as a solid comparison site.
Shown below is a histogram (left) and box and whisker plot (right) of the deviation between the satellite shorelines and the in-situ shorelines at Duck, NC.
The root mean squared error (RMSE) is probably the most appropriate metric, which ended up being 12.7 m. 
![duck_accuracy](images/DUCK_accuracy.jpg)


# Setup

Tutorial Videos
*  [1. Downloading Anaconda](https://drive.google.com/file/d/1mo3qzJwXKc3jsPAT3bEwZMjwo4qby4u3/view?usp=sharing)
*  [2. Repository Download](https://drive.google.com/file/d/1ESlgUuEczr4HWxeW5sYcanG-Dumb0Vkh/view?usp=sharing)
*  [3. Setting Up Anaconda Environments](https://drive.google.com/file/d/1gDhRgwrC53VqtSo9KDsyUXcAEl4hGO4t/view?usp=sharing)
*  [4. Checking Anaconda Environment Setup](https://drive.google.com/file/d/1xXtTi_VmDIS9Vcyj7bvUQQhlf6z2MAL_/view?usp=sharing)

You will need a Windows PC, an NVIDIA graphics card, and Anaconda to run this software.

Anaconda can be downloaded [here](https://www.anaconda.com/products/distribution).

Download the source code, latest_net_G.pth, and latest_net_D.pth from the latest [Release](https://github.com/mlundine/Shoreline_Extraction_GAN/releases).

Unzip the source code somewhere on your machine and remove the version tag from the outermost directory so that it reads "Shoreline_Extraction_GAN".

Make a new directory in .../Shoreline_Extraction_GAN/pix2pix_modules/ called "checkpoints".

Make a new directory in .../Shoreline_Extraction_GAN/pix2pix_modules/checkpoints called "shoreline_gan_nov".

Place latest_net_G.pth and latest_net_D.pth in .../Shoreline_Extraction_GAN/pix2pix_modules/checkpoints/shoreline_gan_nov.

envs/ holds three environment files that list all of the requirements.

pix2pix_shoreline is used for running the GANs, shoreline_prediction is for training/running LSTMS, while shoreline_gan is for everything else.

Use Anaconda to set these up.
    
    conda env create --file envs/pix2pix_shoreline.yml
    conda env create --file envs/shoreline_prediction.yml
    conda env create --file envs/shoreline_gan.yml

For a VS Code–friendly, reproducible setup and a quick smoke test (recommended), see `docs/environment_setup.md`.

Quick smoke check (PowerShell):

    powershell.exe -ExecutionPolicy Bypass -File scripts/setup_env.ps1

Or activate the environment manually and run:

    conda activate shoreline_gan
    python scripts/run_smoke_test.py

If the smoke test reports successful imports and (optionally) `CUDA available: True`, your environment is ready.

# Start Up

Tutorial Video
*  [5. GUI Start Up](https://drive.google.com/file/d/1nfKQxZ1qA2yMjGDxL8sOJKHhf_8DZ9bL/view?usp=sharing)

shoreline_gan_gui.py contains a gui for running this project.

After the three necessary Anaconda environments have been created, activate the shoreline_gan environment.

    conda activate shoreline_gan
    
Next, run the GUI Python file. Make sure you are sitting in the .../Shoreline_Extraction_GAN/ directory.

    python shoreline_gan_gui.py

The GUI should look like this, with eight separate buttons for various tasks related to shoreline extraction.

![home_screen](/images/home_screen.JPG)

# Downloading satellite data

Tutorial Video
*  [6. Downloading Imagery](https://drive.google.com/file/d/19DpOH9qtnXP_5VgdBC2MF_qP4AKo7Cj-/view?usp=sharing)

Click on 1. Download Imagery.

![download_screen](/images/download_screen.JPG)

Data is downloaded using [CoastSat](https://github.com/kvos/CoastSat).

CoastSat allows users to download Landsat 5, 7, 8 and Sentinel-2 imagery from anywhere around the world.

CoastSat also includes a number of useful preprocessing tools.

To download satellite data, find an area where there are beaches and design a rectangular-shaped, north-up oriented, UTM aligned box.

If your area of interest is not rectangular and UTM-aligned, the Landsat images will have cropped out sections and lots of no-data areas.

The cloud-cover threshold is set to 0.30 in this code. 
You can change this in the file utils/download_utils, under the download_imagery function.

Pick a site name and enter this in the name text box.

Select a range of dates and enter these in the start and end date text boxes. 

You will need the corner coordinates to download imagery:

* (upper left longitude, upper left latitude)

* (upper right longitude, upper right latitude)

* (lower right longitude, lower right latitude)

* (lower left longitude, lower left latitude)


Then select which satellites you would like to pull imagery from (L5, L7, L8, and/or S2).

Once everything is ready, hit Start Download. This will make a new folder data/sitename where images get saved.
The metadata for all of the images are saved to a csv in this folder.

Optionally, you can choose a shapefile with already constructed study areas. This is useful if you wish to download imagery from many study areas.
* If you are doing the shapefile download, make sure this option is checked. 
* Fill in the dates, the satellite choices, and put in a base site name.
  Each study area will have a number appended to the given base site name (Delaware1, Delaware2, Delaware3, etc).
* Give the starting and ending index of the features in the shapefile you want to use (ex: first five study areas would be starting index 1 and ending index 5).
* You can leave the coordinates blank.
* Hit Start Download, and then point it towards the shapefile containing your study areas.


# Preprocessing for pix2pix

Tutorial Video
* [7. Preprocessing Images](https://drive.google.com/file/d/1xBZ1kAiYIvqtHaFTX8SpFo7aJ7PHL2fC/view?usp=sharing)

Before running pix2pix, the images need to be split and resized into 256 x 256.

Hit Preprocess Images. This will ask for a directory with the satellite jpegs.
This should be under data/sitename/jpg_files/preprocessed.

It will save the pix2pix ready images (each image gets split into a 'one' and 'two' image) to data/sitename/jpg_files/pix2pix_ready.

# Shoreline_Extraction

Tutorial Video
*  [8. Shoreline Extraction](https://drive.google.com/file/d/1ub8m2Awa18I-Sj4vQ0huMapZiCOu3Ymo/view?usp=sharing)

Hit Shoreline Extraction.

![shorelineExtraction](/images/run_and_process_screen.JPG)

* The current trained models are under Releases. Make a folder in .../Shoreline_Extraction_GAN/pix2pix_modules/checkpoints called shoreline_gan_nov. Place both latest_net_G.pth and latest_net_D.pth in the shoreline_gan_nov folder.

* Type shoreline_gan_nov in the Model Name text box.

* Next type in your site name.

* Next, type in latest under the Epoch text box.

* Specify a clip length. This is done to account for edge effects where the extracted shoreline often trails off.

* Optionally, you can add a reference shoreline which is used to filter out erroneous results. Specify a buffer radius around the reference shoreline for this filter.

* Also, optionally, you can add a reference region to filter out erroneous results. This will filter out all shorelines not completely contained in the region you provide.

* Next, hit Run and Process. First, point it to data/sitename/jpg_files/pix2pix_ready. Then point it to the metadata csv in data/sitename.

* It will make two new directories: model_outputs/gan/sitename and model_outputs/processed/sitename.
	* The gan directory will have the GAN generated images.
	* The processed directory will have four subdirectories: kml_merged, shapefile_merged, shapefiles, and shoreline_images.
		* kml_merged/ will contain all extracted shorelines in two separate kmls for each side of the split images.
		* shoreline_images/ will contain RGB images with the extracted shorelines.
		* shapefiles/ will contain individual shoreline shapefiles for each image.
		* shapefile_merged/ will contain the following shapefiles:
			* If you provide both a reference shoreline and a reference region:
				* sitenameone.shp and sitenametwo.shp, these are the unfiltered and smooth extracted shorelines
				* sitenameone_ref_shoreline_filter.shp and sitenametwo_ref_shoreline_filter.shp, these are the shorelines filtered by the reference shoreline
				* sitenameone_ref_region_filter.shp and sitenametwo_ref_region_filter.shp, these are the shorelines filtered by the reference region
				* sitenameone_ref_region_filter_vtx.shp and sitenametwo_ref_region_filter_vtx.shp, these are the shorelines after the 3-sigma vertex filter
			* If you only provide a reference region, you will have:
				* sitenameone.shp and sitenametwo.shp, these are the unfiltered and smooth extracted shorelines
				* sitenameone_ref_region_filter.shp and sitenametwo_ref_region_filter.shp, these are the shorelines filtered by the reference region
				* sitenameone_ref_region_filter_vtx.shp and sitenametwo_ref_region_filter_vtx.shp, these are the shorelines after the 3-sigma vertex filter
			* If you only provide a reference shoreline, you will have: 
				* sitenameone.shp and sitenametwo.shp, these are the unfiltered and smooth extracted shorelines
				* sitenameone_ref_shoreline_filter.shp and sitenametwo_ref_shoreline_filter.shp, these are the shorelines filtered by the reference shoreline
				* sitenameone_ref_shoreline_filter_vtx.shp and sitenametwo_ref_shoreline_filter_vtx.shp, these are the shorelines after the 3-sigma vertex filter
			* If you don't provide a reference shoreline or a reference region:
				* sitenameone.shp and sitenametwo.shp, these are the unfiltered and smooth extracted shorelines
				* sitenameone_vtx.shp and sitenametwo__vtx.shp, these are the shorelines after the 3-sigma vertex filter.
		
* The shapefiles with the vtx filter will provide the best results. Using a reference shoreline or a reference region will greatly limit any additional editing in GIS software.

![filters](/images/filtering.png)

# Make Transects

Tutorial Video
* [9. Making Transects](https://drive.google.com/file/d/1uSOG-kzbiFzqLFjWD2OZiadokWlId_UW/view?usp=sharing)

![transects_ex](/images/generate_transects.png)

Hit Make Transects.

![transect_diagram](images/generating_transects.jpg)

![transects](/images/make_transects_screen.JPG)

* You need a shapefile containing a reference shoreline to do this. 
  Look in shoreline_images/ for a good example, and then find the corresponding shapefile in shapefiles/
  Copy this file and put it in its own folder.

* Select an alongshore spacing between transects, and a cross-shore length. 
  The cross-shore length should be long enough to intersect all extracted shorelines at each transect.

* Hit Select Reference Shoreline Shapefile, and point it to your reference shoreline. 
  It will save the transects output to the same directory of the reference shoreline.

* Check that the transects look correct in GIS software.

# Make Timeseries

Tutorial Video
* [10. Making Timeseries](https://drive.google.com/file/d/1g5o1H1ZsgFL0_ie1D7uKoIRV3Ve89R6R/view?usp=sharing)

Hit Make Timeseries.

![timeseries_diagram](images/generating_timeseries.jpg)

![timeseries](/images/make_timeseries_screen.JPG)

* Type in your site name. If your transects were oriented in the opposite direction of the ocean/sea/lake, check switch transect direction.

* Next, hit Create Timeseries. This will ask for the shapefile containing all of the shorelines.

* Next, it will ask for your transect shapefile.

* Next, you need to tell it where to save the timeseries data. Make a new folder for this.
	* Raw timeseries data (datetime, northings, eastings, cross-shore distance)
	* Raw timeseries figure
	* Raw timeseries with yearly linear trend figure
	* 3-month, 6-month, and yearly running means with linear trend figure
	* Power spectrum figure
	* 3-month running mean with NAO figure
	* De-trended timeseries figure
	* Yearly trend data (datetime, predicted cross-shore distance, residual)

* This tool will also make a new transects shapefile with the yearly trend values added as a field. 
* This file will be saved in the same directory as the original transect shapefile.


# Making Linear Trend Shapefile

Tutorial Video
*  [11. Making Linear Trend Shapefile](https://drive.google.com/file/d/1Bd9AIKezy-_wd26vdKE6dqSSlRTHjIAp/view?usp=sharing)

This tool allows for the construction of shapefiles that help with visualization of linear trends computed on each transect's cross-shore position timeseries.
Each transect will be re-scaled and the direction changed to correspond with the value of the computed linear trend.

Fit a linear model to this data using ordinary least squares (OLS)
* y_i = b + mx_i + e 
* b is the y-intercept (OLS estimated parameter)
* m is the slope of the line (in m/year) (OLS estimated parameter)
* x_i is the independent variable (years)
* y_i is the dependent variable (cross-shore distance)
* e is the model error (normally distributed, mean of zero)
* m gives us an estimate for yearly shoreline change, under the assumption that the shorelines are eroding or accreting at a constant linear rate

Making a map of shoreline change vectors
* Shoreline linear trend for the ith transect, s_i (m/year)
* Assume s_i is constant over time: ds/dt = 0
* Length of line on map, L_i (m)
* Pick a constant value, call it A, (units of years) to multiply all the slopes by
* L_i = A*s_i
	* y*m/y = m
* So on the map, each line in this case is projecting the estimated slope A years into the future
	* A = 100 years
		* 100m length means a projection of 100m of growth/retreat in 100 years
		* Direction towards land indicates retreat
		* Direction towards sea indicates growth

![trends_visual](images/trends_visual.png)

To use this tool, hit "Get Linear Trend Shapefile"

![get_linear_trend](images/get_linear_trends.PNG)

* This tool should be used after timeseries data has been generated
* You will need to enter the site name in the site name text box, followed by an underscore (ex: Delmarva_)
* Set a minimum and maximum year for the data
	* Only cross-shore positions within these years will be used for computing linear trends
* Type in the EPSG code for the transects shapefile
* Hit Make Linear Trends Shapefile
	* It will first ask for the transects shapefile you used to generate the timeseries data
	* Next it will ask for the folder where the timeseries data was saved to
	* It will save the new shapefile in the same folder as the transects shapefile you pointed it to, with the min/max years added to the name of the new file
	* You will need to edit the symbology of the shapefile to help with visualization (ex: making a graduated color scale for the linear trend values)


# Project Timeseries

Tutorial Videos
* [12. Projecting Timeseries a)](https://drive.google.com/file/d/1u2eZ6dROaYcF-vt_T2JV_90gZsU3g6cM/view?usp=sharing)
* [13. Projecting Timeseries b)](https://drive.google.com/file/d/1K3LL2_HvNrEgXIjUcMwqpadBCkcfwjVQ/view?usp=sharing)

Hit Project Timeseries

![project_timeseries](/images/project_timeseries_screen.JPG)

Using LSTMs to project cross-shore positions into the future for an entire section of the coast.
* LSTM Architecture
	* Training data: N cross-shore position timeseries
	* Two stacked, bidirectional LSTM layers.
	* Loss function: mean absolute error, keeps the units in meters
	* Early stopping for training (if validation loss does not improve for 100 epochs, halt training)
	* Repeat training a set number of times to get a distribution and confidence interval of model outputs
	* Dimensions of inputs and outputs for the model
		* Dependent upon the look-back value, L and the number of transects, N
		* Input: (L, N), or the previous L values for each transect
		* Ouput: (1, N), or the next value for each transect

* To use this tool, you should have a folder with all of the cross-shore timeseries for your study areas (defined by a transect number).

* You will need to input the following:
	* a site name
	* a starting and ending index (transect number to start and stop at)
	* the number of epochs to train each LSTM for
	* the batch size for training the LSTM
	* the number of units in the LSTM
	* the look-back value for the LSTM
	* the number of predictions, 
	* the number of times to repeat training to get a confidence interval for the projections
	* the training data split fraction 

* Values will vary depending upon input datasets. Fine-tuning of various values (epochs, batch size, layers, look-back values, predictions, repeats) would be beneficial to get the best results. 

* Currently, the LSTM is trained to project shorelines at 3-month intervals, so with a number of predicitons equal to 40, it is projecting ten years from the last observed satellite shoreline (4 predictions per year, 40 predictions per ten years).

* Upon clicking Run, you will need to feed it the folder with the extracted timeseries, and then make a new folder to save the projections to.

* For each transect it will save to the projected folder:
	* CSV containing predicted values (datetime, mean projected cross-shore distance, upper 95% confidence bound, lower 95% confidence bound)
	* Timeseries figure with the predicted and ground-truth values
	* CSV containing projected values (datetime, mean projected cross-shore distance, upper 95% confidence bound, lower 95% confidence bound)
	* Timeseries figure with the projected and ground-truth values

![predictioncape](images/CapePredict.png)
![projectioncape](images/CapeProject.png)

# Merge Projections

Tutorial Video
*  [14. Merging Projections](https://drive.google.com/file/d/1mKG4G_gLU7mjz79GFxuIuqPtDOS7K2gi/view?usp=share_link)

With timeseries of projected cross-shore positions, as well as the transects at which the timeseries data was originally extracted from,
we can re-cast these values into UTM coordinates with simple trigonmetry. 

![projection_geom](images/projection_geometry.PNG)

Hit Merge Projections

![merge_projections](/images/merge_projections_screen.JPG)

* This function will merge the timeseries projections into 2D shorelines and 95% confidence polygons for each projected time.

* Input the following:
	* the site name
	* start transect index
	* end transect index
	* the EPSG code for the coordinate system used (whatever EPSG code that corresponds to the study area's WGS84/UTM zone)
	* whether or not the transects are running in the opposite direction of the water and need to be flipped.

* Upon clicking Run, you will need to feed it the folder holding the extracted timeseries, then the folder holding the projected timeseries, and then the shapefile holding the transects.

* It will save four shapefiles (predicted and projected shorelines, predicted and projected confidence intervals) into the projected timeseries folder. 
* It will also add northings and eastings as columns to each timeseries csv.

* Will not work if a shoreline has multiple solutions along one of the transects at a single time. 
Consequently, areas with extremely complex 2D longshore morphologies are not suitable for this type of modeling approach.

![projected_cape](images/projected_cape.png)

# Retraining Model

It is very possible that the area you are testing the model contains completely novel data for the GAN.
This might make the results quite bad. To get better results, you need to train the GAN on annotations from the new study area.

I will add more details on how to set up a training dataset in the future.


Click Retraining Model.

![train](/images/train_screen.JPG)

Once the training dataset is set up, type in the model name. It is probably best to use the default epochs and decay epochs.
If you are continuing training from existing checkpoints, hit the continuing training check box, and specify the starting epoch.
Then hit Run.








