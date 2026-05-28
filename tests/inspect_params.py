import json

# 1) Caminho absoluto para o schema.json
# SCHEMA_PATH = r"C:\Users\João\AppData\Local\intelligent-environments-lab\citylearn\Cache\v2.5.0\datasets\citylearn_challenge_2023_phase_2_local_evaluation\schema.json"
SCHEMA_PATH = r"C:\Users\João\AppData\Local\intelligent-environments-lab\citylearn\Cache\v2.6.0b2\datasets\citylearn_challenge_2023_phase_2_local_evaluation\schema.json"
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