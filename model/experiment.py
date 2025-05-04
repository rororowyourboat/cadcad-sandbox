from typing import Dict, Any, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from cadCAD.tools import easy_run  # type: ignore

from model import default_run_args
from model.types import Params

class SIRSimulation:
    """
    A class to handle SIR model simulations.
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
            # Scale initial state proportionally with population
            scale_factor = population / self.params['population']
            self.params['population'] = population
            self.initial_state = {
                'S': default_run_args['initial_state']['S'] * scale_factor,
                'I': default_run_args['initial_state']['I'] * scale_factor,
                'R': default_run_args['initial_state']['R'] * scale_factor
            }
        else:
            self.initial_state = dict(default_run_args['initial_state'])

    def run(self) -> pd.DataFrame:
        """
        Run the simulation and return results DataFrame.
        
        Returns:
            DataFrame containing simulation results for all runs and timesteps
        """
        sim_args = (
            self.initial_state,
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

def run_sir_model(
    timesteps: int = 100,
    samples: int = 1,
    beta: Optional[float] = None,
    gamma: Optional[float] = None,
    population: Optional[int] = None
) -> pd.DataFrame:
    """
    Run SIR model simulation with specified parameters.
    
    Args:
        timesteps: Number of timesteps to simulate
        samples: Number of Monte Carlo runs
        beta: Transmission rate (optional, uses default if not provided)
        gamma: Recovery rate (optional, uses default if not provided)
        population: Total population (optional, uses default if not provided)
    
    Returns:
        DataFrame containing simulation results
    """
    sim = SIRSimulation(
        timesteps=timesteps,
        samples=samples,
        beta=beta,
        gamma=gamma,
        population=population
    )
    
    return sim.run()
