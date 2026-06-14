import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

DATASETS_ROOT = Path(r"C:\proj_dev\CityLearn\datasets")
OUTPUT_CSV = DATASETS_ROOT / "citylearn_dataset_inventory.csv"

ASSET_KEYS = [
    "cooling_device",
    "heating_device",
    "dhw_device",
    "cooling_storage",
    "heating_storage",
    "dhw_storage",
    "electrical_storage",
    "pv",
]

AREA_CANDIDATES = [
    "floor_area",
    "gross_floor_area",
    "conditioned_floor_area",
    "conditioned_area",
    "area",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_get(d: Optional[Dict[str, Any]], *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def first_present(d: Optional[Dict[str, Any]], keys: List[str]):
    if not isinstance(d, dict):
        return None
    for k in keys:
        if d.get(k) is not None:
            return d.get(k)
    return None


def read_csv_header(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            first = f.readline().strip()
        return first.split(",") if first else []
    except Exception:
        return []


def read_area_from_csv(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            first_row = next(reader, None)
        if not first_row:
            return None, None
        for key in AREA_CANDIDATES:
            if key in first_row and first_row[key] not in [None, "", "null"]:
                return key, first_row[key]
        return None, None
    except Exception:
        return None, None


def summarize_asset(asset: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    asset = asset or {}
    attrs = asset.get("attributes") or {}
    return {
        "type": asset.get("type") or asset.get("name"),
        "autosize": asset.get("autosize"),
        "nominal_power": attrs.get("nominal_power"),
        "capacity": attrs.get("capacity"),
        "efficiency": attrs.get("efficiency"),
    }


def main():
    rows: List[Dict[str, Any]] = []

    if not DATASETS_ROOT.exists():
        raise FileNotFoundError(f"DATASETS_ROOT not found: {DATASETS_ROOT}")

    for ds_dir in sorted(DATASETS_ROOT.iterdir()):
        if not ds_dir.is_dir():
            continue

        schema_path = ds_dir / "schema.json"
        if not schema_path.exists():
            continue

        schema = load_json(schema_path)
        buildings = schema.get("buildings") or {}
        observations = schema.get("observations") or {}
        actions = schema.get("actions") or {}

        for b_name, b in buildings.items():
            energy_sim_rel = b.get("energy_simulation")
            energy_sim_path = ds_dir / energy_sim_rel if energy_sim_rel else None
            csv_header = read_csv_header(energy_sim_path) if energy_sim_path and energy_sim_path.exists() else []
            area_field_csv, area_value_csv = read_area_from_csv(energy_sim_path) if energy_sim_path and energy_sim_path.exists() else (None, None)

            cooling = summarize_asset(b.get("cooling_device"))
            heating = summarize_asset(b.get("heating_device"))
            dhw = summarize_asset(b.get("dhw_device"))
            cool_storage = summarize_asset(b.get("cooling_storage"))
            heat_storage = summarize_asset(b.get("heating_storage"))
            dhw_storage = summarize_asset(b.get("dhw_storage"))
            bess = summarize_asset(b.get("electrical_storage"))
            pv = summarize_asset(b.get("pv"))

            building_area_schema = first_present(
                safe_get(b, "attributes", default={}) or b,
                AREA_CANDIDATES,
            )

            row = {
                "dataset_name": ds_dir.name,
                "building_name": b_name,
                "central_agent": schema.get("central_agent"),
                "simulation_start_time_step": schema.get("simulation_start_time_step"),
                "simulation_end_time_step": schema.get("simulation_end_time_step"),
                "seconds_per_time_step": schema.get("seconds_per_time_step"),
                "energy_simulation_file": energy_sim_rel,
                "weather_file": b.get("weather"),
                "pricing_file": b.get("pricing"),
                "carbon_intensity_file": b.get("carbon_intensity"),
                "has_cooling_device": b.get("cooling_device") is not None,
                "cooling_device_type": cooling["type"],
                "cooling_nominal_power": cooling["nominal_power"],
                "cooling_efficiency": cooling["efficiency"],
                "cooling_autosize": cooling["autosize"],
                "has_heating_device": b.get("heating_device") is not None,
                "heating_device_type": heating["type"],
                "heating_nominal_power": heating["nominal_power"],
                "heating_efficiency": heating["efficiency"],
                "heating_autosize": heating["autosize"],
                "has_dhw_device": b.get("dhw_device") is not None,
                "dhw_device_type": dhw["type"],
                "dhw_nominal_power": dhw["nominal_power"],
                "dhw_efficiency": dhw["efficiency"],
                "dhw_autosize": dhw["autosize"],
                "has_cooling_storage": b.get("cooling_storage") is not None,
                "cooling_storage_capacity": cool_storage["capacity"],
                "has_heating_storage": b.get("heating_storage") is not None,
                "heating_storage_capacity": heat_storage["capacity"],
                "has_dhw_storage": b.get("dhw_storage") is not None,
                "dhw_storage_capacity": dhw_storage["capacity"],
                "has_bess": b.get("electrical_storage") is not None,
                "bess_capacity": bess["capacity"],
                "bess_nominal_power": bess["nominal_power"],
                "bess_efficiency": bess["efficiency"],
                "has_pv": b.get("pv") is not None,
                "pv_nominal_power": pv["nominal_power"],
                "building_area_schema": building_area_schema,
                "building_area_csv_field": area_field_csv,
                "building_area_csv_value": area_value_csv,
                "active_observations": ";".join([k for k, v in observations.items() if isinstance(v, dict) and v.get("active")]),
                "active_actions": ";".join([k for k, v in actions.items() if isinstance(v, dict) and v.get("active")]),
                "csv_columns_preview": ";".join(csv_header[:25]),
            }
            rows.append(row)

    fieldnames = list(rows[0].keys()) if rows else ["dataset_name", "building_name"]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Inventory written to: {OUTPUT_CSV}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()