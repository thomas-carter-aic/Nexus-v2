"""
Predictive Analytics Module

This module provides advanced forecasting, trend prediction, and predictive modeling
capabilities for the AI-Native PaaS Platform.
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
from scipy import stats
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

from .metrics_collector import MetricData, MetricType

logger = logging.getLogger(__name__)


class ForecastModel(Enum):
    """Types of forecasting models"""
    LINEAR_REGRESSION = "linear_regression"
    POLYNOMIAL = "polynomial"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    ARIMA = "arima"
    RANDOM_FOREST = "random_forest"
    SEASONAL_DECOMPOSITION = "seasonal_decomposition"


class ForecastHorizon(Enum):
    """Forecast time horizons"""
    SHORT_TERM = "short_term"    # 1-7 days
    MEDIUM_TERM = "medium_term"  # 1-4 weeks
    LONG_TERM = "long_term"      # 1-6 months


@dataclass
class Forecast:
    """Forecast result"""
    forecast_id: str
    metric_name: str
    model_type: ForecastModel
    horizon: ForecastHorizon
    forecast_values: List[float]
    forecast_timestamps: List[datetime]
    confidence_intervals: List[Tuple[float, float]]
    accuracy_metrics: Dict[str, float]
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'forecast_id': self.forecast_id,
            'metric_name': self.metric_name,
            'model_type': self.model_type.value,
            'horizon': self.horizon.value,
            'forecast_values': self.forecast_values,
            'forecast_timestamps': [ts.isoformat() for ts in self.forecast_timestamps],
            'confidence_intervals': self.confidence_intervals,
            'accuracy_metrics': self.accuracy_metrics,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric_name: str
    trend_type: str  # "linear", "exponential", "seasonal", "cyclical"
    trend_strength: float  # 0.0 to 1.0
    trend_direction: str   # "increasing", "decreasing", "stable"
    seasonality_detected: bool
    seasonal_period: Optional[int] = None
    trend_equation: str = ""
    r_squared: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metric_name': self.metric_name,
            'trend_type': self.trend_type,
            'trend_strength': self.trend_strength,
            'trend_direction': self.trend_direction,
            'seasonality_detected': self.seasonality_detected,
            'seasonal_period': self.seasonal_period,
            'trend_equation': self.trend_equation,
            'r_squared': self.r_squared
        }


@dataclass
class AnomalyPrediction:
    """Anomaly prediction result"""
    metric_name: str
    predicted_anomalies: List[Tuple[datetime, float, float]]  # timestamp, predicted_value, anomaly_score
    anomaly_threshold: float
    model_confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metric_name': self.metric_name,
            'predicted_anomalies': [
                (ts.isoformat(), val, score) 
                for ts, val, score in self.predicted_anomalies
            ],
            'anomaly_threshold': self.anomaly_threshold,
            'model_confidence': self.model_confidence
        }


class PredictiveAnalytics:
    """
    Advanced predictive analytics engine for forecasting and trend analysis
    """
    
    def __init__(self):
        self.forecasts: List[Forecast] = []
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        
    async def create_forecast(self, metrics: List[MetricData], 
                            metric_name: str,
                            horizon: ForecastHorizon = ForecastHorizon.SHORT_TERM,
                            model_type: ForecastModel = ForecastModel.LINEAR_REGRESSION) -> Forecast:
        """Create a forecast for a specific metric"""
        
        # Filter and prepare data
        metric_data = [m for m in metrics if m.name == metric_name]
        if len(metric_data) < 10:
            raise ValueError(f"Insufficient data for forecasting {metric_name}. Need at least 10 data points.")
            
        # Sort by timestamp
        metric_data.sort(key=lambda x: x.timestamp)
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {'timestamp': m.timestamp, 'value': m.value}
            for m in metric_data
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        
        # Determine forecast periods
        forecast_periods = self._get_forecast_periods(horizon)
        
        # Generate forecast based on model type
        if model_type == ForecastModel.LINEAR_REGRESSION:
            forecast = await self._linear_regression_forecast(df, forecast_periods, metric_name)
        elif model_type == ForecastModel.POLYNOMIAL:
            forecast = await self._polynomial_forecast(df, forecast_periods, metric_name)
        elif model_type == ForecastModel.EXPONENTIAL_SMOOTHING:
            forecast = await self._exponential_smoothing_forecast(df, forecast_periods, metric_name)
        elif model_type == ForecastModel.RANDOM_FOREST:
            forecast = await self._random_forest_forecast(df, forecast_periods, metric_name)
        else:
            forecast = await self._linear_regression_forecast(df, forecast_periods, metric_name)
            
        forecast.model_type = model_type
        forecast.horizon = horizon
        
        # Store forecast
        self.forecasts.append(forecast)
        
        return forecast
        
    async def _linear_regression_forecast(self, df: pd.DataFrame, 
                                        forecast_periods: int, 
                                        metric_name: str) -> Forecast:
        """Create linear regression forecast"""
        
        # Prepare features (time-based)
        df_copy = df.copy()
        df_copy['time_index'] = range(len(df_copy))
        
        X = df_copy[['time_index']].values
        y = df_copy['value'].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate predictions
        future_indices = np.arange(len(df_copy), len(df_copy) + forecast_periods).reshape(-1, 1)
        predictions = model.predict(future_indices)
        
        # Calculate confidence intervals (simplified)
        residuals = y - model.predict(X)
        mse = np.mean(residuals ** 2)
        std_error = np.sqrt(mse)
        
        confidence_intervals = [
            (pred - 1.96 * std_error, pred + 1.96 * std_error)
            for pred in predictions
        ]
        
        # Generate future timestamps
        last_timestamp = df.index[-1]
        time_delta = df.index[-1] - df.index[-2] if len(df) > 1 else timedelta(hours=1)
        future_timestamps = [
            last_timestamp + (i + 1) * time_delta 
            for i in range(forecast_periods)
        ]
        
        # Calculate accuracy metrics on training data
        train_predictions = model.predict(X)
        accuracy_metrics = {
            'mae': float(mean_absolute_error(y, train_predictions)),
            'mse': float(mean_squared_error(y, train_predictions)),
            'r_squared': float(model.score(X, y))
        }
        
        return Forecast(
            forecast_id=str(uuid4()),
            metric_name=metric_name,
            model_type=ForecastModel.LINEAR_REGRESSION,
            horizon=ForecastHorizon.SHORT_TERM,
            forecast_values=predictions.tolist(),
            forecast_timestamps=future_timestamps,
            confidence_intervals=confidence_intervals,
            accuracy_metrics=accuracy_metrics
        )
        
    async def _polynomial_forecast(self, df: pd.DataFrame, 
                                 forecast_periods: int, 
                                 metric_name: str) -> Forecast:
        """Create polynomial regression forecast"""
        
        df_copy = df.copy()
        df_copy['time_index'] = range(len(df_copy))
        
        # Create polynomial features
        time_indices = df_copy['time_index'].values
        X = np.column_stack([
            time_indices,
            time_indices ** 2,
            time_indices ** 3
        ])
        y = df_copy['value'].values
        
        # Train model with regularization
        model = Ridge(alpha=1.0)
        model.fit(X, y)
        
        # Generate predictions
        future_indices = np.arange(len(df_copy), len(df_copy) + forecast_periods)
        future_X = np.column_stack([
            future_indices,
            future_indices ** 2,
            future_indices ** 3
        ])
        predictions = model.predict(future_X)
        
        # Calculate confidence intervals
        residuals = y - model.predict(X)
        mse = np.mean(residuals ** 2)
        std_error = np.sqrt(mse)
        
        confidence_intervals = [
            (pred - 1.96 * std_error, pred + 1.96 * std_error)
            for pred in predictions
        ]
        
        # Generate future timestamps
        last_timestamp = df.index[-1]
        time_delta = df.index[-1] - df.index[-2] if len(df) > 1 else timedelta(hours=1)
        future_timestamps = [
            last_timestamp + (i + 1) * time_delta 
            for i in range(forecast_periods)
        ]
        
        # Calculate accuracy metrics
        train_predictions = model.predict(X)
        accuracy_metrics = {
            'mae': float(mean_absolute_error(y, train_predictions)),
            'mse': float(mean_squared_error(y, train_predictions)),
            'r_squared': float(model.score(X, y))
        }
        
        return Forecast(
            forecast_id=str(uuid4()),
            metric_name=metric_name,
            model_type=ForecastModel.POLYNOMIAL,
            horizon=ForecastHorizon.SHORT_TERM,
            forecast_values=predictions.tolist(),
            forecast_timestamps=future_timestamps,
            confidence_intervals=confidence_intervals,
            accuracy_metrics=accuracy_metrics
        )
        
    async def _exponential_smoothing_forecast(self, df: pd.DataFrame, 
                                            forecast_periods: int, 
                                            metric_name: str) -> Forecast:
        """Create exponential smoothing forecast"""
        
        values = df['value'].values
        alpha = 0.3  # Smoothing parameter
        
        # Simple exponential smoothing
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[i-1])
            
        # Forecast future values
        last_smoothed = smoothed[-1]
        predictions = [last_smoothed] * forecast_periods
        
        # Calculate confidence intervals based on historical variance
        residuals = values[1:] - smoothed[:-1]
        std_error = np.std(residuals)
        
        confidence_intervals = [
            (pred - 1.96 * std_error, pred + 1.96 * std_error)
            for pred in predictions
        ]
        
        # Generate future timestamps
        last_timestamp = df.index[-1]
        time_delta = df.index[-1] - df.index[-2] if len(df) > 1 else timedelta(hours=1)
        future_timestamps = [
            last_timestamp + (i + 1) * time_delta 
            for i in range(forecast_periods)
        ]
        
        # Calculate accuracy metrics
        accuracy_metrics = {
            'mae': float(mean_absolute_error(values[1:], smoothed[:-1])),
            'mse': float(mean_squared_error(values[1:], smoothed[:-1])),
            'r_squared': 0.5  # Simplified for exponential smoothing
        }
        
        return Forecast(
            forecast_id=str(uuid4()),
            metric_name=metric_name,
            model_type=ForecastModel.EXPONENTIAL_SMOOTHING,
            horizon=ForecastHorizon.SHORT_TERM,
            forecast_values=predictions,
            forecast_timestamps=future_timestamps,
            confidence_intervals=confidence_intervals,
            accuracy_metrics=accuracy_metrics
        )
        
    async def _random_forest_forecast(self, df: pd.DataFrame, 
                                    forecast_periods: int, 
                                    metric_name: str) -> Forecast:
        """Create random forest forecast"""
        
        # Create features including lags and rolling statistics
        df_copy = df.copy()
        df_copy['time_index'] = range(len(df_copy))
        
        # Add lag features
        for lag in [1, 2, 3, 7]:
            if len(df_copy) > lag:
                df_copy[f'lag_{lag}'] = df_copy['value'].shift(lag)
                
        # Add rolling statistics
        for window in [3, 7]:
            if len(df_copy) > window:
                df_copy[f'rolling_mean_{window}'] = df_copy['value'].rolling(window).mean()
                df_copy[f'rolling_std_{window}'] = df_copy['value'].rolling(window).std()
                
        # Add time-based features
        df_copy['hour'] = df_copy.index.hour
        df_copy['day_of_week'] = df_copy.index.dayofweek
        
        # Drop rows with NaN values
        df_clean = df_copy.dropna()
        
        if len(df_clean) < 10:
            # Fall back to linear regression if not enough data
            return await self._linear_regression_forecast(df, forecast_periods, metric_name)
            
        # Prepare features and target
        feature_cols = [col for col in df_clean.columns if col != 'value']
        X = df_clean[feature_cols].values
        y = df_clean['value'].values
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Generate predictions (simplified - assumes similar patterns continue)
        last_row = df_clean.iloc[-1:][feature_cols].values
        predictions = []
        
        for i in range(forecast_periods):
            pred = model.predict(last_row)[0]
            predictions.append(pred)
            
            # Update features for next prediction (simplified)
            # In practice, this would be more sophisticated
            
        # Calculate confidence intervals using prediction intervals
        # Simplified approach using model variance
        train_predictions = model.predict(X)
        residuals = y - train_predictions
        std_error = np.std(residuals)
        
        confidence_intervals = [
            (pred - 1.96 * std_error, pred + 1.96 * std_error)
            for pred in predictions
        ]
        
        # Generate future timestamps
        last_timestamp = df.index[-1]
        time_delta = df.index[-1] - df.index[-2] if len(df) > 1 else timedelta(hours=1)
        future_timestamps = [
            last_timestamp + (i + 1) * time_delta 
            for i in range(forecast_periods)
        ]
        
        # Calculate accuracy metrics
        accuracy_metrics = {
            'mae': float(mean_absolute_error(y, train_predictions)),
            'mse': float(mean_squared_error(y, train_predictions)),
            'r_squared': float(model.score(X, y))
        }
        
        return Forecast(
            forecast_id=str(uuid4()),
            metric_name=metric_name,
            model_type=ForecastModel.RANDOM_FOREST,
            horizon=ForecastHorizon.SHORT_TERM,
            forecast_values=predictions,
            forecast_timestamps=future_timestamps,
            confidence_intervals=confidence_intervals,
            accuracy_metrics=accuracy_metrics
        )
        
    def _get_forecast_periods(self, horizon: ForecastHorizon) -> int:
        """Get number of forecast periods based on horizon"""
        if horizon == ForecastHorizon.SHORT_TERM:
            return 24  # 24 periods (e.g., hours)
        elif horizon == ForecastHorizon.MEDIUM_TERM:
            return 168  # 1 week in hours
        else:  # LONG_TERM
            return 720  # 1 month in hours
            
    async def analyze_trends(self, metrics: List[MetricData], 
                           metric_name: str) -> TrendAnalysis:
        """Analyze trends in metric data"""
        
        # Filter and prepare data
        metric_data = [m for m in metrics if m.name == metric_name]
        if len(metric_data) < 5:
            raise ValueError(f"Insufficient data for trend analysis of {metric_name}")
            
        # Sort by timestamp
        metric_data.sort(key=lambda x: x.timestamp)
        
        values = np.array([m.value for m in metric_data])
        timestamps = [m.timestamp for m in metric_data]
        
        # Linear trend analysis
        x = np.arange(len(values))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
        
        # Determine trend direction
        if abs(slope) < std_err:
            trend_direction = "stable"
        elif slope > 0:
            trend_direction = "increasing"
        else:
            trend_direction = "decreasing"
            
        # Calculate trend strength
        trend_strength = abs(r_value)
        
        # Detect seasonality (simplified)
        seasonality_detected = False
        seasonal_period = None
        
        if len(values) > 24:  # Need sufficient data
            # Check for daily seasonality (24-hour cycle)
            autocorr_24 = np.corrcoef(values[:-24], values[24:])[0, 1]
            if not np.isnan(autocorr_24) and abs(autocorr_24) > 0.5:
                seasonality_detected = True
                seasonal_period = 24
                
        # Determine trend type
        if seasonality_detected:
            trend_type = "seasonal"
        elif abs(slope) > 0.1 * np.std(values):
            trend_type = "linear"
        else:
            trend_type = "stable"
            
        # Create trend equation
        trend_equation = f"y = {slope:.4f}x + {intercept:.4f}"
        
        return TrendAnalysis(
            metric_name=metric_name,
            trend_type=trend_type,
            trend_strength=trend_strength,
            trend_direction=trend_direction,
            seasonality_detected=seasonality_detected,
            seasonal_period=seasonal_period,
            trend_equation=trend_equation,
            r_squared=r_value ** 2
        )
        
    async def predict_anomalies(self, metrics: List[MetricData], 
                              metric_name: str,
                              forecast_horizon: int = 24) -> AnomalyPrediction:
        """Predict future anomalies in metric data"""
        
        # Filter and prepare data
        metric_data = [m for m in metrics if m.name == metric_name]
        if len(metric_data) < 20:
            raise ValueError(f"Insufficient data for anomaly prediction of {metric_name}")
            
        # Sort by timestamp
        metric_data.sort(key=lambda x: x.timestamp)
        
        values = np.array([m.value for m in metric_data])
        
        # Calculate baseline statistics
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        # Define anomaly threshold (3 sigma rule)
        anomaly_threshold = 3.0
        
        # Create forecast for future values
        forecast = await self.create_forecast(
            metrics, metric_name, 
            ForecastHorizon.SHORT_TERM, 
            ForecastModel.LINEAR_REGRESSION
        )
        
        # Predict anomalies in forecast
        predicted_anomalies = []
        
        for i, (timestamp, predicted_value) in enumerate(
            zip(forecast.forecast_timestamps, forecast.forecast_values)
        ):
            # Calculate anomaly score
            z_score = abs((predicted_value - mean_value) / std_value) if std_value > 0 else 0
            
            if z_score > anomaly_threshold:
                predicted_anomalies.append((timestamp, predicted_value, z_score))
                
        # Calculate model confidence based on forecast accuracy
        model_confidence = forecast.accuracy_metrics.get('r_squared', 0.5)
        
        return AnomalyPrediction(
            metric_name=metric_name,
            predicted_anomalies=predicted_anomalies,
            anomaly_threshold=anomaly_threshold,
            model_confidence=model_confidence
        )
        
    async def get_forecast_accuracy(self, forecast_id: str) -> Dict[str, float]:
        """Get accuracy metrics for a specific forecast"""
        forecast = next((f for f in self.forecasts if f.forecast_id == forecast_id), None)
        
        if not forecast:
            raise ValueError(f"Forecast {forecast_id} not found")
            
        return forecast.accuracy_metrics
        
    async def compare_models(self, metrics: List[MetricData], 
                           metric_name: str) -> Dict[str, Dict[str, float]]:
        """Compare different forecasting models for a metric"""
        
        models_to_test = [
            ForecastModel.LINEAR_REGRESSION,
            ForecastModel.POLYNOMIAL,
            ForecastModel.EXPONENTIAL_SMOOTHING,
            ForecastModel.RANDOM_FOREST
        ]
        
        results = {}
        
        for model_type in models_to_test:
            try:
                forecast = await self.create_forecast(
                    metrics, metric_name, 
                    ForecastHorizon.SHORT_TERM, 
                    model_type
                )
                results[model_type.value] = forecast.accuracy_metrics
            except Exception as e:
                logger.error(f"Error testing {model_type.value}: {e}")
                results[model_type.value] = {'error': str(e)}
                
        return results


# Example usage
async def example_predictive_analytics():
    """Example of using predictive analytics"""
    from .metrics_collector import MetricData, MetricType, MetricUnit
    
    # Create sample time series data
    metrics = []
    base_time = datetime.utcnow() - timedelta(days=7)
    
    for i in range(168):  # 7 days of hourly data
        timestamp = base_time + timedelta(hours=i)
        
        # Simulate CPU usage with trend and seasonality
        trend = i * 0.05  # Slight upward trend
        seasonal = 10 * np.sin(2 * np.pi * i / 24)  # Daily seasonality
        noise = np.random.normal(0, 5)
        cpu_usage = max(0, min(100, 50 + trend + seasonal + noise))
        
        metrics.append(MetricData(
            metric_id=str(uuid4()),
            metric_type=MetricType.RESOURCE_USAGE,
            name="cpu_usage_percentage",
            value=cpu_usage,
            unit=MetricUnit.PERCENTAGE,
            timestamp=timestamp
        ))
        
    # Create predictive analytics engine
    predictor = PredictiveAnalytics()
    
    # Create forecast
    forecast = await predictor.create_forecast(
        metrics, "cpu_usage_percentage", 
        ForecastHorizon.SHORT_TERM, 
        ForecastModel.LINEAR_REGRESSION
    )
    
    print(f"Forecast for {forecast.metric_name}:")
    print(f"Model: {forecast.model_type.value}")
    print(f"Accuracy (R²): {forecast.accuracy_metrics['r_squared']:.3f}")
    print(f"MAE: {forecast.accuracy_metrics['mae']:.2f}")
    print(f"Next 5 predictions:")
    
    for i in range(5):
        ts = forecast.forecast_timestamps[i]
        val = forecast.forecast_values[i]
        ci_low, ci_high = forecast.confidence_intervals[i]
        print(f"  {ts.strftime('%Y-%m-%d %H:%M')}: {val:.1f} ({ci_low:.1f}-{ci_high:.1f})")
        
    # Analyze trends
    trend_analysis = await predictor.analyze_trends(metrics, "cpu_usage_percentage")
    print(f"\nTrend Analysis:")
    print(f"Direction: {trend_analysis.trend_direction}")
    print(f"Strength: {trend_analysis.trend_strength:.3f}")
    print(f"Type: {trend_analysis.trend_type}")
    print(f"Seasonality: {trend_analysis.seasonality_detected}")
    
    # Predict anomalies
    anomaly_prediction = await predictor.predict_anomalies(metrics, "cpu_usage_percentage")
    print(f"\nAnomaly Prediction:")
    print(f"Predicted anomalies: {len(anomaly_prediction.predicted_anomalies)}")
    print(f"Model confidence: {anomaly_prediction.model_confidence:.3f}")
    
    # Compare models
    model_comparison = await predictor.compare_models(metrics, "cpu_usage_percentage")
    print(f"\nModel Comparison:")
    for model, metrics_dict in model_comparison.items():
        if 'r_squared' in metrics_dict:
            print(f"  {model}: R² = {metrics_dict['r_squared']:.3f}")


if __name__ == "__main__":
    asyncio.run(example_predictive_analytics())
