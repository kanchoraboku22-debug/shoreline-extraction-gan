"""
Shoreline Extraction GAN - High-Resolution Chart Export Utility
Export publication-quality visualizations (300 DPI) for thesis, journals, and reports

Usage:
    python export_publication_charts.py
    
This creates a publication_exports/ directory with 300 DPI PNG/PDF charts
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from datetime import datetime

# Import the data loader
from utils.realtime_data import ProjectDataLoader


class PublicationChartExporter:
    """Export high-resolution charts for publications"""

    def __init__(self, output_dir: str = "publication_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.loader = ProjectDataLoader(".")
        self.dpi = 300  # Publication quality

    def export_transect_chart(self) -> str:
        """Export transect change rates chart"""
        data = self.loader.load_transect_data()

        fig, ax = plt.subplots(figsize=(14, 7))

        transect_ids = data["transect_ids"]
        change_rates = data["change_rates"]
        colors = ['#d13438' if x < 0 else '#107c10' for x in change_rates]

        bars = ax.bar(transect_ids, change_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=0.7)

        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.2)
        ax.set_xlabel('Transect ID', fontsize=14, fontweight='bold')
        ax.set_ylabel('Shoreline Change Rate (m/year)', fontsize=14, fontweight='bold')
        ax.set_title('Shoreline Change Rates by Transect (Mombasa, 1994-2024)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # Legend
        erosion_patch = mpatches.Patch(color='#d13438', alpha=0.8, label='Erosion (Retreat)')
        accretion_patch = mpatches.Patch(color='#107c10', alpha=0.8, label='Accretion (Advance)')
        ax.legend(handles=[erosion_patch, accretion_patch], fontsize=12, loc='upper right')

        fig.tight_layout()
        output_path = self.output_dir / "01_transect_change_rates.png"
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ Exported: {output_path}")
        plt.close(fig)
        return str(output_path)

    def export_timeseries_chart(self) -> str:
        """Export 30-year time-series chart"""
        data = self.loader.load_timeseries_data()

        fig, ax = plt.subplots(figsize=(12, 7))

        years = data["years"]
        mean = data["mean_position"]
        std = data["std_position"]

        ax.plot(years, mean, 'o-', linewidth=3, markersize=10, color='#0078d4', label='Mean Position')
        ax.fill_between(years, np.array(mean) - np.array(std), np.array(mean) + np.array(std),
                        alpha=0.25, color='#0078d4', label='±1 Std. Dev.')

        ax.set_xlabel('Year', fontsize=14, fontweight='bold')
        ax.set_ylabel('Shoreline Position (m)', fontsize=14, fontweight='bold')
        ax.set_title('30-Year Shoreline Position Time-Series (Mombasa)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=12, loc='upper right')

        # Formatting
        ax.set_xticks(years)
        ax.set_xticklabels(years)

        fig.tight_layout()
        output_path = self.output_dir / "02_timeseries_30year.png"
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ Exported: {output_path}")
        plt.close(fig)
        return str(output_path)

    def export_forecast_chart(self) -> str:
        """Export LSTM forecast chart"""
        data = self.loader.load_forecast_data()

        fig, ax = plt.subplots(figsize=(12, 7))

        years = data["years"]
        position = data["position"]
        lower = data["lower_bound"]
        upper = data["upper_bound"]
        is_forecast = data["is_forecast"]

        # Split historical and forecast
        hist_years = [y for y, f in zip(years, is_forecast) if not f]
        hist_pos = [p for p, f in zip(position, is_forecast) if not f]
        hist_lower = [l for l, f in zip(lower, is_forecast) if not f]
        hist_upper = [u for u, f in zip(upper, is_forecast) if not f]

        forecast_years = [y for y, f in zip(years, is_forecast) if f]
        forecast_pos = [p for p, f in zip(position, is_forecast) if f]
        forecast_lower = [l for l, f in zip(lower, is_forecast) if f]
        forecast_upper = [u for u, f in zip(upper, is_forecast) if f]

        # Plot historical
        ax.plot(hist_years, hist_pos, 'o-', linewidth=3, markersize=9, color='#107c10', label='Historical Data')
        ax.fill_between(hist_years, hist_lower, hist_upper, alpha=0.2, color='#107c10')

        # Plot forecast
        ax.plot(forecast_years, forecast_pos, 's--', linewidth=3, markersize=9, color='#ffb900', label='LSTM Forecast')
        ax.fill_between(forecast_years, forecast_lower, forecast_upper, alpha=0.2, color='#ffb900', label='95% Confidence Interval')

        ax.set_xlabel('Year', fontsize=14, fontweight='bold')
        ax.set_ylabel('Shoreline Position (m)', fontsize=14, fontweight='bold')
        ax.set_title('LSTM Shoreline Forecast (1994-2044)', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=12, loc='upper right')

        fig.tight_layout()
        output_path = self.output_dir / "03_lstm_forecast.png"
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ Exported: {output_path}")
        plt.close(fig)
        return str(output_path)

    def export_statistics_dashboard(self) -> str:
        """Export project statistics as infographic"""
        stats = self.loader.load_project_statistics()

        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('Shoreline Extraction GAN - Project Overview', 
                     fontsize=18, fontweight='bold', y=0.98)

        # Remove axes
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Create stat boxes
        stat_data = [
            ("Shorelines\nExtracted", str(stats.get("shorelines_extracted", 3204)), "#0078d4"),
            ("Transects\nAnalyzed", str(stats.get("transects_analyzed", 62)), "#107c10"),
            ("Time-Series\nPoints", str(stats.get("timeseries_points", 248)), "#ffb900"),
            ("Forecasts\nGenerated", str(stats.get("forecasts_generated", 124)), "#d13438"),
        ]

        # Position boxes in grid
        positions = [(0.15, 0.75), (0.55, 0.75), (0.15, 0.35), (0.55, 0.35)]

        for (title, value, color), (x, y) in zip(stat_data, positions):
            # Box background
            rect = mpatches.FancyBboxPatch((x-0.12, y-0.12), 0.24, 0.18,
                                          boxstyle="round,pad=0.01",
                                          facecolor=color, alpha=0.1,
                                          edgecolor=color, linewidth=2,
                                          transform=fig.transFigure)
            fig.patches.append(rect)

            # Title text
            fig.text(x, y+0.06, title, fontsize=13, fontweight='bold',
                    ha='center', va='center', color=color)

            # Value text
            fig.text(x, y-0.02, value, fontsize=28, fontweight='bold',
                    ha='center', va='center', color=color)

        # Footer
        fig.text(0.5, 0.08, f'Study Area: Mombasa, Kenya | Time Period: 1994-2024 (30 years)',
                fontsize=12, ha='center', style='italic', color='#616161')

        fig.text(0.5, 0.02, f'Generated: {datetime.now().strftime("%B %d, %Y")}',
                fontsize=10, ha='center', color='#999999')

        output_path = self.output_dir / "04_project_statistics.png"
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ Exported: {output_path}")
        plt.close(fig)
        return str(output_path)

    def export_methodology_diagram(self) -> str:
        """Export workflow methodology diagram"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Title
        ax.text(5, 9.5, 'Shoreline Extraction GAN - Methodology', 
                ha='center', fontsize=18, fontweight='bold')

        # Phase boxes
        phases = [
            (1.5, 7, "Phase 1\nShoreline\nExtraction", "#0078d4"),
            (3.5, 7, "Phase 2\nVector\nExport", "#107c10"),
            (5.5, 7, "Phase 3A\nTransect\nAnalysis", "#ffb900"),
            (7.5, 7, "Phase 3B\nTime-Series", "#d13438"),
            (5.5, 4.5, "Phase 3C\nLSTM\nForecasting", "#0078d4"),
        ]

        for x, y, label, color in phases:
            rect = mpatches.FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8,
                                          boxstyle="round,pad=0.05",
                                          facecolor=color, alpha=0.7,
                                          edgecolor=color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')

        # Arrows
        arrow_props = dict(arrowstyle='->', lw=2.5, color='#333333')
        ax.annotate('', xy=(3.0, 7), xytext=(2.1, 7), arrowprops=arrow_props)
        ax.annotate('', xy=(5.0, 7), xytext=(4.1, 7), arrowprops=arrow_props)
        ax.annotate('', xy=(7.0, 7), xytext=(6.1, 7), arrowprops=arrow_props)
        ax.annotate('', xy=(5.5, 4.9), xytext=(6.5, 6.6), arrowprops=arrow_props)
        ax.annotate('', xy=(4.5, 4.9), xytext=(3.5, 6.6), arrowprops=arrow_props)

        # Input/Output
        ax.text(5, 5.7, '3,204 Shorelines | 62 Transects | 248 Observations | 124 Forecasts',
               ha='center', fontsize=11, style='italic', color='#616161', fontweight='bold')

        # Technologies
        tech_text = 'Deep Learning (Pix2Pix) | GIS Analysis | LSTM Forecasting | Python'
        ax.text(5, 3.5, tech_text,
               ha='center', fontsize=10, style='italic', color='#0078d4', fontweight='bold')

        # Study area
        ax.text(5, 2, 'Study Area: Mombasa, Kenya | Time Period: 1994-2024',
               ha='center', fontsize=11, color='#333333', fontweight='bold')

        fig.tight_layout()
        output_path = self.output_dir / "05_methodology_diagram.png"
        fig.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        print(f"✓ Exported: {output_path}")
        plt.close(fig)
        return str(output_path)

    def export_all(self):
        """Export all charts"""
        print("\n" + "="*80)
        print("EXPORTING PUBLICATION-QUALITY CHARTS (300 DPI)")
        print("="*80 + "\n")

        exported_files = [
            self.export_transect_chart(),
            self.export_timeseries_chart(),
            self.export_forecast_chart(),
            self.export_statistics_dashboard(),
            self.export_methodology_diagram(),
        ]

        print("\n" + "="*80)
        print(f"✓ ALL CHARTS EXPORTED SUCCESSFULLY!")
        print("="*80)
        print(f"\nOutput Directory: {self.output_dir}")
        print(f"Total Files: {len(exported_files)}")
        print(f"Resolution: {self.dpi} DPI (Publication Quality)")
        print(f"\nFiles ready for:")
        print("  ✓ Thesis/Dissertation")
        print("  ✓ Journal Articles")
        print("  ✓ Conference Presentations")
        print("  ✓ Reports & Publications")
        print("\n")

        return exported_files


if __name__ == "__main__":
    exporter = PublicationChartExporter()
    exporter.export_all()
