# Shoreline Extraction GAN - Desktop Application Guide

## 🖥️ PyQt6 GUI Applications

This project includes **three production-ready GUI applications** for executing the shoreline extraction and forecasting pipeline on Windows, macOS, and Linux.

---

## 📋 Application Overview

### 1. **gui_prototype.html** - Visual Mockup
- **Purpose:** Interactive browser-based prototype
- **Technology:** HTML5 + CSS3 + JavaScript
- **Design:** Windows 11 Fluent Design System
- **Usage:** `Open in any modern web browser`

**Features:**
- Sidebar navigation with 8 workflow buttons
- Dashboard with project statistics (3,204 shorelines, 62 transects, etc.)
- Progress bars and operation tracking
- Modal dialogs for settings
- Responsive mobile design

**Best For:**
- Design reference
- Non-technical stakeholders
- Presentations
- Mobile access

---

### 2. **shoreline_gui.py** - Standalone PyQt6 Dashboard
- **Purpose:** Desktop application with Fluent Design
- **Technology:** PyQt6 with native Windows 11 styling
- **Platform:** Windows, macOS, Linux
- **Usage:** `python shoreline_gui.py`

**Features:**
- Modern sidebar navigation
- Dashboard with stat cards
- Quick action buttons
- Background worker threads (non-blocking)
- Settings dialog with GPU/batch configuration
- Page navigation system

**Installation:**
```bash
pip install PyQt6
python shoreline_gui.py
```

**Best For:**
- Local testing and visualization
- Interactive dashboard
- Real-time system monitoring

---

### 3. **shoreline_gui_pipeline.py** - Pipeline Executor
- **Purpose:** Execute all pipeline stages from the GUI
- **Technology:** PyQt6 with subprocess integration
- **Platform:** Windows, macOS, Linux
- **Usage:** `python shoreline_gui_pipeline.py`

**Features:**
- 6 pipeline stage buttons (Load → Preprocess → GAN → Extract → Analysis → Reports)
- Real-time command output in console
- Progress bar with status indicator
- Pipeline validation (checks all scripts exist)
- Error handling and completion messages

**Installation:**
```bash
pip install PyQt6
python shoreline_gui_pipeline.py
```

**Workflow:**
1. Click "Load Data" → Downloads Mombasa satellite imagery
2. Click "Preprocess" → Harmonizes and tiles dataset
3. Click "Run GAN" → Executes Pix2Pix deep learning model
4. Click "Extract Shorelines" → Extracts vector boundaries
5. Click "Temporal Analysis" → Builds transects & LSTM forecasts
6. Click "Generate Reports" → Creates output CSV/visualizations

**Best For:**
- Full pipeline execution
- Production deployment
- Automated workflows

---

### 4. **shoreline_gui_advanced.py** - Advanced Dashboard with Visualizations
- **Purpose:** Complete dashboard with live data visualizations
- **Technology:** PyQt6 + Matplotlib
- **Platform:** Windows, macOS, Linux
- **Usage:** `python shoreline_gui_advanced.py`

**Features:**
- Tabbed interface (5 tabs):
  - **Execution:** Pipeline control and output logging
  - **Transects:** Bar chart of shoreline change rates (62 transects)
  - **Time-Series:** 30-year shoreline position graph
  - **Forecasts:** LSTM predictions for 2034 and 2044
  - **Statistics:** Project overview with key metrics
- Matplotlib embedded charts
- Real-time execution monitoring
- Professional data visualization
- Interactive plot exploration

**Installation:**
```bash
pip install PyQt6 matplotlib
python shoreline_gui_advanced.py
```

**Tabs Explained:**

#### **Execution Tab**
- Pipeline stage buttons
- Real-time output console
- Progress bar with status
- Pipeline validation

#### **Transects Tab**
- Bar chart of 62 transects
- Color-coded change rates (red = erosion, green = accretion)
- Shows coastal change metrics
- Unit: meters per year

#### **Time-Series Tab**
- 30-year shoreline position graph (1994-2024)
- 4 time points: 1994, 2004, 2014, 2024
- Standard deviation shading
- Historical trend visualization

#### **Forecasts Tab**
- LSTM neural network predictions
- Historical data (1994-2024)
- Future forecasts (2034, 2044)
- Uncertainty bounds
- 20-year projection ahead

#### **Statistics Tab**
- Project overview cards:
  - 3,204 shorelines extracted
  - 62 transects analyzed
  - 248 time-series observations
  - 124 forecast predictions
  - 3,265+ output files
  - Study area: Mombasa, Kenya

**Best For:**
- Complete project dashboard
- Scientific presentations
- Data exploration
- Publication-quality visualizations

---

## 🚀 Quick Start

### **Option 1: HTML Prototype (No Installation)**
```bash
# Open in browser
open gui_prototype.html
# OR
start gui_prototype.html  # Windows
```

### **Option 2: Standalone Dashboard**
```bash
pip install PyQt6
python shoreline_gui.py
```

### **Option 3: Pipeline Executor**
```bash
pip install PyQt6
python shoreline_gui_pipeline.py
```

### **Option 4: Advanced Dashboard (Recommended)**
```bash
pip install PyQt6 matplotlib
python shoreline_gui_advanced.py
```

---

## 🔧 System Requirements

### **Hardware**
- CPU: 2+ cores recommended
- RAM: 4 GB minimum, 8 GB recommended
- GPU: NVIDIA CUDA-enabled (optional, for GAN acceleration)

### **Software**
- Python 3.8+
- PyQt6 (for Python GUIs)
- Matplotlib (for advanced visualizations)
- TensorFlow/Keras (for GAN execution)
- GeoPandas (for vector processing)

### **Operating System**
- Windows 10/11
- macOS 10.12+
- Linux (Ubuntu 18.04+)

---

## 📊 Project Architecture

```
Shoreline_Extraction_GAN/
├── gui_prototype.html              ← Visual mockup (HTML/CSS/JS)
├── shoreline_gui.py                ← Standalone dashboard (PyQt6)
├── shoreline_gui_pipeline.py       ← Pipeline executor (PyQt6)
├── shoreline_gui_advanced.py       ← Advanced dashboard (PyQt6 + Matplotlib)
├── scripts/
│   ├── download_mombasa.py         ← Data loader
│   ├── preprocess_mombasa.py       ← Data preprocessor
│   ├── run_pipeline_mombasa.py     ← GAN executor
│   ├── extract_shorelines_simple.py ← Shoreline extractor
│   ├── run_phase3_full.py          ← Temporal analysis
│   └── generate_report.py          ← Report generator
├── utils/                          ← Python utilities (40+ modules)
├── data/                           ← Mombasa satellite imagery
└── model_outputs/                  ← Analysis results (3,265+ files)
```

---

## 🎯 Use Cases

### **Scenario 1: Quick Desktop Dashboard**
```bash
python shoreline_gui.py
```
→ For local testing, visualization, and monitoring

### **Scenario 2: Production Pipeline Execution**
```bash
python shoreline_gui_pipeline.py
```
→ Execute all phases with status updates

### **Scenario 3: Scientific Analysis**
```bash
python shoreline_gui_advanced.py
```
→ Interactive charts and forecasts for research/publications

### **Scenario 4: Non-Technical Presentations**
```bash
open gui_prototype.html
```
→ Share interactive mockup with stakeholders

---

## 📈 Data Visualization Details

### **Transect Analysis**
Shows the shoreline change rate at 62 different measurement profiles:
- **Red bars:** Erosion (negative change)
- **Green bars:** Accretion (positive change)
- **Unit:** Meters per year (m/yr)
- **Time period:** 30-year average

### **Time-Series Graph**
Displays shoreline position over 30 years:
- **X-axis:** Year (1994, 2004, 2014, 2024)
- **Y-axis:** Shoreline position (meters)
- **Shaded area:** ±1 standard deviation
- **Shows:** Mean position and variability

### **LSTM Forecasts**
Predicts future shoreline positions using neural networks:
- **Historical:** 1994-2024 (green solid line)
- **Forecast:** 2024-2044 (yellow dashed line)
- **Uncertainty:** ±2 meter bounds
- **Model:** LSTM recurrent neural network

### **Statistics Dashboard**
Project-wide overview:
- **3,204:** Total shoreline contours extracted
- **62:** Transects for change analysis
- **248:** Time-series observation points
- **124:** Future year predictions
- **3,265+:** Output files generated
- **30 years:** Analysis period (1994-2024)

---

## ⚙️ Configuration

### **GPU Settings** (shoreline_gui.py Settings)
```
Theme: Light / Dark / System
GPU: Automatic / NVIDIA RTX 3080 / CPU Only
Batch Size: 1-128 (default: 16)
```

### **Environment Variables**
```bash
# Force CPU-only execution
export CUDA_VISIBLE_DEVICES=-1

# Enable debug logging
export TF_CPP_MIN_LOG_LEVEL=0
```

### **Pipeline Parameters** (shoreline_gui_pipeline.py)
```python
# In button configuration:
"Run GAN": "python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest"
```

Modify `--year`, `--model`, and `--epoch` as needed.

---

## 🐛 Troubleshooting

### **Issue: PyQt6 won't install**
```bash
# Try conda instead
conda install -c conda-forge pyqt

# Or use PyQt5
pip install PyQt5
```

### **Issue: Matplotlib plots not showing**
```bash
# Ensure backend is correct
pip install matplotlib --upgrade
```

### **Issue: Pipeline scripts not found**
- Use **Validate** button in GUI to check
- Ensure scripts are in `scripts/` directory
- Verify all dependencies are installed

### **Issue: GPU memory error**
- Reduce batch size in Settings
- Close other GPU applications
- Use CPU-only mode: `export CUDA_VISIBLE_DEVICES=-1`

---

## 📚 File Reference

| File | Lines | Purpose |
|------|-------|---------|
| gui_prototype.html | 3,500+ | Browser-based prototype |
| shoreline_gui.py | 600+ | Standalone dashboard |
| shoreline_gui_pipeline.py | 500+ | Pipeline executor |
| shoreline_gui_advanced.py | 800+ | Advanced dashboard with charts |

---

## 🔗 Integration with Scripts

The GUI applications automatically execute these backend scripts:

```python
"📥 Load Data" → scripts/download_mombasa.py
"⚙️ Preprocess" → scripts/preprocess_mombasa.py
"🧠 Run GAN" → scripts/run_pipeline_mombasa.py
"🌊 Extract Shorelines" → scripts/extract_shorelines_simple.py
"📈 Temporal Analysis" → scripts/run_phase3_full.py
"📊 Generate Reports" → scripts/generate_report.py
```

Each button runs the corresponding Python script as a subprocess, maintaining UI responsiveness through multi-threading.

---

## 🚢 Docker Deployment

To run the GUI in Docker:

```bash
docker build -t shoreline-gan:latest .
docker run -it --gpus all -e DISPLAY=$DISPLAY shoreline-gan:latest python shoreline_gui_advanced.py
```

See [Dockerfile](Dockerfile) for details.

---

## 📦 Distribution

### **Standalone Executable** (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile shoreline_gui_advanced.py
```

Creates `dist/shoreline_gui_advanced.exe` for direct execution.

### **Package Distribution**
```bash
python setup.py bdist_wheel
pip install dist/shoreline_gan-1.0.0-py3-none-any.whl
```

---

## ✅ Verification Checklist

Before running the GUI:
- [ ] Python 3.8+ installed
- [ ] PyQt6 installed
- [ ] All scripts in `scripts/` directory
- [ ] Data in `data/` directory
- [ ] TensorFlow/Keras available
- [ ] Matplotlib installed (for advanced dashboard)

---

## 🎓 Academic Use

For thesis or journal submission, use **shoreline_gui_advanced.py** to:
1. Generate publication-quality charts
2. Export visualizations as high-resolution images
3. Document methodology with GUI screenshots
4. Demonstrate interactive analysis workflow

**Export Settings:**
- Right-click on plot → "Save Figure As"
- Format: PNG, PDF, SVG
- DPI: 300 (publication quality)

---

## 📞 Support

If issues occur:

1. **Check validation:** Click "✓ Validate" in the GUI
2. **Review logs:** Console output shows detailed error messages
3. **Check documentation:** See [GITHUB_REPOSITORY_SETUP.md](GITHUB_REPOSITORY_SETUP.md)
4. **Review code:** Scripts are well-commented for debugging

---

## 🎉 Ready to Use!

All three GUI applications are **production-ready** and can be deployed immediately. Choose the one that best fits your use case:

- **HTML Mockup** → Quick reference & presentations
- **Standalone GUI** → Desktop dashboard
- **Pipeline Executor** → Full workflow automation
- **Advanced Dashboard** → Scientific analysis & visualization

Start with the **Advanced Dashboard** for the best experience!

```bash
python shoreline_gui_advanced.py
```

**Happy analyzing! 🚀**

---

*Last Updated: January 16, 2026*  
*All applications tested and verified*
