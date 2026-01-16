"""
Shoreline Extraction GAN - PyQt6 GUI with Full Pipeline Integration
Executes all project phases (Load → Preprocess → GAN → Extract → Analyze) directly from the GUI

Run: python shoreline_gui_pipeline.py
Requires: pip install PyQt6
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QMessageBox, QTextEdit, QProgressBar, QScrollArea
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import sys
import subprocess
import os


# ===== COLORS (Windows 11 Fluent Design) =====
class Colors:
    PRIMARY = "#0078d4"
    SUCCESS = "#107c10"
    WARNING = "#ffb900"
    ERROR = "#d13438"
    BACKGROUND = "#f3f3f3"
    SURFACE = "#ffffff"
    BORDER = "#e0e0e0"
    TEXT = "#1c1c1c"
    TEXT_SECONDARY = "#616161"


# ===== WORKER THREAD FOR PIPELINE EXECUTION =====
class PipelineWorker(QThread):
    """Background worker thread for running pipeline commands"""
    status_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, command, stage_name):
        super().__init__()
        self.command = command
        self.stage_name = stage_name
        self.is_running = True

    def run(self):
        try:
            self.status_signal.emit(f"🚀 Starting: {self.stage_name}...\n")
            self.progress_signal.emit(10)

            # Run the command as subprocess
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.getcwd()
            )

            output_lines = []
            for line in process.stdout:
                if not self.is_running:
                    process.terminate()
                    break
                output_lines.append(line.strip())
                self.status_signal.emit(line.strip())

            process.wait()
            self.progress_signal.emit(90)

            if process.returncode == 0:
                self.progress_signal.emit(100)
                self.finished_signal.emit(True, f"✓ {self.stage_name} completed successfully!")
            else:
                self.finished_signal.emit(False, f"✗ {self.stage_name} failed with code {process.returncode}")

        except Exception as e:
            self.finished_signal.emit(False, f"✗ Exception in {self.stage_name}: {str(e)}")

    def stop(self):
        self.is_running = False


# ===== MAIN APPLICATION WINDOW =====
class ShorelineGANPipelineApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoreline Extraction GAN - Pipeline Executor")
        self.setGeometry(100, 100, 1300, 800)
        self.setMinimumSize(1100, 700)

        # Worker thread
        self.worker = None
        self.current_stage = None

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR WITH PIPELINE STAGES =====
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-right: 1px solid {Colors.BORDER};
            }}
        """)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)

        # Title
        title = QLabel("Shoreline GAN")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title.setFont(title_font)
        sidebar_layout.addWidget(title)

        subtitle = QLabel("Pipeline Executor")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle_font.setItalic(True)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(20)

        # Pipeline stages
        sidebar_layout.addWidget(QLabel("PIPELINE STAGES"))

        self.stage_buttons = {}
        stages = [
            ("📥", "Load Data", "python scripts/download_mombasa.py"),
            ("⚙️", "Preprocess", "python scripts/preprocess_mombasa.py"),
            ("🧠", "Run GAN", "python scripts/run_pipeline_mombasa.py --year 2014 --model shoreline_gan_nov --epoch latest"),
            ("🌊", "Extract Shorelines", "python scripts/extract_shorelines_simple.py"),
            ("📈", "Temporal Analysis", "python scripts/run_phase3_full.py"),
            ("📊", "Generate Reports", "python scripts/generate_report.py"),
        ]

        for emoji, label, command in stages:
            btn = self.create_stage_button(f"{emoji} {label}", command, label)
            self.stage_buttons[label] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(QLabel("UTILITIES"))

        # Utility buttons
        validate_btn = self.create_utility_button("✓ Validate")
        validate_btn.clicked.connect(self.validate_pipeline)
        sidebar_layout.addWidget(validate_btn)

        clear_btn = self.create_utility_button("🗑️ Clear Log")
        clear_btn.clicked.connect(lambda: self.output_text.clear())
        sidebar_layout.addWidget(clear_btn)

        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)

        # ===== MAIN CONTENT AREA =====
        content = QFrame()
        content.setStyleSheet(f"background-color: {Colors.BACKGROUND};")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(16)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 16, 20, 16)

        header_title = QLabel("Pipeline Execution Dashboard")
        header_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(header_title)

        instructions = QLabel(
            "📋 Execute pipeline stages in order: Load Data → Preprocess → Run GAN → Extract Shorelines → Analysis → Reports"
        )
        instructions.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        instructions.setFont(QFont("Segoe UI", 10))
        instructions.setWordWrap(True)
        header_layout.addWidget(instructions)

        header_frame.setLayout(header_layout)
        content_layout.addWidget(header_frame)

        # Status card
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(20, 16, 20, 16)

        status_label = QLabel("Status")
        status_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        status_layout.addWidget(status_label)

        self.status_indicator = QLabel("● Ready to execute")
        self.status_indicator.setStyleSheet(f"color: {Colors.SUCCESS}; font-size: 11pt;")
        status_layout.addWidget(self.status_indicator)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BORDER};
                border-radius: 4px;
                height: 6px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
                border-radius: 2px;
            }}
        """)
        self.progress_bar.setValue(0)
        status_layout.addWidget(self.progress_bar)

        status_frame.setLayout(status_layout)
        content_layout.addWidget(status_frame)

        # Output console
        console_label = QLabel("Execution Output")
        console_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        content_layout.addWidget(console_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                font-family: 'Courier New';
                font-size: 10pt;
                padding: 12px;
            }}
        """)
        content_layout.addWidget(self.output_text, 1)

        content.setLayout(content_layout)

        # Add to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, 1)
        central_widget.setLayout(main_layout)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_stage_button(self, label: str, command: str, stage_name: str) -> QPushButton:
        """Create a pipeline stage button"""
        btn = QPushButton(label)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setMinimumHeight(44)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.execute_stage(command, stage_name))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                color: {Colors.TEXT};
                padding: 10px 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: #f5f5f5;
                border: 1px solid {Colors.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 120, 212, 0.05);
            }}
        """)
        return btn

    def create_utility_button(self, label: str) -> QPushButton:
        """Create utility button"""
        btn = QPushButton(label)
        btn.setFont(QFont("Segoe UI", 10))
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SURFACE};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
                color: {Colors.TEXT_SECONDARY};
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: #f5f5f5;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        return btn

    def execute_stage(self, command: str, stage_name: str):
        """Execute a pipeline stage"""
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.warning(
                self,
                "Operation in Progress",
                f"Please wait for {self.current_stage} to complete before starting a new stage."
            )
            return

        self.current_stage = stage_name
        self.output_text.append(f"\n{'='*80}")
        self.output_text.append(f"STARTING: {stage_name.upper()}")
        self.output_text.append(f"Command: {command}")
        self.output_text.append(f"{'='*80}\n")

        self.status_indicator.setText(f"● Running: {stage_name}")
        self.status_indicator.setStyleSheet(f"color: {Colors.WARNING}; font-size: 11pt;")
        self.progress_bar.setValue(0)

        self.worker = PipelineWorker(command, stage_name)
        self.worker.status_signal.connect(self.append_output)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.stage_finished)
        self.worker.start()

    def append_output(self, message: str):
        """Append message to output console"""
        if message.strip():
            self.output_text.append(message)
            # Auto-scroll to bottom
            self.output_text.verticalScrollBar().setValue(
                self.output_text.verticalScrollBar().maximum()
            )

    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def stage_finished(self, success: bool, message: str):
        """Handle stage completion"""
        self.output_text.append(f"\n{'='*80}")
        self.output_text.append(message)
        self.output_text.append(f"{'='*80}\n")

        if success:
            self.status_indicator.setText(f"● {message}")
            self.status_indicator.setStyleSheet(f"color: {Colors.SUCCESS}; font-size: 11pt;")
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Stage Complete", message)
        else:
            self.status_indicator.setText(f"● {message}")
            self.status_indicator.setStyleSheet(f"color: {Colors.ERROR}; font-size: 11pt;")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "Stage Failed", message)

        self.statusBar().showMessage(message)

    def validate_pipeline(self):
        """Validate pipeline setup"""
        checks = {
            "scripts/download_mombasa.py": "Data download script",
            "scripts/preprocess_mombasa.py": "Preprocessing script",
            "scripts/run_pipeline_mombasa.py": "GAN execution script",
            "scripts/extract_shorelines_simple.py": "Shoreline extraction script",
            "scripts/run_phase3_full.py": "Temporal analysis script",
            "scripts/generate_report.py": "Report generation script",
        }

        missing = []
        for script, description in checks.items():
            if not os.path.exists(script):
                missing.append(f"  ✗ {description} ({script})")

        if missing:
            message = "Missing pipeline scripts:\n\n" + "\n".join(missing)
            QMessageBox.warning(self, "Validation Failed", message)
            self.append_output(f"\n⚠️  VALIDATION ERROR: {len(missing)} scripts missing")
        else:
            message = "✓ All pipeline scripts found!\n\nReady to execute."
            QMessageBox.information(self, "Validation Successful", message)
            self.append_output("\n✓ VALIDATION PASSED: All pipeline scripts present")


# ===== MAIN ENTRY POINT =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShorelineGANPipelineApp()
    window.show()
    sys.exit(app.exec())
