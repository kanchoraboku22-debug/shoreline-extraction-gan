"""
Shoreline Extraction GAN - PyQt6 Windows 11 Desktop Application
Complete starter GUI with Fluent Design principles and pipeline integration

Run: python shoreline_gui.py
Requires: pip install PyQt6 PyQt6-Charts
"""

import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QScrollArea, QProgressBar, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget, QDialog,
    QMessageBox, QFileDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QFont, QIcon, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis


# ===== COLORS (Windows 11 Fluent Design) =====
class Colors:
    PRIMARY = "#0078d4"
    PRIMARY_HOVER = "#005a9e"
    SUCCESS = "#107c10"
    WARNING = "#ffb900"
    ERROR = "#d13438"
    BACKGROUND = "#f3f3f3"
    SURFACE = "#ffffff"
    SURFACE_SECONDARY = "#fafafa"
    BORDER = "#e0e0e0"
    TEXT = "#1c1c1c"
    TEXT_SECONDARY = "#616161"


# ===== WORKER THREAD FOR LONG OPERATIONS =====
class PipelineWorker(QThread):
    """Background worker for pipeline operations"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, operation, params=None):
        super().__init__()
        self.operation = operation
        self.params = params or {}

    def run(self):
        try:
            if self.operation == "preprocess":
                self.preprocess()
            elif self.operation == "gan":
                self.run_gan()
            elif self.operation == "extract":
                self.extract_shorelines()
            elif self.operation == "analyze":
                self.analyze_temporal()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def preprocess(self):
        """Simulate preprocessing pipeline"""
        steps = ["Loading imagery...", "Normalizing bands...", "Tiling dataset...", "Preparing GAN input..."]
        for i, step in enumerate(steps):
            self.status_updated.emit(step)
            self.progress_updated.emit((i + 1) * 25)
            self.msleep(500)
        self.finished.emit({"status": "complete", "files": 128})

    def run_gan(self):
        """Simulate GAN inference"""
        for i in range(1, 101, 5):
            self.status_updated.emit(f"GAN Training... Epoch {i//10}/10")
            self.progress_updated.emit(i)
            self.msleep(200)
        self.finished.emit({"status": "complete", "predictions": 128})

    def extract_shorelines(self):
        """Simulate shoreline extraction"""
        steps = ["Applying U-Net...", "Filtering contours...", "Extracting coordinates...", "Exporting vectors..."]
        for i, step in enumerate(steps):
            self.status_updated.emit(step)
            self.progress_updated.emit((i + 1) * 25)
            self.msleep(600)
        self.finished.emit({"status": "complete", "shorelines": 3204})

    def analyze_temporal(self):
        """Simulate temporal analysis"""
        steps = ["Building transects...", "Computing change rates...", "Training LSTM...", "Generating forecasts..."]
        for i, step in enumerate(steps):
            self.status_updated.emit(step)
            self.progress_updated.emit((i + 1) * 25)
            self.msleep(800)
        self.finished.emit({"status": "complete", "forecasts": 124})


# ===== CUSTOM WIDGETS =====
class CardWidget(QFrame):
    """Fluent Design card widget"""
    def __init__(self, title: str, value: str, subtitle: str = ""):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title.upper())
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {Colors.PRIMARY};")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        self.setLayout(layout)


class SidebarButton(QPushButton):
    """Fluent Design sidebar button"""
    def __init__(self, icon: str, label: str):
        super().__init__(f"{icon}  {label}")
        self.setFont(QFont("Segoe UI", 11))
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                color: {Colors.TEXT};
                text-align: left;
                padding: 10px 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.SURFACE_SECONDARY};
                border: 1px solid {Colors.BORDER};
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 120, 212, 0.1);
                border: 1px solid {Colors.PRIMARY};
                color: {Colors.PRIMARY};
            }}
        """)


# ===== MAIN APPLICATION WINDOW =====
class ShorelineGANApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoreline Extraction GAN")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 600)

        # Worker thread
        self.worker = None

        # Initialize UI
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-right: 1px solid {Colors.BORDER};
            }}
        """)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(4)

        # Sidebar Title
        title = QLabel("Shoreline GAN")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title.setFont(title_font)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(12)

        # Navigation buttons
        sidebar_layout.addWidget(QLabel("WORKFLOW"))
        nav_buttons = [
            ("📊", "Dashboard", self.show_dashboard),
            ("📁", "Data", self.show_data),
            ("⚙️", "Preprocess", self.show_preprocess),
            ("🧠", "GAN", self.show_gan),
            ("🌊", "Shorelines", self.show_shorelines),
            ("📈", "Analysis", self.show_analysis),
            ("🎨", "Visualizations", self.show_visualizations),
        ]

        for icon, label, callback in nav_buttons:
            btn = SidebarButton(icon, label)
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(QLabel("APP"))

        settings_btn = SidebarButton("⚡", "Settings")
        settings_btn.clicked.connect(self.show_settings)
        sidebar_layout.addWidget(settings_btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # ===== MAIN CONTENT AREA =====
        content_area = QFrame()
        content_area.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        content_area.setLayout(self.content_layout)

        # Make content scrollable
        scroll = QScrollArea()
        scroll.setWidget(content_area)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        # ===== STATUS BAR =====
        self.status_indicator = QLabel()
        self.status_indicator.setText("● System Ready")
        self.status_indicator.setStyleSheet(f"color: {Colors.SUCCESS};")
        self.statusBar().addWidget(self.status_indicator)

        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(scroll)
        central_widget.setLayout(main_layout)

        # Show dashboard initially
        self.show_dashboard()

    def clear_content(self):
        """Clear main content area"""
        while self.content_layout.count():
            self.content_layout.takeAt(0).widget().deleteLater()

    def show_dashboard(self):
        """Display dashboard page"""
        self.clear_content()

        # Header
        header = QLabel("Dashboard")
        header.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(header)

        # Stats Cards
        stats_layout = QHBoxLayout()
        stats = [
            ("Shorelines Extracted", "3,204", "All time periods"),
            ("Transects Analyzed", "62", "Coastal change metrics"),
            ("Time-Series Points", "248", "30-year observations"),
            ("Forecasts Generated", "124", "2034 & 2044"),
        ]

        for title, value, subtitle in stats:
            stats_layout.addWidget(CardWidget(title, value, subtitle))

        self.content_layout.addLayout(stats_layout)

        # Quick Actions
        self.content_layout.addSpacing(24)
        actions_label = QLabel("Quick Actions")
        actions_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.content_layout.addWidget(actions_label)

        actions_layout = QHBoxLayout()
        actions = [
            ("Preprocess Data", "preprocess", Colors.PRIMARY),
            ("Run GAN", "gan", Colors.PRIMARY),
            ("Extract Shorelines", "extract", Colors.PRIMARY),
            ("Temporal Analysis", "analyze", Colors.PRIMARY),
        ]

        for label, op, color in actions:
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {Colors.PRIMARY_HOVER};
                }}
            """)
            btn.clicked.connect(lambda checked, op=op: self.run_operation(op))
            actions_layout.addWidget(btn)

        self.content_layout.addLayout(actions_layout)

        # Status Panel
        self.content_layout.addSpacing(24)
        status_label = QLabel("Recent Operations")
        status_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.content_layout.addWidget(status_label)

        status_card = QFrame()
        status_card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(20, 20, 20, 20)

        operations = [
            ("GAN Training (2024)", 65),
            ("Shoreline Extraction", 100),
            ("Temporal Analysis", 100),
        ]

        for op_name, progress in operations:
            op_label = QLabel(op_name)
            op_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            status_layout.addWidget(op_label)

            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {Colors.BORDER};
                    border-radius: 2px;
                    height: 4px;
                }}
                QProgressBar::chunk {{
                    background-color: {Colors.PRIMARY};
                }}
            """)
            status_layout.addWidget(progress_bar)
            status_layout.addSpacing(8)

        status_card.setLayout(status_layout)
        self.content_layout.addWidget(status_card)

        self.content_layout.addStretch()

    def show_data(self):
        """Display data management page"""
        self.clear_content()
        title = QLabel("Data Management")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("📁 Upload, manage, and preview satellite imagery datasets."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_preprocess(self):
        self.clear_content()
        title = QLabel("Data Preprocessing")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("⚙️ Harmonization, tiling, and GAN preparation pipeline."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_gan(self):
        self.clear_content()
        title = QLabel("GAN Inference")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("🧠 Run Pix2Pix models for shoreline enhancement."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_shorelines(self):
        self.clear_content()
        title = QLabel("Shoreline Extraction")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("🌊 Extract and export vector shoreline data."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_analysis(self):
        self.clear_content()
        title = QLabel("Temporal Analysis")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("📈 Transect-based change analysis and LSTM forecasting."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_visualizations(self):
        self.clear_content()
        title = QLabel("Visualizations")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.content_layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("🎨 View and export charts, maps, and overlay visualizations."))
        card.setLayout(layout)
        self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def show_settings(self):
        """Display settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setGeometry(400, 300, 500, 400)

        layout = QVBoxLayout()

        # Theme
        theme_label = QLabel("Theme:")
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark", "System"])
        layout.addWidget(theme_label)
        layout.addWidget(theme_combo)

        # GPU
        gpu_label = QLabel("GPU Selection:")
        gpu_combo = QComboBox()
        gpu_combo.addItems(["Automatic", "NVIDIA RTX 3080", "CPU Only"])
        layout.addWidget(gpu_label)
        layout.addWidget(gpu_combo)

        # Batch Size
        batch_label = QLabel("Batch Size:")
        batch_spin = QSpinBox()
        batch_spin.setValue(16)
        batch_spin.setRange(1, 128)
        layout.addWidget(batch_label)
        layout.addWidget(batch_spin)

        layout.addStretch()

        # OK/Cancel buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)
        dialog.exec()

    def run_operation(self, operation):
        """Run a pipeline operation in background"""
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.warning(self, "Operation in Progress", "An operation is already running!")
            return

        self.worker = PipelineWorker(operation)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.finished.connect(self.operation_finished)
        self.worker.error_occurred.connect(self.operation_error)
        self.worker.start()

    def update_progress(self, value):
        """Update progress indicator"""
        self.status_label.setText(f"{value}%")

    def update_status(self, message):
        """Update status message"""
        self.status_indicator.setText(f"● {message}")

    def operation_finished(self, result):
        """Handle operation completion"""
        self.status_indicator.setText("● System Ready")
        self.status_label.setText("")
        QMessageBox.information(self, "Operation Complete", f"✓ {result}")

    def operation_error(self, error):
        """Handle operation error"""
        self.status_indicator.setText("● Error")
        QMessageBox.critical(self, "Error", f"Operation failed:\n{error}")

    def apply_theme(self):
        """Apply Fluent Design theme"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(Colors.BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(Colors.TEXT))
        self.setPalette(palette)


# ===== MAIN ENTRY POINT =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShorelineGANApp()
    window.show()
    sys.exit(app.exec())
