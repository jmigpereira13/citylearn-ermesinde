# python .\schema_comparison.py `
#   C:\proj_dev\CityLearn\datasets\baeda_3dem\schema.json `
#   C:\proj_dev\CityLearn\datasets\citylearn_challenge_2023_phase_2_evaluation\schema.json `
#   --label-a baeda_3dem `
#   --label-b challenge_2023

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Union

SchemaLike = Union[Dict[str, Any], str, Path]


def load_schema(schema_or_path: SchemaLike) -> Dict[str, Any]:
    if isinstance(schema_or_path, dict):
        return schema_or_path
    path = Path(schema_or_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _fmt(v: Any) -> str:
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _active_keys(section: Dict[str, Any]) -> Set[str]:
    return {k for k, v in section.items() if isinstance(v, dict) and v.get("active")}


def _present_assets(building: Dict[str, Any]) -> Set[str]:
    return {
        k for k in [
            "cooling_device", "heating_device", "dhw_device", "cooling_storage",
            "heating_storage", "dhw_storage", "electrical_storage", "pv"
        ] if building.get(k) is not None
    }


def _building_summary(schema: Dict[str, Any], building_name: str) -> Dict[str, Any]:
    building = schema.get("buildings", {}).get(building_name, {})
    observations = schema.get("observations", {})
    actions = schema.get("actions", {})
    inactive_obs = set(building.get("inactive_observations", []))
    inactive_actions = set(building.get("inactive_actions", []))
    effective_obs = {k for k, v in observations.items() if v.get("active") and k not in inactive_obs}
    effective_actions = {k for k, v in actions.items() if v.get("active") and k not in inactive_actions}
    dynamics = building.get("dynamics") or {}
    dynamics_attr = dynamics.get("attributes") or {}
    return {
        "type": building.get("type"),
        "include": building.get("include"),
        "energy_simulation": building.get("energy_simulation"),
        "weather": building.get("weather"),
        "pricing": building.get("pricing"),
        "carbon_intensity": building.get("carbon_intensity"),
        "assets": _present_assets(building),
        "inactive_observations": inactive_obs,
        "inactive_actions": inactive_actions,
        "effective_observations": effective_obs,
        "effective_actions": effective_actions,
        "dynamics_type": dynamics.get("type"),
        "dynamics_inputs": set(dynamics_attr.get("input_observation_names", [])),
        "dynamics_file": dynamics_attr.get("filename"),
        "dynamics_hidden_size": dynamics_attr.get("hidden_size"),
        "dynamics_num_layers": dynamics_attr.get("num_layers"),
        "dynamics_lookback": dynamics_attr.get("lookback"),
    }


def compare_schemas(schema_a: SchemaLike, schema_b: SchemaLike, label_a: str = "schema_a", label_b: str = "schema_b") -> List[str]:
    a = load_schema(schema_a)
    b = load_schema(schema_b)
    lines: List[str] = []

    lines.append(f"COMPARE: {label_a} vs {label_b}")
    lines.append("")
    lines.append("GLOBAL SETTINGS")
    for key in [
        "central_agent", "simulation_start_time_step", "simulation_end_time_step",
        "seconds_per_time_step", "rolling_episode_split", "random_episode_split"
    ]:
        lines.append(f"- {key}: {label_a}={_fmt(a.get(key))} | {label_b}={_fmt(b.get(key))}")

    lines.append("")
    lines.append("AGENT")
    lines.append(f"- type: {label_a}={a.get('agent', {}).get('type')} | {label_b}={b.get('agent', {}).get('type')}")
    a_agent_attrs = a.get("agent", {}).get("attributes") or {}
    b_agent_attrs = b.get("agent", {}).get("attributes") or {}
    for key in sorted(set(a_agent_attrs) | set(b_agent_attrs)):
        lines.append(f"- agent.{key}: {label_a}={_fmt(a_agent_attrs.get(key))} | {label_b}={_fmt(b_agent_attrs.get(key))}")

    lines.append("")
    lines.append("REWARD")
    lines.append(f"- type: {label_a}={a.get('reward_function', {}).get('type')} | {label_b}={b.get('reward_function', {}).get('type')}")
    lines.append(f"- attributes: {label_a}={_fmt(a.get('reward_function', {}).get('attributes'))} | {label_b}={_fmt(b.get('reward_function', {}).get('attributes'))}")

    lines.append("")
    lines.append("GLOBAL OBSERVATIONS")
    a_obs = a.get("observations", {})
    b_obs = b.get("observations", {})
    obs_keys = sorted(set(a_obs) | set(b_obs))
    for key in obs_keys:
        av = a_obs.get(key)
        bv = b_obs.get(key)
        lines.append(
            f"- {key}: {label_a}={'MISSING' if av is None else ('ON' if av.get('active') else 'OFF')} | {label_b}={'MISSING' if bv is None else ('ON' if bv.get('active') else 'OFF')}"
        )
    lines.append(f"- active_only_in_{label_a}: {_fmt(sorted(_active_keys(a_obs) - _active_keys(b_obs)))}")
    lines.append(f"- active_only_in_{label_b}: {_fmt(sorted(_active_keys(b_obs) - _active_keys(a_obs)))}")

    lines.append("")
    lines.append("GLOBAL ACTIONS")
    a_act = a.get("actions", {})
    b_act = b.get("actions", {})
    act_keys = sorted(set(a_act) | set(b_act))
    for key in act_keys:
        av = a_act.get(key)
        bv = b_act.get(key)
        lines.append(
            f"- {key}: {label_a}={'MISSING' if av is None else ('ON' if av.get('active') else 'OFF')} | {label_b}={'MISSING' if bv is None else ('ON' if bv.get('active') else 'OFF')}"
        )
    lines.append(f"- active_only_in_{label_a}: {_fmt(sorted(_active_keys(a_act) - _active_keys(b_act)))}")
    lines.append(f"- active_only_in_{label_b}: {_fmt(sorted(_active_keys(b_act) - _active_keys(a_act)))}")

    lines.append("")
    lines.append("BUILDINGS OVERVIEW")
    a_buildings = set(a.get("buildings", {}))
    b_buildings = set(b.get("buildings", {}))
    lines.append(f"- building_names_{label_a}: {_fmt(sorted(a_buildings))}")
    lines.append(f"- building_names_{label_b}: {_fmt(sorted(b_buildings))}")
    lines.append(f"- only_in_{label_a}: {_fmt(sorted(a_buildings - b_buildings))}")
    lines.append(f"- only_in_{label_b}: {_fmt(sorted(b_buildings - a_buildings))}")

    common = sorted(a_buildings & b_buildings)
    lines.append("")
    lines.append("COMMON BUILDINGS DETAIL")
    for building_name in common:
        sa = _building_summary(a, building_name)
        sb = _building_summary(b, building_name)
        lines.append(f"- {building_name}")
        for key in [
            "include", "type", "energy_simulation", "weather", "pricing", "carbon_intensity",
            "dynamics_type", "dynamics_file", "dynamics_hidden_size", "dynamics_num_layers", "dynamics_lookback"
        ]:
            lines.append(f"  - {key}: {label_a}={_fmt(sa.get(key))} | {label_b}={_fmt(sb.get(key))}")
        lines.append(f"  - assets_only_in_{label_a}: {_fmt(sorted(sa['assets'] - sb['assets']))}")
        lines.append(f"  - assets_only_in_{label_b}: {_fmt(sorted(sb['assets'] - sa['assets']))}")
        lines.append(f"  - inactive_observations_only_in_{label_a}: {_fmt(sorted(sa['inactive_observations'] - sb['inactive_observations']))}")
        lines.append(f"  - inactive_observations_only_in_{label_b}: {_fmt(sorted(sb['inactive_observations'] - sa['inactive_observations']))}")
        lines.append(f"  - inactive_actions_only_in_{label_a}: {_fmt(sorted(sa['inactive_actions'] - sb['inactive_actions']))}")
        lines.append(f"  - inactive_actions_only_in_{label_b}: {_fmt(sorted(sb['inactive_actions'] - sa['inactive_actions']))}")
        lines.append(f"  - effective_observations_only_in_{label_a}: {_fmt(sorted(sa['effective_observations'] - sb['effective_observations']))}")
        lines.append(f"  - effective_observations_only_in_{label_b}: {_fmt(sorted(sb['effective_observations'] - sa['effective_observations']))}")
        lines.append(f"  - effective_actions_only_in_{label_a}: {_fmt(sorted(sa['effective_actions'] - sb['effective_actions']))}")
        lines.append(f"  - effective_actions_only_in_{label_b}: {_fmt(sorted(sb['effective_actions'] - sa['effective_actions']))}")
        lines.append(f"  - dynamics_inputs_only_in_{label_a}: {_fmt(sorted(sa['dynamics_inputs'] - sb['dynamics_inputs']))}")
        lines.append(f"  - dynamics_inputs_only_in_{label_b}: {_fmt(sorted(sb['dynamics_inputs'] - sa['dynamics_inputs']))}")

    lines.append("")
    lines.append("INCONSISTENCY HINTS")
    for label, schema in [(label_a, a), (label_b, b)]:
        global_obs = schema.get("observations", {})
        for building_name in schema.get("buildings", {}):
            s = _building_summary(schema, building_name)
            for obs_name in sorted(s["dynamics_inputs"]):
                g = global_obs.get(obs_name)
                if g is None:
                    lines.append(f"- {label}:{building_name}: dynamics input '{obs_name}' not defined globally")
                elif not g.get("active"):
                    lines.append(f"- {label}:{building_name}: dynamics input '{obs_name}' is globally OFF")
                if obs_name in s["inactive_observations"]:
                    lines.append(f"- {label}:{building_name}: dynamics input '{obs_name}' is blocked locally via inactive_observations")

    return lines


def print_compare(schema_a: SchemaLike, schema_b: SchemaLike, label_a: str = "schema_a", label_b: str = "schema_b", start: int = 0, block_size: int = 100, return_lines: bool = False):
    lines = compare_schemas(schema_a, schema_b, label_a=label_a, label_b=label_b)
    end = min(start + block_size, len(lines))
    print(f"\n=== COMPARE SCHEMAS | lines {start + 1}-{end} of {len(lines)} ===")
    for line in lines[start:end]:
        print(line)
    if end < len(lines):
        print(f"\n...continua com start={end}")
    if return_lines:
        return lines


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compare two CityLearn schema.json files.")
    parser.add_argument("schema_a", help="Path to first schema.json")
    parser.add_argument("schema_b", help="Path to second schema.json")
    parser.add_argument("--label-a", default="schema_a")
    parser.add_argument("--label-b", default="schema_b")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--block-size", type=int, default=100)
    args = parser.parse_args()

    print_compare(
        args.schema_a,
        args.schema_b,
        label_a=args.label_a,
        label_b=args.label_b,
        start=args.start,
        block_size=args.block_size,
    )