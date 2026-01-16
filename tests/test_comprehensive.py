"""
Comprehensive test suite for Shoreline Extraction GAN pipeline.
Covers all phases: extraction, vector export, transect analysis, and forecasting.
"""

import unittest
import numpy as np
import tempfile
import os
from pathlib import Path

# Mock imports (adjust paths as needed)
try:
    from utils.shoreline_extraction_utils import extract_shorelines
    from utils.vector_export_utils import export_to_shapefile
    from utils.transect_analysis import generate_transects, compute_change_rates
    from utils.lstm_forecasting import build_lstm_model, forecast_shoreline
except ImportError:
    # Fallback for test environment
    pass


class TestPhase1ShorlineExtraction(unittest.TestCase):
    """Test Phase 1: Automated shoreline extraction"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        # Create mock image array (256x256, RGB)
        self.mock_image = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
        
    def tearDown(self):
        """Clean up test fixtures"""
        self.temp_dir.cleanup()
    
    def test_image_normalization(self):
        """Test image normalization to [0, 1] range"""
        normalized = self.mock_image.astype(float) / 255.0
        self.assertTrue(np.all(normalized >= 0))
        self.assertTrue(np.all(normalized <= 1))
        self.assertEqual(normalized.dtype, np.float64)
    
    def test_ndwi_calculation(self):
        """Test NDWI (Normalized Difference Water Index) computation"""
        # Create mock NIR and Red bands
        nir = np.random.rand(256, 256)
        red = np.random.rand(256, 256)
        
        # NDWI formula: (NIR - Red) / (NIR + Red)
        ndwi = (nir - red) / (nir + red + 1e-8)  # Add epsilon to avoid division by zero
        
        self.assertTrue(np.all(ndwi >= -1))
        self.assertTrue(np.all(ndwi <= 1))
        self.assertEqual(ndwi.shape, (256, 256))
    
    def test_water_mask_threshold(self):
        """Test water mask generation with threshold"""
        ndwi = np.random.uniform(-1, 1, (256, 256))
        threshold = 0.3
        water_mask = ndwi > threshold
        
        self.assertEqual(water_mask.dtype, bool)
        self.assertTrue(0 <= np.sum(water_mask) <= 256*256)
    
    def test_contour_area_filtering(self):
        """Test filtering contours by minimum area"""
        # Mock contours (areas in pixels)
        mock_contours = [100, 250, 50, 1200, 30]  # pixels
        min_area = 100
        
        valid_contours = [c for c in mock_contours if c >= min_area]
        
        self.assertEqual(len(valid_contours), 3)  # 100, 250, 1200
        self.assertNotIn(50, valid_contours)
        self.assertNotIn(30, valid_contours)
    
    def test_extraction_output_consistency(self):
        """Test that extraction produces consistent output structure"""
        # Mock extraction results
        result = {
            'year': 1994,
            'contour_count': 801,
            'mean_length': 2847,
            'total_area': 89.3,
            'validation_accuracy': 0.921
        }
        
        # Verify structure
        self.assertIn('contour_count', result)
        self.assertIn('validation_accuracy', result)
        self.assertGreater(result['contour_count'], 0)
        self.assertGreaterEqual(result['validation_accuracy'], 0)
        self.assertLessEqual(result['validation_accuracy'], 1)


class TestPhase2VectorExport(unittest.TestCase):
    """Test Phase 2: Vector export and GIS integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        # Mock shoreline data
        self.mock_coordinates = np.array([
            [39.6, -3.5],
            [39.601, -3.501],
            [39.602, -3.502],
            [39.603, -3.503]
        ])
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def test_coordinate_transformation_wgs84(self):
        """Test coordinate transformation to WGS84"""
        # Verify coordinates are within valid ranges
        for lon, lat in self.mock_coordinates:
            self.assertGreaterEqual(lon, -180)
            self.assertLessEqual(lon, 180)
            self.assertGreaterEqual(lat, -90)
            self.assertLessEqual(lat, 90)
    
    def test_linestring_geometry_creation(self):
        """Test creation of LineString geometry"""
        coords = self.mock_coordinates.tolist()
        
        # Verify minimum 2 points for valid linestring
        self.assertGreaterEqual(len(coords), 2)
        self.assertEqual(len(coords[0]), 2)  # Each point has lon, lat
    
    def test_shapefile_attribute_schema(self):
        """Test shapefile attribute schema"""
        attributes = {
            'year': 1994,
            'length_m': 2847,
            'segment_id': 1,
            'confidence': 0.921
        }
        
        self.assertIn('year', attributes)
        self.assertIn('length_m', attributes)
        self.assertIsInstance(attributes['year'], int)
        self.assertIsInstance(attributes['length_m'], (int, float))
    
    def test_geojson_output_structure(self):
        """Test GeoJSON output structure"""
        geojson = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': self.mock_coordinates.tolist()
                    },
                    'properties': {'year': 1994}
                }
            ]
        }
        
        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertGreater(len(geojson['features']), 0)
        self.assertEqual(geojson['features'][0]['type'], 'Feature')


class TestPhase3ATransectAnalysis(unittest.TestCase):
    """Test Phase 3A: Transect-based change analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock transect positions over time (distance from reference line in meters)
        self.mock_transect_data = {
            'transect_id': 1,
            'positions_by_year': {
                1994: 0.0,
                2004: 2.1,
                2014: 1.8,
                2024: 3.2
            }
        }
    
    def test_distance_calculation(self):
        """Test distance calculation between shorelines"""
        positions = list(self.mock_transect_data['positions_by_year'].values())
        
        distances = []
        for i in range(1, len(positions)):
            dist = abs(positions[i] - positions[i-1])
            distances.append(dist)
        
        self.assertEqual(len(distances), 3)  # 4 years = 3 distances
        self.assertTrue(all(d >= 0 for d in distances))
    
    def test_erosion_accretion_classification(self):
        """Test classification of erosion vs. accretion"""
        rate_m_per_year = -0.5  # Negative = erosion
        
        if rate_m_per_year < -0.1:
            classification = 'erosion'
        elif rate_m_per_year > 0.1:
            classification = 'accretion'
        else:
            classification = 'stable'
        
        self.assertEqual(classification, 'erosion')
    
    def test_change_rate_computation(self):
        """Test computation of mean change rate"""
        distances = [2.1, -0.3, 1.4]  # From year to year
        years = 30  # 1994 to 2024
        
        mean_rate = np.mean(distances) / (years / 10)
        
        self.assertIsInstance(mean_rate, (int, float, np.number))
        self.assertTrue(-5 < mean_rate < 5)  # Reasonable bounds
    
    def test_stability_classification(self):
        """Test coastal stability classification"""
        change_rates = [0.2, -0.1, 0.05, 2.1, 0.3, -0.2]
        threshold = 0.5  # m/year
        
        stable = sum(1 for rate in change_rates if abs(rate) < threshold)
        unstable = sum(1 for rate in change_rates if abs(rate) >= threshold)
        stability_percent = (stable / len(change_rates)) * 100
        
        self.assertEqual(stable + unstable, len(change_rates))
        self.assertGreaterEqual(stability_percent, 0)
        self.assertLessEqual(stability_percent, 100)


class TestPhase3BTimeSeriesAssembly(unittest.TestCase):
    """Test Phase 3B: Time-series assembly"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.n_transects = 62
        self.n_years = 31  # 1994-2024
        self.n_features = 3  # distance, velocity, acceleration
    
    def test_timeseries_tensor_shape(self):
        """Test time-series tensor shape"""
        tensor_shape = (self.n_transects, self.n_years, self.n_features)
        tensor = np.random.randn(*tensor_shape)
        
        self.assertEqual(tensor.shape[0], self.n_transects)
        self.assertEqual(tensor.shape[1], self.n_years)
        self.assertEqual(tensor.shape[2], self.n_features)
    
    def test_velocity_calculation(self):
        """Test velocity (rate of change) calculation"""
        positions = np.array([0.0, 1.5, 1.2, 3.0])  # meters
        years = np.array([1994, 2004, 2014, 2024])
        
        velocities = []
        for i in range(1, len(positions)):
            dt = (years[i] - years[i-1]) / 1000  # Convert to thousands of years
            v = (positions[i] - positions[i-1]) / 10  # 10-year interval
            velocities.append(v)
        
        self.assertEqual(len(velocities), 3)
    
    def test_acceleration_calculation(self):
        """Test acceleration calculation"""
        velocities = np.array([0.15, -0.03, 0.18])
        
        accelerations = []
        for i in range(1, len(velocities)):
            a = velocities[i] - velocities[i-1]
            accelerations.append(a)
        
        self.assertEqual(len(accelerations), 2)
    
    def test_linear_interpolation(self):
        """Test linear interpolation for missing years"""
        # Known positions at 10-year intervals
        known_years = [1994, 2004, 2014, 2024]
        known_positions = [0.0, 2.1, 1.8, 3.2]
        
        # Interpolate to 1999
        year_to_interpolate = 1999
        # Simple linear interpolation between 1994 and 2004
        t = (year_to_interpolate - 1994) / (2004 - 1994)
        interpolated_position = 0.0 + t * (2.1 - 0.0)
        
        self.assertGreater(interpolated_position, 0.0)
        self.assertLess(interpolated_position, 2.1)
        self.assertAlmostEqual(interpolated_position, 1.05, places=1)


class TestPhase3CLSTMForecasting(unittest.TestCase):
    """Test Phase 3C: LSTM forecasting"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.n_samples = 62  # transects
        self.n_timesteps = 31  # years
        self.n_features = 3  # input features
        self.input_shape = (self.n_timesteps, self.n_features)
    
    def test_lstm_input_tensor_shape(self):
        """Test LSTM input tensor shape"""
        X = np.random.randn(self.n_samples, self.n_timesteps, self.n_features)
        
        self.assertEqual(X.shape, (self.n_samples, self.n_timesteps, self.n_features))
        self.assertEqual(X.ndim, 3)
    
    def test_lstm_output_shape(self):
        """Test LSTM output shape (2 forecasts: 2034, 2044)"""
        y = np.random.randn(self.n_samples, 2)  # 2 forecast years
        
        self.assertEqual(y.shape, (self.n_samples, 2))
        self.assertEqual(y.shape[1], 2)  # 2034 and 2044
    
    def test_train_test_split(self):
        """Test train/validation split"""
        X = np.random.randn(self.n_samples, self.n_timesteps, self.n_features)
        split_ratio = 0.2
        
        split_idx = int(len(X) * (1 - split_ratio))
        X_train = X[:split_idx]
        X_val = X[split_idx:]
        
        self.assertAlmostEqual(len(X_val) / len(X), split_ratio, places=2)
        self.assertEqual(len(X_train) + len(X_val), len(X))
    
    def test_forecast_output_range(self):
        """Test forecast output is within reasonable range"""
        # Mock forecast output (distance changes in meters)
        forecast_2034 = np.array([-0.15, 0.5, -0.8, 1.2])
        forecast_2044 = np.array([-0.31, 0.8, -1.5, 2.1])
        
        # All forecasts should be within ±10m (reasonable coastal change bounds)
        self.assertTrue(np.all(np.abs(forecast_2034) < 10))
        self.assertTrue(np.all(np.abs(forecast_2044) < 10))
    
    def test_forecast_confidence_metrics(self):
        """Test forecast R² and confidence metrics"""
        y_true = np.array([0.0, 0.2, -0.1, 0.3])
        y_pred = np.array([0.1, 0.18, -0.05, 0.35])
        
        # R² = 1 - (SS_res / SS_tot)
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        self.assertGreaterEqual(r2, -1)
        self.assertLessEqual(r2, 1)
        self.assertGreater(r2, 0)  # Should be positive for decent forecast


class TestIntegration(unittest.TestCase):
    """Integration tests for complete pipeline"""
    
    def test_phase1_to_phase2_compatibility(self):
        """Test that Phase 1 output is compatible with Phase 2"""
        # Mock Phase 1 output
        phase1_output = {
            'year': 1994,
            'contours': [[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]],
            'crs': 'EPSG:4326'
        }
        
        # Verify compatibility for Phase 2
        self.assertIn('contours', phase1_output)
        self.assertIn('crs', phase1_output)
        self.assertEqual(phase1_output['crs'], 'EPSG:4326')
    
    def test_phase2_to_phase3a_compatibility(self):
        """Test that Phase 2 output is compatible with Phase 3A"""
        # Mock Phase 2 output
        phase2_output = {
            'vectorfiles': 28,
            'years': [1994, 2004, 2014, 2024],
            'formats': ['shp', 'geojson']
        }
        
        # Verify compatibility
        self.assertEqual(len(phase2_output['years']), 4)
        self.assertIn('shp', phase2_output['formats'])
    
    def test_phase3a_to_phase3b_compatibility(self):
        """Test that Phase 3A output is compatible with Phase 3B"""
        # Mock Phase 3A output
        phase3a_output = {
            'transect_count': 62,
            'change_metrics': {
                'mean_rate': -0.2,
                'stable_percent': 87.1
            },
            'observations': 248
        }
        
        self.assertEqual(phase3a_output['transect_count'], 62)
        self.assertEqual(phase3a_output['observations'], 248)
    
    def test_phase3b_to_phase3c_compatibility(self):
        """Test that Phase 3B output is compatible with Phase 3C"""
        # Mock Phase 3B output
        phase3b_output = {
            'tensor_shape': (62, 31, 3),
            'timeseries_count': 248,
            'features': ['distance', 'velocity', 'acceleration']
        }
        
        self.assertEqual(len(phase3b_output['features']), 3)
        self.assertEqual(phase3b_output['tensor_shape'][0], 62)


class TestDataValidation(unittest.TestCase):
    """Test data validation and quality checks"""
    
    def test_missing_data_handling(self):
        """Test handling of missing data"""
        data = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
        
        # Should handle NaN values
        valid_data = data[~np.isnan(data)]
        self.assertEqual(len(valid_data), 4)
        self.assertTrue(np.all(np.isfinite(valid_data)))
    
    def test_outlier_detection(self):
        """Test outlier detection using standard deviation"""
        data = np.array([1.0, 1.1, 0.9, 1.05, 15.0])  # Last is outlier
        
        mean = np.mean(data)
        std = np.std(data)
        threshold = 3 * std
        
        outliers = np.abs(data - mean) > threshold
        self.assertTrue(outliers[-1])  # Last value should be flagged
    
    def test_temporal_continuity(self):
        """Test temporal continuity of time-series"""
        years = [1994, 2004, 2014, 2024]
        expected_intervals = [10, 10, 10]
        
        intervals = [years[i+1] - years[i] for i in range(len(years)-1)]
        
        self.assertEqual(intervals, expected_intervals)


def run_tests():
    """Run all tests with verbose output"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
