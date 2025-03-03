from model.core_logic import sir_update
from model.types import Params, PolicyOutput

def p_sir(params: Params, substep: int, state_history: list, previous_state: dict) -> PolicyOutput:
    """
    Policy function for updating the SIR state.
    """
    return sir_update(params, substep, state_history, previous_state)
