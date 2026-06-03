import os
import json

CACHE_ROOT = r"C:\proj_dev\CityLearn\datasets"  # ajuste para o caminho do cache local dos datasets

DATASETS = [
    #"citylearn_challenge_2023_phase_2_local_evaluation",
    #"citylearn_challenge_2022_phase_1",
    "baeda_3dem",
    #"tx_travis_county_neighborhood",
    # acrescentar mais nomes se tiver na cache
]

for ds_name in DATASETS:
    schema_path = os.path.join(CACHE_ROOT, ds_name, "schema.json")
    if not os.path.isfile(schema_path):
        print(f"\n[WARN] schema.json não encontrado para {ds_name}")
        continue

    print(f"\n==============================")
    print(f"DATASET: {ds_name}")
    print(f"schema: {schema_path}")

    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    for b_name, b in schema["buildings"].items():
        cooling = b.get("cooling_device") or {}
        heating = b.get("heating_device") or {}
        storage = b.get("electrical_storage") or {}
        pv = b.get("pv") or {}

        print(f"\n--- {b_name} ---")

        if cooling:
            attrs = cooling.get("attributes", {})
            print(f"  Cooling nominal_power: {attrs.get('nominal_power')}")
            print(f"  Cooling efficiency param: {attrs.get('efficiency')}")
        else:
            print("  Cooling: None")

        if storage:
            attrs = storage.get("attributes", {})
            print(f"  Battery capacity: {attrs.get('capacity')} kWh")
            print(f"  Battery nominal_power: {attrs.get('nominal_power')} kW")
            print(f"  Battery efficiency: {attrs.get('efficiency')}")
        else:
            print("  Battery: None")

        if pv:
            attrs = pv.get("attributes", {})
            print(f"  PV nominal_power: {attrs.get('nominal_power')} kWp")
        else:
            print("  PV: None")