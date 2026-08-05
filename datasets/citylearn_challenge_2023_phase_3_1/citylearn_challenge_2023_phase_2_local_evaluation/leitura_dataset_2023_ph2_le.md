## Dataset: citylearn_challenge_2023_phase_2_local_evaluation

### Visão geral

- `central_agent: true` – há um único agente central (SACBasicRBC) a observar o agregado e a decidir para todos os edifícios. 
- Horizonte de simulação: `0` a `719` → 720 passos de tempo de 1 hora (30 dias). 
- Observações globais ativas: dia-tipo, hora, temperatura exterior (real e previstas), irradiâncias difusa e direta (reais e previstas), intensidade carbónica, preços de eletricidade (reais e previstos). 
- Observações locais por edifício: temperatura interior, setpoint de arrefecimento, `cooling_demand`, `dhw_demand`, `non_shiftable_load`, `solar_generation`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `occupant_count`, `power_outage`, entre outras. 
- Ações ativas: controlo de `dhw_storage`, `electrical_storage` e `cooling_device`; não há ações sobre aquecimento nem sobre storages de aquecimento. 
- Função de recompensa: `ComfortReward` com banda de ±1 °C e expoentes 2 e 3, focada em penalizar violações de conforto térmico. 

### Agente

- Tipo: `citylearn.agents.sac.SACBasicRBC` (SAC com componente rule-based básica). 
- Hiperparâmetros principais:
  - `hidden_dimension: [256, 256]`, `discount: 0.9`, `tau: 0.005`, `lr: 1e-3`. 
  - `batch_size: 512`, `replay_buffer_capacity: 100000`. 
  - `action_scaling_coef: 0.5`, `reward_scaling: 5.0`, `update_per_time_step: 2`, `alpha: 1.0`. 

### Observações e ações (catálogo)

- Observações meteorológicas e de rede:
  - `day_type`, `hour`; `outdoor_dry_bulb_temperature` + previsões a 3 passos; `diffuse_solar_irradiance` e `direct_solar_irradiance` + previsões; `carbon_intensity`. 
- Observações por edifício (energia/conforto):
  - `indoor_dry_bulb_temperature`, `non_shiftable_load`, `solar_generation`, `cooling_demand`, `dhw_demand`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `occupant_count`, `power_outage`, `indoor_dry_bulb_temperature_cooling_set_point`. 
- Ações ativas:
  - `cooling_device` (setpoint/potência de AC), `dhw_storage` (carregamento/descarga de AQS), `electrical_storage` (bateria). 
- Ações inativas:
  - `cooling_storage`, `heating_storage`, `heating_device`, `cooling_or_heating_device`. 

### Edifícios e assets

Todos os edifícios `Building_1` a `Building_N` (no schema são pelo menos 2 e seguem o mesmo padrão) têm a mesma arquitetura de assets; diferem apenas nos parâmetros numéricos. 

Características comuns por edifício:

- **Tipo e dinâmica**
  - `type`: `citylearn.building.LSTMDynamicsBuilding`. 
  - `dynamics`:
    - `type`: `citylearn.dynamics.LSTMDynamics`. 
    - Tipicamente `input_size: 13`, `hidden_size: 16`, `num_layers: 2`, `lookback: 12`, com ficheiro de pesos `Building_X.pth`. 
    - `input_observation_names` incluem: `direct_solar_irradiance`, `diffuse_solar_irradiance`, `outdoor_dry_bulb_temperature`, `indoor_dry_bulb_temperature_cooling_set_point`, `occupant_count`, `cooling_demand`, senos/cossenos de mês/hora/dia-tipo, e `indoor_dry_bulb_temperature`. 

- **AC (arrefecimento)**
  - `cooling_device`:
    - `type`: `citylearn.energy_model.HeatPump`. 
    - `autosize: false` – potência nominal explícita (por exemplo, ~4.1 kW em `Building_1`, ~2.25 kW em `Building_2`). 
    - Atributos: `nominal_power`, `efficiency` (COP implícito), `target_cooling_temperature` tipicamente ~6–8 °C, `target_heating_temperature: 45` °C. 

- **DHW (Água Quente Sanitária)**
  - `dhw_device`:
    - `type`: `citylearn.energy_model.ElectricHeater`, `autosize: false`. 
    - `nominal_power` na gama de ~3–5 kW, `efficiency` ~0.9–0.94. 
  - `dhw_storage`:
    - `type`: `citylearn.energy_model.StorageTank`, `autosize: false`. 
    - `capacity` ≈ 1.6–2.3 (unidades de energia), `loss_coefficient` ≈ 0.003–0.004. 

- **Bateria elétrica**
  - `electrical_storage`:
    - `type`: `citylearn.energy_model.Battery`, `autosize: false`. 
    - Atributos típicos:
      - `capacity: 4.0`, `nominal_power: 3.32`, `efficiency: 0.95`. 
      - Curva de eficiência `power_efficiency_curve` com 5 pontos (0–1 p.u.) e `depth_of_discharge: 0.8`. 

- **PV**
  - `pv`:
    - `type`: `citylearn.energy_model.PV`, `autosize: false`. 
    - `nominal_power` tipicamente entre ~1.2 e ~2.4 (kW), consoante o edifício. 

- **Power outage**
  - `power_outage`:
    - `"simulate_power_outage": true`, `"stochastic_power_outage": true`. 
    - Modelo: `citylearn.power_outage.ReliabilityMetricsPowerOutage` com `saifi: 1.436`, `caidi: 331.2` e `random_seed` fixo, igual em todos os edifícios. 

### Notas rápidas para escolha de dataset

- Cenário curto (30 dias) com foco em:
  - **Controlo conjunto** de AC, AQS, PV e bateria sob um agente central. 
  - **Interação com falhas de rede** (power outages estocásticos). 
  - **Penalização de conforto térmico** como objetivo principal. 
- Bom candidato para testar:
  - Estratégias de gestão de bateria + AQS com robustez a falhas de rede.
  - Efeito de previsões de irradiância, temperatura e preço na política de controlo. 