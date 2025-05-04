from fastapi import FastAPI, HTTPException
from pydantic.v1 import BaseModel, Field
from typing import Dict, Any, Optional, List, TypeVar, Union, Literal
import json
from time import time
from datetime import datetime
import uvicorn
import pandas as pd

from model.experiment import SIRSimulation

app = FastAPI(
    title="cadCAD SIR Model API",
    description="REST API for running SIR model simulations",
    version="1.0.0"
)

# Load metadata on startup
with open("metadata.json", "r") as f:
    METADATA: Dict[str, Any] = json.load(f)

T = TypeVar('T', bound=BaseModel)

class SimulationParameters(BaseModel):
    class Config:
        extra = 'forbid'
    
    beta: Optional[float] = Field(None, description="Transmission rate")
    gamma: Optional[float] = Field(None, description="Recovery rate")
    population: Optional[int] = Field(None, description="Total population")

class SimulationConfig(BaseModel):
    class Config:
        extra = 'forbid'
    
    timesteps: int = Field(
        METADATA["config"]["timesteps"]["default"],
        description="Number of timesteps to simulate"
    )
    samples: int = Field(
        METADATA["config"]["samples"]["default"],
        description="Number of Monte Carlo samples"
    )

class SimulationRequest(BaseModel):
    class Config:
        extra = 'forbid'
    
    parameters: SimulationParameters
    config: SimulationConfig

class SimulationMetadata(BaseModel):
    class Config:
        extra = 'forbid'
    
    execution_time: str
    timestamp: str

class SimulationData(BaseModel):
    class Config:
        extra = 'forbid'
    
    results: List[Dict[str, Any]]
    parameters: Dict[str, Union[float, int, None]]
    config: Dict[str, int]

class SimulationResponse(BaseModel):
    class Config:
        extra = 'forbid'
    
    success: bool
    data: SimulationData
    metadata: SimulationMetadata

@app.get("/healthcheck", response_model=Dict[str, str])
async def healthcheck() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metadata", response_model=Dict[str, Any])
async def get_metadata() -> Dict[str, Any]:
    """Return model metadata including parameters and configuration options."""
    return METADATA

@app.post("/run", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest) -> SimulationResponse:
    """Run a simulation with the specified parameters and configuration."""
    try:
        start_time = time()
        
        # Initialize simulation with provided parameters
        sim = SIRSimulation(
            timesteps=request.config.timesteps,
            samples=request.config.samples,
            beta=request.parameters.beta,
            gamma=request.parameters.gamma,
            population=request.parameters.population
        )

        # Run simulation and get results
        results = sim.run()
        results_dict = results.to_dict(orient="records")
        
        execution_time = time() - start_time

        # Prepare response
        data = SimulationData(
            results=results_dict,
            parameters=request.parameters.dict(exclude_none=True),
            config=request.config.dict(exclude_none=True)
        )

        metadata = SimulationMetadata(
            execution_time=f"{execution_time:.3f}s",
            timestamp=datetime.now().isoformat()
        )
        
        return SimulationResponse(
            success=True,
            data=data,
            metadata=metadata
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running simulation: {str(e)}"
        )

def run_server() -> None:
    """Run the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()
