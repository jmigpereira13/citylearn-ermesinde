from citylearn.agents.rbc import BasicRBC as Agent
from citylearn.citylearn import CityLearnEnv
from IPython.display import display

# initialize
env = CityLearnEnv('citylearn_challenge_2023_phase_2_local_evaluation', central_agent=True)
model = Agent(env)

# step through environment and apply agent actions
observations, _ = env.reset()

while not env.terminated:
    actions = model.predict(observations)
    observations, reward, info, terminated, truncated = env.step(actions)

# test
kpis = model.env.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')
display(kpis)