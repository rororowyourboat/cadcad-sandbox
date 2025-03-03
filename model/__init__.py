from model.params import SINGLE_RUN_PARAMS, INITIAL_STATE
from model.structure import MODEL_BLOCKS

default_run_args = {
    'initial_state': INITIAL_STATE,
    'params': SINGLE_RUN_PARAMS,
    'model_blocks': MODEL_BLOCKS,
    'timesteps': 100,
    'samples': 1
}
