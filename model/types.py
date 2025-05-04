from typing import TypedDict, Dict, Any, List, Union, Sequence

class SIRState(TypedDict):
    S: float  # Susceptible individuals
    I: float  # Infected individuals
    R: float  # Recovered individuals

class SIRParams(TypedDict):
    beta: float        # Transmission rate
    gamma: float       # Recovery rate
    population: int    # Total population

class DefaultRunArgs(TypedDict):
    initial_state: SIRState
    params: SIRParams
    model_blocks: List[Any]  # cadCAD specific type
    timesteps: int
    samples: int

Params = Dict[str, Any]
PolicyOutput = Dict[str, Any]
Substep = int
StateHistory = List[Dict[str, Any]]
