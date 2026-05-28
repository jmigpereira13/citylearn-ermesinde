from citylearn.agents.rbc import BasicRBC as Agent
from citylearn.citylearn import CityLearnEnv
from citylearn.end_use_load_profiles.neighborhood import Neighborhood, SampleMethod
from IPython.display import display

# path to version EnergyPlus 9.6.0 IDD
idd_filepath = 'C:\EnergyPlusV9-6-0\PreProcess\IDFVersionUpdater\V9-6-0-Energy+.idd'

# build a neighborhood with n buildings through random sampling of single-family residential buildings in EULP dataset.
# Sampling population is filtered to include specific county and building vintage.
# train their LSTM thermal dynamics models and generate a CityLearn schema for the two buildings
neighborhood = Neighborhood()
n = 2
neighborhood_build = neighborhood.build(
    idd_filepath=idd_filepath,
    delete_energyplus_simulation_output=True,
    sample_buildings_kwargs=dict(
        sample_method=SampleMethod.RANDOM,
        sample_count=n,
        filters={
            'in.resstock_county_id': ['TX, Travis County'],
            'in.vintage': ['2000s']
        },
    ),
)

# simulate neighborhood in CityLearn
env = CityLearnEnv(neighborhood_build.schema_filepath, central_agent=True)
model = Agent(env)
observations, _ = env.reset()

while not env.terminated:
    actions = model.predict(observations)
    observations, reward, info, terminated, truncated = env.step(actions)

kpis = model.env.evaluate_v2()
kpis = kpis.pivot(index='cost_function', columns='name', values='value').round(3)
kpis = kpis.dropna(how='all')
display(kpis)