from typing import TypedDict, Dict, Any, List

class SIRState(TypedDict):
    S: float  # Susceptible individuals
    I: float  # Infected individuals
    R: float  # Recovered individuals

Params = Dict[str, Any]
PolicyOutput = Dict[str, Any]
Substep = int
StateHistory = List[Dict[str, Any]]
