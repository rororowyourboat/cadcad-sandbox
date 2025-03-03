"""
Provides a command-line interface for running the SIR model simulation.
"""

import click
from model.experiment import run_simulation
from datetime import datetime
import os
import pandas as pd

pd.set_option("display.width", None)
pd.set_option("display.max_columns", None)

def write_pickle_results(df: pd.DataFrame, directory: str, filename: str) -> None:
    """
    Write the simulation results to a pickle file.

    Args:
        df (pd.DataFrame): The DataFrame containing simulation results.
        directory (str): The directory to save the file in.
        filename (str): The name of the file to save.
    """
    filepath = os.path.join(directory, filename)

    # Check if the directory exists; create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the DataFrame with gzip compression
    df.to_pickle(filepath, compression="gzip")
    click.echo(f"Results saved to {filepath}.")

@click.command()
@click.option('--samples', default=1, help='Number of samples to run')
@click.option('--timesteps', default=100, help='Timesteps to simulate')
@click.option('--output', default='results.pkl.gz', help='Output file name')
@click.option('--experiment', default='simulation', help='Experiment name')
def main(samples: int, timesteps: int, output: str, experiment: str) -> None:
    """
    Run the SIR model simulation and save the results.
    """
    config = {
        'samples': samples,
        'timesteps': timesteps,
    }

    df = run_simulation(config)

    click.echo(f"Saving results to {output}...")
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    experiment = experiment.replace(" ", "_")
    output_filename = f"data/simulations/{experiment}-{timestamp}-{output}"
    write_pickle_results(df, os.path.dirname(output_filename), os.path.basename(output_filename))

    click.echo("Simulation complete!")

if __name__ == "__main__":
    main()
