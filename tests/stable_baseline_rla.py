from stable_baselines3.sac import SAC as Agent
from citylearn.citylearn import CityLearnEnv
from citylearn.wrappers import NormalizedObservationWrapper, StableBaselines3Wrapper
from IPython.display import display

# initialize
env = CityLearnEnv('citylearn_challenge_2023_phase_2_local_evaluation', central_agent=True)
env = NormalizedObservationWrapper(env)
env = StableBaselines3Wrapper(env)
model = Agent('MlpPolicy', env)

# train
episodes = 2
model.learn(total_timesteps=env.unwrapped.time_steps*episodes)

# test
observations, _ = env.reset()

while not env.unwrapped.terminated:
    actions, _ = model.predict(observations, deterministic=True)
    observations, _, _, _, _ = env.step(actions)

kpis = env.unwrapped.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')
display(kpis)