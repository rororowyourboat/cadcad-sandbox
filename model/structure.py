from copy import deepcopy
from model.logic import p_sir

MODEL_BLOCKS = [
    {
        "label": "SIR Dynamics",
        "ignore": False,
        "desc": "Updates the SIR state based on the SIR model dynamics",
        "policies": {"sir_policy": p_sir},
        "variables": {
            "S": lambda _params, _substep, _history, state, signal: ("S", signal.get("S", state["S"])),
            "I": lambda _params, _substep, _history, state, signal: ("I", signal.get("I", state["I"])),
            "R": lambda _params, _substep, _history, state, signal: ("R", signal.get("R", state["R"])),
        },
    },
]
