from cadCAD.tools import easy_run  # type: ignore
from model import default_run_args
import pandas as pd
from typing import Dict, Any

def run_simulation(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Run the SIR model simulation using easy_run.

    Args:
        config (Dict[str, Any]): Configuration parameters for the simulation.

    Returns:
        pd.DataFrame: The simulation results as a DataFrame.
    """
    sim_args = (
        default_run_args['initial_state'],
        default_run_args['params'],
        default_run_args['model_blocks'],
        config['timesteps'],
        config['samples'],
    )

    print("Running simulation with easy_run...")
    sim_df = easy_run(
        *sim_args,
        exec_mode="single",
        assign_params=True,
        deepcopy_off=True,
    )

    return sim_df
