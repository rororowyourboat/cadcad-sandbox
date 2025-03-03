# cadcad-sandbox

A cadCAD project implementing an SIR (Susceptible, Infected, Recovered) epidemic model simulation with Monte Carlo capabilities and KPI tracking.

## Project Structure

```
cadcad-sandbox/
├── model/               # Main simulation code
│   ├── __init__.py     # Default run configuration
│   ├── __main__.py     # CLI interface
│   ├── types.py        # Type definitions
│   ├── params.py       # Model parameters
│   ├── helper.py       # Helper functions
│   ├── core_logic.py   # Core SIR update logic
│   ├── logic.py        # cadCAD policy wrapper
│   ├── structure.py    # Model blocks definition
│   ├── load_data.py    # Data loading utilities
│   ├── experiment.py   # Simulation execution
│   └── kpi.py         # KPI calculations
├── data/               # Data directory
│   └── simulations/    # Simulation results
├── requirements.txt    # Project dependencies
└── pyproject.toml     # Project metadata and configuration
```

## Setup with uv

This project uses [uv](https://github.com/astral-sh/uv) as the Python package manager for fast, reliable dependency management. The project configuration is managed through `pyproject.toml`, which defines project metadata, dependencies, and development tools configuration.

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Create a new virtual environment:
```bash
uv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. Install project dependencies:
```bash
uv pip install -e .
```

## Package Usage

### Basic Simulation

```python
from model.experiment import SIRSimulation

# Run a single simulation with default parameters
sim = SIRSimulation(timesteps=100, samples=1)
results_df, kpi_summary = sim.run()

# Run with custom parameters
sim = SIRSimulation(
    timesteps=200,
    samples=5,
    beta=0.3,      # transmission rate
    gamma=0.1,     # recovery rate
    population=1000
)
results_df, kpi_summary = sim.run()
```

### Monte Carlo Parameter Sweep

```python
from model.experiment import monte_carlo_sweep

# Define parameter ranges to explore
param_ranges = {
    'beta': (0.2, 0.4),
    'gamma': (0.1, 0.2)
}

# Run Monte Carlo simulations
results = monte_carlo_sweep(
    param_ranges,
    n_samples=10,         # Monte Carlo runs per parameter set
    n_timesteps=100,      # Length of each simulation
    n_parameter_sets=5    # Number of parameter combinations to try
)

# Results contain KPIs for each parameter set
for result in results:
    print(f"Parameters: {result['params']}")
    print(f"KPIs: {result['kpis']}")
```

### Key Performance Indicators (KPIs)

The simulation tracks several important KPIs:

1. **Peak Infections**: Maximum number of infected individuals at any point
2. **Total Infections**: Cumulative number of infections over the simulation
3. **Epidemic Duration**: Time until active infections drop below threshold
4. **Basic Reproduction Number (R0)**: Calculated as β/γ

KPI results include summary statistics for each metric:
- Mean
- Standard deviation
- Minimum
- Maximum
- Median

## Installation and CLI Usage

### Install via pip

Install from local directory:
```bash
pip install -e .
```

Or install from GitHub:
```bash
pip install git+https://github.com/yourusername/cadcad-sandbox.git
```

Check out `examples/github_install_example.py` for a complete example that demonstrates:
- Installing the package from GitHub
- Using the Python API to run simulations
- Using the CLI command

### CLI Usage

After installation, run simulations using the `cadcad-sir` command:
```bash
cadcad-sir --samples 5 --timesteps 200 --experiment "custom_run"
```

Available options:
- `--samples`: Number of simulation samples (default: 1)
- `--timesteps`: Number of timesteps to simulate (default: 100)
- `--output`: Base name for output files (default: results)
- `--experiment`: Experiment name (default: simulation)
- `--beta`: Transmission rate (optional)
- `--gamma`: Recovery rate (optional)
- `--population`: Total population (optional)

Results are saved in `data/simulations/` with timestamp and experiment name.

## Managing Dependencies with uv

- Add a new dependency:
```bash
uv pip install package_name
```

- Add a development dependency:
```bash
uv pip install --dev package_name
```

- Update dependencies:
```bash
uv pip sync requirements.txt
```

- Generate requirements.txt from current environment:
```bash
uv pip freeze > requirements.txt
```

- Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

- Install from pyproject.toml:
```bash
uv pip install -e .
```

uv Benefits:
- Faster package installation than pip
- Built-in virtual environment management
- Reliable dependency resolution
- Improved security with lockfile support
