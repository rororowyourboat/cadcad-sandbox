# SIR Model Parameters
SIR_PARAMS = {
    "beta": 0.3,         # Transmission rate
    "gamma": 0.1,        # Recovery rate
    "population": 1000,  # Total population for scaling the dynamics
}

SINGLE_RUN_PARAMS = SIR_PARAMS

# Initial state for the SIR model (e.g., 990 susceptible, 10 infected, 0 recovered)
INITIAL_STATE = {
    "S": 990.0,
    "I": 10.0,
    "R": 0.0,
}
