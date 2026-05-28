import json

# 1) Caminho absoluto para o schema.json
#Schema path para citylearn_challenge_2023_phase_2_local_evaluation
#SCHEMA_PATH = r"C:\proj_dev\CityLearn\datasets\citylearn_challenge_2023_phase_2_local_evaluation\schema.json" 

#Schema path para citylearn_challenge_2022_phase_1
SCHEMA_PATH = r"C:\proj_dev\CityLearn\datasets\citylearn_challenge_2022_phase_1\schema.json"
print("Schema path:", SCHEMA_PATH)

# 2) Carregar o schema
with open(SCHEMA_PATH, encoding="utf-8") as f:
    schema = json.load(f)

# 3) Ver que buildings existem
print("Buildings:", list(schema["buildings"].keys()))

# 4) Escolher um building (por ex. Building_1)
b1 = schema["buildings"]["Building_1"]

# print("\n=== Building_1 parameters ===")
# print("\nCooling device:", b1.get("cooling_device"))
# print("\nHeating device:", b1.get("heating_device"))
# print("\nElectrical storage:", b1.get("electrical_storage"))
# print("\nPV:", b1.get("pv"))

# Flexibilidade de iterar sobre todos os buildings e imprimir seus parâmetros
for name, b in schema["buildings"].items():
    print(f"\n=== {name} ===")
    print("  \n Cooling_device:", b.get("cooling_device"))
    print("  \n Heating_device:", b.get("heating_device"))
    print("  \n Electrical_storage:", b.get("electrical_storage"))
    print("  \n PV:", b.get("pv"))