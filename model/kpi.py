from typing import Dict, Any, List
import pandas as pd
import numpy as np
from model.types import Params

def calculate_peak_infections(df: pd.DataFrame) -> float:
    """Calculate the maximum number of infected individuals."""
    if df.empty or 'I' not in df.columns:
        print("Warning: DataFrame is empty or 'I' column not found in calculate_peak_infections")
        return 0.0
    # Get maximum I value across all timesteps
    return float(df['I'].max())

def calculate_epidemic_duration(df: pd.DataFrame, threshold: float = 1.0) -> float:
    """Calculate time until active infections drop below threshold."""
    if df.empty or 'I' not in df.columns or 'timestep' not in df.columns:
        print("Warning: DataFrame is empty or required columns not found in calculate_epidemic_duration")
        return 0.0
    
    # Sort by timestep to ensure proper progression
    df_sorted = df.sort_values('timestep')
    
    # Find first timestep where infections drop below threshold
    below_threshold = df_sorted[df_sorted['I'] < threshold]
    if below_threshold.empty:
        return float(df_sorted['timestep'].max())  # If never drops below threshold
    return float(below_threshold.iloc[0]['timestep'])

def calculate_total_infections(df: pd.DataFrame) -> float:
    """Calculate the cumulative number of infections (final R value)."""
    if df.empty:
        print("Warning: DataFrame is empty in calculate_total_infections")
        return 0.0
    if 'R' not in df.columns:
        print(f"Warning: 'R' column not found in DataFrame. Columns: {df.columns}")
        return 0.0
    
    # Sort by timestep and get the final R value
    df_sorted = df.sort_values('timestep')
    return float(df_sorted['R'].iloc[-1])

def calculate_r0(params: Params) -> float:
    """Calculate basic reproduction number (R0 = β/γ)."""
    return params['beta'] / params['gamma']
def calculate_kpis(df: pd.DataFrame, params: Params) -> Dict[str, float]:
    """
    Calculate all KPIs for a single simulation run.
    
    Args:
        df: DataFrame containing simulation results for a single run
        params: Simulation parameters including beta and gamma
    
    Returns:
        Dictionary containing KPI values
    """
    return {
        'peak_infections': calculate_peak_infections(df),
        'total_infections': calculate_total_infections(df),
        'epidemic_duration': calculate_epidemic_duration(df),
        'r0': calculate_r0(params)
    }

def summarize_kpis(df: pd.DataFrame, params: Params) -> Dict[str, Dict[str, float]]:
    """
    Summarize KPIs across multiple simulation runs.
    
    Args:
        df: DataFrame containing simulation results for all runs
        params: Simulation parameters including beta and gamma
    
    Returns:
        Dictionary containing summary statistics for each KPI
    """
    kpi_results = []
    for run in df['run'].unique():
        run_df = df[df['run'] == run]
        kpis = calculate_kpis(run_df, params)
        kpi_results.append(kpis)
    
    kpi_df = pd.DataFrame(kpi_results)
    
    summary = {}
    for column in kpi_df.columns:
        summary[column] = {
            'mean': kpi_df[column].mean(),
            'std': kpi_df[column].std(),
            'min': kpi_df[column].min(),
            'max': kpi_df[column].max(),
            'median': kpi_df[column].median()
        }
    
    return summary
