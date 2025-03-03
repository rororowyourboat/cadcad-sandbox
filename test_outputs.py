from model.experiment import run_sir_model
import pandas as pd
import numpy as np

# Configure pandas display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

print("\n=== Testing Full Results ===")
full_results = run_sir_model(
    timesteps=5,
    samples=2,
    beta=0.3,
    gamma=0.1,
    population=1000,
    output_format='full'
)
print("\nFull Results Shape:", full_results.shape)
print("\nFirst few rows:")
print(full_results.head())

print("\n=== Testing KPI Vector ===")
kpi_vector = run_sir_model(
    timesteps=5,
    samples=2,
    beta=0.3,
    gamma=0.1,
    population=1000,
    output_format='kpi_vector'
)
print("\nKPI Vector Results:")
for kpi_name, stats in kpi_vector.items():
    print(f"\n{kpi_name}:")
    for stat_name, value in stats.items():
        print(f"  {stat_name}: {value}")

print("\n=== Testing KPI Matrix ===")
kpi_matrix = run_sir_model(
    timesteps=5,
    samples=2,
    beta=0.3,
    gamma=0.1,
    population=1000,
    output_format='kpi_matrix'
)
print("\nKPI Matrix Results:")
print(kpi_matrix)
