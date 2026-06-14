# EX COMANDO: python .\explain_schema.py C:\proj_dev\CityLearn\datasets\baeda_3dem\schema.json --start 0 --block-size 300

import json
from pathlib import Path
from typing import Any, Dict, List, Union

SchemaLike = Union[Dict[str, Any], str, Path]

OBSERVATION_HELP = {
    "month": "Mês do ano.",
    "day_type": "Tipo de dia/índice do dia da semana usado pelo dataset.",
    "hour": "Hora do dia.",
    "daylight_savings_status": "Indica se o passo temporal está em horário de verão.",
    "outdoor_dry_bulb_temperature": "Temperatura exterior do ar.",
    "outdoor_dry_bulb_temperature_predicted_1": "Previsão futura da temperatura exterior (horizonte 1).",
    "outdoor_dry_bulb_temperature_predicted_2": "Previsão futura da temperatura exterior (horizonte 2).",
    "outdoor_dry_bulb_temperature_predicted_3": "Previsão futura da temperatura exterior (horizonte 3).",
    "outdoor_relative_humidity": "Humidade relativa exterior.",
    "outdoor_relative_humidity_predicted_1": "Previsão futura da humidade exterior (horizonte 1).",
    "outdoor_relative_humidity_predicted_2": "Previsão futura da humidade exterior (horizonte 2).",
    "outdoor_relative_humidity_predicted_3": "Previsão futura da humidade exterior (horizonte 3).",
    "diffuse_solar_irradiance": "Irradiância solar difusa.",
    "diffuse_solar_irradiance_predicted_1": "Previsão futura da irradiância difusa (horizonte 1).",
    "diffuse_solar_irradiance_predicted_2": "Previsão futura da irradiância difusa (horizonte 2).",
    "diffuse_solar_irradiance_predicted_3": "Previsão futura da irradiância difusa (horizonte 3).",
    "direct_solar_irradiance": "Irradiância solar direta.",
    "direct_solar_irradiance_predicted_1": "Previsão futura da irradiância direta (horizonte 1).",
    "direct_solar_irradiance_predicted_2": "Previsão futura da irradiância direta (horizonte 2).",
    "direct_solar_irradiance_predicted_3": "Previsão futura da irradiância direta (horizonte 3).",
    "carbon_intensity": "Intensidade carbónica da eletricidade da rede.",
    "indoor_dry_bulb_temperature": "Temperatura interior do edifício.",
    "average_unmet_cooling_setpoint_difference": "Desvio médio face ao setpoint de arrefecimento.",
    "indoor_relative_humidity": "Humidade relativa interior.",
    "non_shiftable_load": "Carga elétrica não deslocável/infeliz de controlar.",
    "solar_generation": "Produção local fotovoltaica.",
    "cooling_storage_soc": "Estado de carga do armazenamento de frio.",
    "heating_storage_soc": "Estado de carga do armazenamento de aquecimento.",
    "dhw_storage_soc": "Estado de carga do armazenamento de AQS.",
    "electrical_storage_soc": "Estado de carga da bateria elétrica.",
    "net_electricity_consumption": "Consumo elétrico líquido do edifício.",
    "electricity_pricing": "Preço da eletricidade no instante atual.",
    "electricity_pricing_predicted_1": "Previsão do preço da eletricidade (horizonte 1).",
    "electricity_pricing_predicted_2": "Previsão do preço da eletricidade (horizonte 2).",
    "electricity_pricing_predicted_3": "Previsão do preço da eletricidade (horizonte 3).",
    "cooling_device_efficiency": "Eficiência instantânea do dispositivo de arrefecimento.",
    "heating_device_efficiency": "Eficiência instantânea do dispositivo de aquecimento.",
    "cooling_demand": "Necessidade térmica de arrefecimento.",
    "heating_demand": "Necessidade térmica de aquecimento.",
    "occupant_count": "Número de ocupantes.",
    "power_outage": "Indica falha de energia elétrica.",
    "hvac_mode": "Modo do HVAC.",
    "comfort_band": "Banda de conforto térmico admissível.",
    "indoor_dry_bulb_temperature_cooling_set_point": "Setpoint interior de arrefecimento.",
    "indoor_dry_bulb_temperature_heating_set_point": "Setpoint interior de aquecimento.",
    "indoor_dry_bulb_temperature_cooling_delta": "Diferença entre temperatura interior e setpoint de arrefecimento.",
    "indoor_dry_bulb_temperature_heating_delta": "Diferença entre temperatura interior e setpoint de aquecimento.",
}

ACTION_HELP = {
    "cooling_storage": "Ação sobre o armazenamento de frio.",
    "heating_storage": "Ação sobre o armazenamento de aquecimento.",
    "dhw_storage": "Ação sobre o armazenamento de AQS.",
    "electrical_storage": "Ação sobre a bateria elétrica.",
    "cooling_device": "Ação direta sobre o dispositivo de arrefecimento.",
    "heating_device": "Ação direta sobre o dispositivo de aquecimento.",
    "cooling_or_heating_device": "Ação sobre um dispositivo reversível frio/calor.",
}


def load_schema(schema_or_path: SchemaLike) -> Dict[str, Any]:
    if isinstance(schema_or_path, dict):
        return schema_or_path
    path = Path(schema_or_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _flag(v: Any) -> str:
    return "ON" if bool(v) else "OFF"


def _fmt(v: Any) -> str:
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def schema_to_lines(schema_or_path: SchemaLike) -> List[str]:
    schema = load_schema(schema_or_path)
    lines: List[str] = []

    start = schema.get("simulation_start_time_step")
    end = schema.get("simulation_end_time_step")
    total = None if start is None or end is None else end - start + 1

    lines.append("SCHEMA SUMMARY")
    lines.append(f"- random_seed: {schema.get('random_seed')}")
    lines.append(f"- root_directory: {schema.get('root_directory')}")
    lines.append(f"- central_agent: {schema.get('central_agent')} -> {'agente central único' if schema.get('central_agent') else 'agentes por building'}")
    lines.append(f"- simulation_start_time_step: {start}")
    lines.append(f"- simulation_end_time_step: {end}")
    lines.append(f"- total_time_steps: {total}")
    lines.append(f"- seconds_per_time_step: {schema.get('seconds_per_time_step')}")
    lines.append(f"- rolling_episode_split: {schema.get('rolling_episode_split')}")
    lines.append(f"- random_episode_split: {schema.get('random_episode_split')}")

    lines.append("")
    lines.append("AGENT")
    agent = schema.get("agent", {})
    lines.append(f"- type: {agent.get('type')}")
    for k, v in (agent.get("attributes") or {}).items():
        lines.append(f"  - {k}: {_fmt(v)}")

    lines.append("")
    lines.append("REWARD FUNCTION")
    reward = schema.get("reward_function", {})
    lines.append(f"- type: {reward.get('type')}")
    lines.append(f"- attributes: {_fmt(reward.get('attributes'))}")

    lines.append("")
    lines.append("GLOBAL OBSERVATIONS")
    observations = schema.get("observations", {})
    for name, meta in observations.items():
        lines.append(
            f"- {name}: active={_flag(meta.get('active'))}, shared_in_central_agent={_flag(meta.get('shared_in_central_agent'))} -> {OBSERVATION_HELP.get(name, 'Sem descrição curta definida.')}"
        )

    lines.append("")
    lines.append("GLOBAL ACTIONS")
    actions = schema.get("actions", {})
    for name, meta in actions.items():
        lines.append(f"- {name}: active={_flag(meta.get('active'))} -> {ACTION_HELP.get(name, 'Sem descrição curta definida.')}")

    lines.append("")
    lines.append("BUILDINGS")
    for building_name, building in schema.get("buildings", {}).items():
        lines.append(f"- {building_name}")
        lines.append(f"  - include: {building.get('include')}")
        lines.append(f"  - type: {building.get('type')}")
        lines.append(f"  - energy_simulation: {building.get('energy_simulation')}")
        lines.append(f"  - weather: {building.get('weather')}")
        lines.append(f"  - carbon_intensity: {building.get('carbon_intensity')}")
        lines.append(f"  - pricing: {building.get('pricing')}")

        for asset_name in ["cooling_device", "heating_device", "dhw_device", "cooling_storage", "heating_storage", "dhw_storage", "electrical_storage", "pv"]:
            asset = building.get(asset_name)
            if asset is not None:
                lines.append(f"  - {asset_name}: PRESENT")
                lines.append(f"      - type: {asset.get('type')}")
                if 'autosize' in asset:
                    lines.append(f"      - autosize: {asset.get('autosize')}")
                if 'autosize_attributes' in asset:
                    lines.append(f"      - autosize_attributes: {_fmt(asset.get('autosize_attributes'))}")
                lines.append(f"      - attributes: {_fmt(asset.get('attributes'))}")
            else:
                lines.append(f"  - {asset_name}: ABSENT")

        inactive_obs = building.get("inactive_observations", [])
        inactive_actions = building.get("inactive_actions", [])
        lines.append(f"  - inactive_observations ({len(inactive_obs)}): {_fmt(inactive_obs)}")
        lines.append(f"  - inactive_actions ({len(inactive_actions)}): {_fmt(inactive_actions)}")

        active_local_obs = []
        for obs_name, obs_meta in observations.items():
            if obs_meta.get("active") and obs_name not in inactive_obs:
                active_local_obs.append(obs_name)
        lines.append(f"  - effective_active_observations ({len(active_local_obs)}): {_fmt(active_local_obs)}")

        active_local_actions = []
        for action_name, action_meta in actions.items():
            if action_meta.get("active") and action_name not in inactive_actions:
                active_local_actions.append(action_name)
        lines.append(f"  - effective_active_actions ({len(active_local_actions)}): {_fmt(active_local_actions)}")

        dynamics = building.get("dynamics")
        if dynamics is not None:
            d_attr = dynamics.get("attributes", {})
            lines.append("  - dynamics: PRESENT")
            lines.append(f"      - type: {dynamics.get('type')}")
            for k in ["input_size", "hidden_size", "num_layers", "lookback", "filename"]:
                if k in d_attr:
                    lines.append(f"      - {k}: {_fmt(d_attr.get(k))}")
            input_names = d_attr.get("input_observation_names", [])
            lines.append(f"      - input_observation_names ({len(input_names)}): {_fmt(input_names)}")
            for obs_name in input_names:
                g = observations.get(obs_name)
                global_state = "NOT_DEFINED_GLOBALLY" if g is None else _flag(g.get("active"))
                local_state = "BLOCKED_IN_BUILDING" if obs_name in inactive_obs else "AVAILABLE_OR_INTERNAL"
                lines.append(f"        * {obs_name}: global={global_state}, local={local_state}")
        else:
            lines.append("  - dynamics: ABSENT")

    return lines


def explain_schema(schema_or_path: SchemaLike, start: int = 0, block_size: int = 100, return_lines: bool = False):
    lines = schema_to_lines(schema_or_path)
    end = min(start + block_size, len(lines))
    print(f"\n=== SCHEMA EXPLAINED | lines {start + 1}-{end} of {len(lines)} ===")
    for line in lines[start:end]:
        print(line)
    if end < len(lines):
        print(f"\n...continua com start={end}")
    if return_lines:
        return lines


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Explain a CityLearn schema in readable blocks.")
    parser.add_argument("schema", help="Path to schema.json")
    parser.add_argument("--start", type=int, default=0, help="Start line index for paginated print")
    parser.add_argument("--block-size", type=int, default=100, help="Number of lines to print")
    args = parser.parse_args()

    explain_schema(args.schema, start=args.start, block_size=args.block_size)