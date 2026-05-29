import json
import os
from pathlib import Path

# raiz onde tens os datasets locais
DATASETS_ROOT = Path(r"C:\proj_dev\CityLearn\datasets")

def summarize_building(schema, dataset_name):
    print(f"\n  Buildings in '{dataset_name}':")
    for b_name, b in schema.get("buildings", {}).items():
        cooling = b.get("cooling_device") or {}
        heating = b.get("heating_device") or {}
        storage = b.get("electrical_storage") or {}
        pv = b.get("pv") or {}

        print(f"    - {b_name}")
        print(f"        cooling_device:   {cooling.get('name')}   attrs: {list((cooling.get('attributes') or {}).keys())}")
        print(f"        heating_device:   {heating.get('name')}   attrs: {list((heating.get('attributes') or {}).keys())}")
        print(f"        electrical_storage: {storage.get('name')} attrs: {list((storage.get('attributes') or {}).keys())}")
        print(f"        pv:               {pv.get('name')}       attrs: {list((pv.get('attributes') or {}).keys())}")

def summarize_files(schema, dataset_path: Path):
    print("  Files referenced in schema:")
    # dataset_info, pricing, carbon, weather, building files, etc.
    for key, val in schema.items():
        if key.endswith("_file") or key.endswith("_filepath"):
            print(f"    {key}: {val}")
    # building-specific filepaths
    for b_name, b in schema.get("buildings", {}).items():
        bf = b.get("building_attributes", {}).get("filepath")
        if bf:
            print(f"    building '{b_name}' file: {bf}")

def peek_building_csv(dataset_path: Path, building_csv_rel: str, max_rows: int = 3):
    import csv
    csv_path = dataset_path / building_csv_rel
    if not csv_path.is_file():
        print(f"      [WARN] CSV not found: {csv_path}")
        return

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        print(f"      columns: {header}")
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
        print(f"      (showing {min(i+1, max_rows)} data rows)")

def main():
    if not DATASETS_ROOT.is_dir():
        print(f"[ERROR] DATASETS_ROOT not found: {DATASETS_ROOT}")
        return

    for ds_dir in sorted(DATASETS_ROOT.iterdir()):
        if not ds_dir.is_dir():
            continue

        schema_path = ds_dir / "schema.json"
        if not schema_path.is_file():
            print(f"\n[SKIP] {ds_dir.name}: no schema.json")
            continue

        print("\n" + "="*70)
        print(f"DATASET: {ds_dir.name}")
        print(f"  schema: {schema_path}")

        with schema_path.open(encoding="utf-8") as f:
            schema = json.load(f)

        # info global
        dataset_info = schema.get("dataset", {})
        print(f"  period_start: {dataset_info.get('period_start')}")
        print(f"  period_end:   {dataset_info.get('period_end')}")
        print(f"  timestep:     {dataset_info.get('timestep')}")
        print(f"  climate_zone: {dataset_info.get('climate_zone')}")

        # buildings e devices
        summarize_building(schema, ds_dir.name)

        # ficheiros
        summarize_files(schema, ds_dir)

        # espreitar 1 building CSV (primeiro da lista)
        buildings = list(schema.get("buildings", {}).items())
        if buildings:
            b_name, b = buildings[0]
            b_file_rel = b.get("building_attributes", {}).get("filepath")
            if b_file_rel:
                print(f"\n  Preview CSV for first building '{b_name}':")
                peek_building_csv(ds_dir, b_file_rel)
        print()

if __name__ == "__main__":
    main()