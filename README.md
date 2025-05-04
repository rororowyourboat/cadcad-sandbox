# cadcad-sandbox
# Dockerized cadCAD Model

This repository contains a cadCAD model that has been containerized using Docker.

## Prerequisites

- Docker installed on your system
- Git (for cloning the repository)

## Building the Docker Image

To build the Docker image, run the following command from the root directory of the project:

```bash
docker build -t cadcad-model .
```

## Running the Model

To run the model in a container:

```bash
docker run cadcad-model
```

### Development

If you want to mount your local code for development:

```bash
docker run -v ${PWD}/model:/app/model cadcad-model
```

## Project Structure

- `model/` - Contains the cadCAD model implementation
- `Dockerfile` - Defines the Docker container configuration
- `requirements.txt` - Python package dependencies
- `.dockerignore` - Specifies which files should be excluded from the Docker build

## Notes

- The model is built using cadCAD framework
- Uses uv as the Python package manager
- Environment variables in the container:
  - `PYTHONUNBUFFERED=1`: Ensures Python output is sent straight to terminal
  - `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing .pyc files

AjecipmgaSIR(Sa-poib/,Iee   d, R c ve edi ep─ _miy #   l s  ul  swhMnC├─goy  p bia ei.s─aa  KPI   r─ ijg.
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
