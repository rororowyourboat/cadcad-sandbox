from typing import Callable, Any

def replace_suf(variable: str, default_value: Any = 0.0) -> Callable:
    return lambda _params, _substep, _history, state, signal: (
        variable,
        signal.get(variable, default_value),
    )

def add_suf(variable: str, default_value: Any = 0.0) -> Callable:
    return lambda _params, _substep, _history, state, signal: (
        variable,
        signal.get(variable, default_value) + state[variable],
    )
