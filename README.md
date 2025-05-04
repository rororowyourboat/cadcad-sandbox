# cadCAD Model API

A REST API wrapper for cadCAD simulation models using FastAPI. This service provides raw simulation results from the SIR (Susceptible, Infected, Recovered) model.

## Quick Start

```bash
# Build and run with Docker
docker build -t cadcad-model .
docker run -p 8000:8000 cadcad-model
```

## API Documentation

### 1. Health Check
```
GET /healthcheck
```
Returns server status and timestamp.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-05-04T21:57:13.754047"
}
```

### 2. Model Metadata
```
GET /metadata
```
Returns model parameters and configuration options.

**Response:**
```json
{
    "name": "SIR Model",
    "parameters": {
        "beta": {
            "type": "number",
            "default": 0.3,
            "min": 0.0,
            "max": 1.0,
            "description": "Transmission rate"
        },
        "gamma": {
            "type": "number",
            "default": 0.1,
            "min": 0.0,
            "max": 1.0,
            "description": "Recovery rate"
        },
        "population": {
            "type": "integer",
            "default": 1000,
            "min": 100,
            "max": 1000000,
            "description": "Total population for scaling"
        }
    },
    "state_variables": ["S", "I", "R"],
    "config": {
        "timesteps": {
            "type": "integer",
            "default": 100,
            "min": 10,
            "max": 1000,
            "description": "Number of timesteps to simulate"
        },
        "samples": {
            "type": "integer",
            "default": 1,
            "min": 1,
            "max": 100,
            "description": "Number of Monte Carlo samples"
        }
    }
}
```

### 3. Run Simulation
```
POST /run
```
Executes a model simulation with the specified parameters and configuration.

**Request Body:**
```json
{
    "parameters": {
        "beta": 0.3,
        "gamma": 0.1,
        "population": 1000
    },
    "config": {
        "timesteps": 100,
        "samples": 1
    }
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "timestep": 0,
                "run": 0,
                "S": 990.0,
                "I": 10.0,
                "R": 0.0
            },
            {
                "timestep": 1,
                "run": 0,
                "S": 987.1,
                "I": 12.7,
                "R": 0.2
            }
        ],
        "parameters": {
            "beta": 0.3,
            "gamma": 0.1,
            "population": 1000
        },
        "config": {
            "timesteps": 100,
            "samples": 1
        }
    },
    "metadata": {
        "execution_time": "0.123s",
        "timestamp": "2025-05-04T21:57:13.754047"
    }
}
```

## Model Details

### State Variables
- `S`: Susceptible population
- `I`: Infected population
- `R`: Recovered population

### Parameters
- `beta`: Transmission rate
- `gamma`: Recovery rate
- `population`: Total population size

## Development

This project uses:
- FastAPI for the REST API
- cadCAD for system modeling
- uv for Python package management
- Docker for containerization

## Deployment

The service is designed to be deployed on Coolify. Set the following environment variables:
- `PORT`: Port for the FastAPI server (default: 8000)
