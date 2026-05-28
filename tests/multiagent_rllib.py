import warnings
from citylearn.wrappers import ClippedObservationWrapper, NormalizedObservationWrapper, RLlibMultiAgentEnv
from ray.rllib.algorithms.sac import SACConfig as Config
from ray.rllib.policy.policy import PolicySpec
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
    .environment(RLlibMultiAgentEnv, env_config=env_config)
    .multi_agent(
        policies={a: PolicySpec() for a in RLlibMultiAgentEnv(env_config)._agent_ids},
        policy_mapping_fn=lambda agent_id, episode, worker, **kwargs: agent_id,
    )
)
model = config.build()

# train
for i in range(2):
    _ = model.train()

# test
env = RLlibMultiAgentEnv(env_config)
observations, _ = env.reset()

while not env.terminated:
    actions = {p: model.compute_single_action(o, policy_id=p, explore=False) for p, o in observations.items()}
    observations, _, _, _, _ = env.step(actions)

kpis = env.unwrapped.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')
display(kpis)