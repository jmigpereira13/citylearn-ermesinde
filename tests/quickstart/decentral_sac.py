from citylearn.agents.sac import SAC as Agent
from citylearn.citylearn import CityLearnEnv
from IPython.display import display
from pathlib import Path

# initialize
#env = CityLearnEnv('citylearn_challenge_2023_phase_2_local_evaluation', central_agent=False)
print('Creating environment...')
env = CityLearnEnv(
    'citylearn_challenge_2023_phase_2_local_evaluation',
    central_agent=False,                  # no SAC descentralizado manténs False
    render_mode='during',                 # 'during' ou 'end'
    render_directory=Path('outputs/ui_exports'),
    render_session_name='decentral_sac'   # nome da simulação (pasta)
)
print('Creating agent...')
model = Agent(env)

# train
print('Training agent...')
model.learn(episodes=2, deterministic_finish=True)
print('Training finished.')

# test
kpis = model.env.evaluate()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')

print('KPIs finais:')
display(kpis)
#print(kpis)