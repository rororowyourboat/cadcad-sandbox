from typing import Dict, Any, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from cadCAD.tools import easy_run  # type: ignore

from model import default_run_args
from model.kpi import calculate_kpis, summarize_kpis
from model.types import Params

class SIRSimulation:
    """
    A class to handle SIR model simulations and KPI calculations.
    """
    
    def __init__(
        self,
        timesteps: int = 100,
        samples: int = 1,
        beta: Optional[float] = None,
        gamma: Optional[float] = None,
        population: Optional[int] = None
    ):
        """
        Initialize simulation parameters.
        
        Args:
            timesteps: Number of timesteps to simulate
            samples: Number of Monte Carlo runs
            beta: Transmission rate (optional, uses default if not provided)
            gamma: Recovery rate (optional, uses default if not provided)
            population: Total population (optional, uses default if not provided)
        """
        self.timesteps = timesteps
        self.samples = samples
        
        # Use provided parameters or defaults
        self.params = dict(default_run_args['params'])
        if beta is not None:
            self.params['beta'] = beta
        if gamma is not None:
            self.params['gamma'] = gamma
        if population is not None:
            self.params['population'] = population

    def _run_sim(self) -> pd.DataFrame:
        """
        Run the simulation and return raw DataFrame.
        
        Returns:
            DataFrame with simulation results
        """
        sim_args = (
            default_run_args['initial_state'],
            self.params,
            default_run_args['model_blocks'],
            self.timesteps,
            self.samples,
        )

        return easy_run(
            *sim_args,
            exec_mode="single",
            assign_params=True,
            deepcopy_off=True,
            supress_print=True
        )

    def get_full_results(self) -> pd.DataFrame:
        """
        Get the complete simulation results DataFrame.
        
        Returns:
            DataFrame containing all simulation data for all runs and timesteps
        """
        return self._run_sim()
    
    def get_kpi_vector(self) -> Dict[str, Dict[str, float]]:
        """
        Get aggregated KPI statistics across all runs.
        
        Returns:
            Dictionary of KPI names mapping to their statistics (mean, std, min, max, median)
        """
        df = self._run_sim()
        kpi_results = []
        
        for run in df['run'].unique():
            run_df = df[df['run'] == run].copy()
            run_df = run_df.sort_values('timestep')
            kpis = calculate_kpis(run_df, self.params)
            kpi_results.append({**kpis, 'run': run})
        
        kpi_df = pd.DataFrame(kpi_results)
        summary = {}
        for column in kpi_df.columns:
            if column != 'run':
                summary[column] = {
                    'mean': float(kpi_df[column].mean()),
                    'std': float(kpi_df[column].std()),
                    'min': float(kpi_df[column].min()),
                    'max': float(kpi_df[column].max()),
                    'median': float(kpi_df[column].median())
                }
        
        return summary
    
    def get_kpi_matrix(self) -> pd.DataFrame:
        """
        Get KPIs for each run in matrix form.
        
        Returns:
            DataFrame where each row is a run and columns are KPIs
        """
        df = self._run_sim()
        kpi_results = []
        
        for run in df['run'].unique():
            run_df = df[df['run'] == run].copy()
            run_df = run_df.sort_values('timestep')
            kpis = calculate_kpis(run_df, self.params)
            kpi_results.append({**kpis, 'run': run})
        
        return pd.DataFrame(kpi_results).set_index('run')

def run_sir_model(
    timesteps: int = 100,
    samples: int = 1,
    beta: Optional[float] = None,
    gamma: Optional[float] = None,
    population: Optional[int] = None,
    output_format: str = 'full'
) -> Union[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """
    Run SIR model simulation with specified parameters and return results in desired format.
    
    Args:
        timesteps: Number of timesteps to simulate
        samples: Number of Monte Carlo runs
        beta: Transmission rate (optional, uses default if not provided)
        gamma: Recovery rate (optional, uses default if not provided)
        population: Total population (optional, uses default if not provided)
        output_format: Type of output to return:
            - 'full': Complete simulation DataFrame
            - 'kpi_vector': Aggregated KPI statistics
            - 'kpi_matrix': KPIs for each run in matrix form
    
    Returns:
        Based on output_format:
        - 'full': DataFrame with all simulation data
        - 'kpi_vector': Dict of KPI statistics
        - 'kpi_matrix': DataFrame of KPIs by run
    """
    sim = SIRSimulation(
        timesteps=timesteps,
        samples=samples,
        beta=beta,
        gamma=gamma,
        population=population
    )
    
    if output_format == 'full':
        return sim.get_full_results()
    elif output_format == 'kpi_vector':
        return sim.get_kpi_vector()
    elif output_format == 'kpi_matrix':
        return sim.get_kpi_matrix()
    else:
        raise ValueError(
            "output_format must be one of: 'full', 'kpi_vector', 'kpi_matrix'"
        )
