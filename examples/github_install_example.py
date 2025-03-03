"""
Example script demonstrating how to install and use cadcad-sandbox directly from GitHub.

To run this example:
1. First install the package:
   pip install git+https://github.com/yourusername/cadcad-sandbox.git

2. Then run this script:
   python github_install_example.py
"""
from model.experiment import SIRSimulation
import subprocess
import sys

def main():
    print("Running SIR simulation example...")
    
    # Create and run a simulation with custom parameters
    sim = SIRSimulation(
        timesteps=150,
        samples=3,
        beta=0.3,      # transmission rate
        gamma=0.1,     # recovery rate
        population=1000
    )
    
    # Run simulation and get results
    results_df, kpi_summary = sim.run()
    
    # Print KPI summary
    print("\nSimulation KPI Summary:")
    for metric, stats in kpi_summary.items():
        print(f"\n{metric}:")
        for stat, value in stats.items():
            print(f"  {stat}: {value:.2f}")
    
    # Demonstrate CLI usage
    print("\nDemonstrating CLI usage...")
    subprocess.run([
        "cadcad-sir",
        "--samples", "2",
        "--timesteps", "100",
        "--experiment", "github_example",
        "--beta", "0.3",
        "--gamma", "0.1",
        "--population", "1000"
    ])

if __name__ == "__main__":
    main()
