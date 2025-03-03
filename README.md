# cadcad-sandbox

A cadCAD project implementing an SIR (Susceptible, Infected, Recovered) epidemic model simulation.

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
│   └── experiment.py   # Simulation execution
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
uv pip install -r requirements.txt
```

## Usage

Run a simulation with default parameters:
```bash
python -m model
```

Customize simulation parameters:
```bash
python -m model --samples 5 --timesteps 200 --experiment "custom_run"
```

Options:
- `--samples`: Number of simulation samples (default: 1)
- `--timesteps`: Number of timesteps to simulate (default: 100)
- `--output`: Output file name (default: results.pkl.gz)
- `--experiment`: Experiment name for output file (default: simulation)

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
