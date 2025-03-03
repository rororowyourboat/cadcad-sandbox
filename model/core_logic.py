import numpy as np

def sir_update(params, substep, state_history, previous_state):
    # Get base parameters
    base_beta = params.get("beta")
    base_gamma = params.get("gamma")
    
    # Add random variation to parameters (±10%)
    beta = base_beta * (1 + np.random.uniform(-0.1, 0.1))
    gamma = base_gamma * (1 + np.random.uniform(-0.1, 0.1))
    S = previous_state.get("S")
    I = previous_state.get("I")
    R = previous_state.get("R")
    population = params.get("population")
    
    # Calculate new infections and recoveries
    new_infections = beta * S * I / population
    new_recoveries = gamma * I

    # Update SIR state using a simple Euler approximation
    new_S = S - new_infections
    new_I = I + new_infections - new_recoveries
    new_R = R + new_recoveries

    return {
         "S": new_S,
         "I": new_I,
         "R": new_R,
    }
