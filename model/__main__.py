from model.experiment import SIRSimulation
from model.kpi import summarize_kpis
import click
import pandas as pd
import os
import json
from datetime import datetime

@click.command()
@click.option('--samples', default=1, help='Number of samples to run')
@click.option('--timesteps', default=100, help='Timesteps to simulate')
@click.option('--output', default='results', help='Base name for output files')
@click.option('--experiment', default='simulation', help='Experiment name')
@click.option('--beta', type=float, help='Transmission rate (optional)')
@click.option('--gamma', type=float, help='Recovery rate (optional)')
@click.option('--population', type=int, help='Total population (optional)')
def main(samples: int, timesteps: int, output: str, experiment: str,
         beta: float = None, gamma: float = None, population: int = None) -> None:
    """
    Run the SIR model simulation and save the results.
    """
    click.echo("Initializing simulation...")
    sim = SIRSimulation(
        timesteps=timesteps,
        samples=samples,
        beta=beta,
        gamma=gamma,
        population=population
    )

    click.echo("Running simulation...")
    results_df, kpi_summary = sim.run()

    click.echo("\nSimulation complete! Summary of KPIs:")
    for metric, stats in kpi_summary.items():
        click.echo(f"\n{metric}:")
        for stat, value in stats.items():
            click.echo(f"  {stat}: {value:.2f}")

    click.echo("\nSaving results...")
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    experiment = experiment.replace(" ", "_")
    output_filename = f"{experiment}-{timestamp}-{output}"
    write_results(
        results_df,
        kpi_summary,
        os.path.dirname(f"data/simulations/{output_filename}"),
        os.path.basename(output_filename)
    )

    click.echo("\nDone!")

def write_results(df: pd.DataFrame, kpis: dict, directory: str, filename: str) -> None:
    """
    Write the simulation results and KPIs to files.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    sim_filepath = os.path.join(directory, f"{filename}.pkl.gz")
    df.to_pickle(sim_filepath, compression="gzip")
    click.echo(f"Simulation results saved to {sim_filepath}")

    kpi_filepath = os.path.join(directory, f"{filename}_kpis.json")
    with open(kpi_filepath, 'w') as f:
        json.dump(kpis, f, indent=2)
    click.echo(f"KPI results saved to {kpi_filepath}")

if __name__ == "__main__":
    main()
