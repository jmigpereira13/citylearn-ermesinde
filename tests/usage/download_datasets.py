from citylearn.data import DataSet

DATASETS = [
    #"citylearn_challenge_2023_phase_2_local_evaluation", #comment/uncomment set of datasets to download
    #"citylearn_challenge_2022_phase_1",
    #"baeda_3dem",
    "tx_travis_county_neighborhood"
]

#target_dir = r"C:\proj_dev\CityLearn\datasets\citylearn_challenge_2023_phase_2_local_evaluation"
#target_dir = r"C:\proj_dev\CityLearn\datasets\citylearn_challenge_2022_phase_1"
#target_dir = r"C:\proj_dev\CityLearn\datasets\baeda_3dem"
target_dir = r"C:\proj_dev\CityLearn\datasets\tx_travis_county_neighborhood"

ds = DataSet()

for name in DATASETS:
    schema_filepath = ds.get_dataset(name, directory=target_dir)
    print(f"{name} -> {schema_filepath}")