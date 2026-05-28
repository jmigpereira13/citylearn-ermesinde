import warnings
from citylearn.wrappers import ClippedObservationWrapper, NormalizedObservationWrapper, RLlibSingleAgentWrapper
from ray.rllib.algorithms.sac import SACConfig as Config
from IPython.display import display

warnings.filterwarnings('ignore', category=DeprecationWarning)

# initialize
env_config = {
    'env_kwargs': {
        'schema': 'citylearn_challenge_2023_phase_2_local_evaluation',
    },
    'wrappers': [
        NormalizedObservationWrapper,
        ClippedObservationWrapper
    ]
}
config = (
    Config()
    .environment(RLlibSingleAgentWrapper, env_config=env_config)
)
model = config.build()

# train
for i in range(2):
    _ = model.train()

# test
env = RLlibSingleAgentWrapper(env_config)
observations, _ = env.reset()

while not env.unwrapped.terminated:
    actions = model.compute_single_action(observations, explore=False)
    observations, _, _, _, _ = env.step(actions)

kpis = env.unwrapped.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')
display(kpis)