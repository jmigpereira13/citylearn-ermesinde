## Dataset: citylearn_challenge_2023_phase_2_online_evaluation_1

### Visão geral

- `central_agent: true` – um único agente central (SACBasicRBC) controla todos os edifícios. 
- Horizonte de simulação: `0` a `2207` → 2208 passos de 1 hora (≈ 92 dias, cerca de 3 meses). 
- Observações globais ativas: `day_type`, `hour`, temperatura exterior real e prevista (3 passos), irradiâncias difusa e direta reais e previstas (3 passos cada), intensidade carbónica, preços de eletricidade reais e previstos (3 passos). 
- Observações locais por edifício: `indoor_dry_bulb_temperature`, `non_shiftable_load`, `solar_generation`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `cooling_demand`, `dhw_demand`, `occupant_count`, `power_outage`, `indoor_dry_bulb_temperature_cooling_set_point`, entre outras; `cooling_storage_soc`, `heating_storage_soc` e consumos elétricos individuais (cooling/heating/DHW) estão inativos. 
- Ações ativas: `dhw_storage`, `electrical_storage`, `cooling_device`; ações de aquecimento e `cooling_storage` estão desativadas. 
- Função de recompensa: `ComfortReward` com banda ±1 °C, expoente inferior 2 e superior 3, igual ao dataset local. 

### Agente

- Tipo: `citylearn.agents.sac.SACBasicRBC`. 
- Hiperparâmetros:
  - `hidden_dimension: [256, 256]`, `discount: 0.9`, `tau: 0.005`, `lr: 0.001`. 
  - `batch_size: 512`, `replay_buffer_capacity: 100000`. 
  - `standardize_start_time_step: 2928`, `end_exploration_time_step: 2929` (herdados da configuração padrão). 
  - `action_scaling_coef: 0.5`, `reward_scaling: 5.0`, `update_per_time_step: 2`, `alpha: 1.0`. 

### Observações e ações (catálogo)

- Observações meteorologia/rede:
  - `day_type`, `hour`, `outdoor_dry_bulb_temperature` + `*_predicted_1/2/3`. 
  - `diffuse_solar_irradiance` e `direct_solar_irradiance` + respetivas previsões. 
  - `carbon_intensity`, `electricity_pricing` + `electricity_pricing_predicted_1/2/3`. 
- Observações edifício:
  - Ativas: `indoor_dry_bulb_temperature`, `non_shiftable_load`, `solar_generation`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `cooling_demand`, `dhw_demand`, `occupant_count`, `power_outage`, `indoor_dry_bulb_temperature_cooling_set_point`. 
  - Inativas: `cooling_storage_soc`, `heating_storage_soc`, `cooling_device_efficiency`, `heating_device_efficiency`, `heating_demand`, consumos elétricos parciais e variáveis de conforto avançadas. 
- Ações:
  - Ativas: `cooling_device`, `dhw_storage`, `electrical_storage`. 
  - Inativas: `cooling_storage`, `heating_storage`, `heating_device`, `cooling_or_heating_device`. 

### Edifícios e assets

Tal como no dataset local, os edifícios `Building_1`, `Building_2`, … partilham a mesma estrutura de assets, variando apenas os parâmetros numéricos. 

Elementos típicos por edifício:

- **Tipo e dinâmica**
  - `type`: `citylearn.building.LSTMDynamicsBuilding`. 
  - `dynamics`:
    - `type`: `citylearn.dynamics.LSTMDynamics`. 
    - Configuração típica: `input_size: 13`, `hidden_size: 16`, `num_layers: 2`, `lookback: 12`, com ficheiro `Building_X.pth`. 
    - `input_observation_names`: `direct_solar_irradiance`, `diffuse_solar_irradiance`, `outdoor_dry_bulb_temperature`, `indoor_dry_bulb_temperature_cooling_set_point`, `occupant_count`, `cooling_demand`, senos/cossenos de mês/hora/dia-tipo, `indoor_dry_bulb_temperature`. 

- **AC (arrefecimento)**
  - `cooling_device`:
    - `type`: `citylearn.energy_model.HeatPump`. 
    - `autosize: false` – `nominal_power` e `efficiency` definidos explicitamente (valores variam por edifício, em torno de alguns kW). 
    - `target_cooling_temperature` ≈ 6–8 °C, `target_heating_temperature: 45` °C. 

- **DHW**
  - `dhw_device`: `citylearn.energy_model.ElectricHeater`, `autosize: false`, com `nominal_power` ≈ 3–5 kW e `efficiency` perto de 0.9. 
  - `dhw_storage`: `StorageTank`, `autosize: false`, `capacity` ≈ 1.6–2.3, `loss_coefficient` na ordem de 0.003–0.004. 

- **Bateria elétrica**
  - `electrical_storage`:
    - `type`: `citylearn.energy_model.Battery`, `autosize: false`. 
    - Atributos comuns: `capacity: 4.0`, `nominal_power: 3.32`, `efficiency: 0.95`, `depth_of_discharge: 0.8`, curva `power_efficiency_curve` com 5 pontos. 

- **PV**
  - `pv`:
    - `type`: `citylearn.energy_model.PV`, `autosize: false`. 
    - `nominal_power` na gama ≈ 1.2–2.4 por edifício. 

- **Power outage**
  - `power_outage`:
    - `"simulate_power_outage": true`, `"stochastic_power_outage": true`. 
    - Modelo: `citylearn.power_outage.ReliabilityMetricsPowerOutage` com `saifi: 1.436`, `caidi: 331.2`, `random_seed: 73055`. 

### Notas rápidas para escolha de dataset

- Estrutura de assets e agente **idêntica** ao `phase_2_local_evaluation`, mas:
  - Janela temporal **mais longa** (≈ 3 meses) – melhor para avaliar generalização da política. 
  - Mesma combinação de AC + DHW + PV + bateria por edifício e falhas de rede estocásticas. 
- Bom para:
  - Treino/avaliação online em horizonte mais extenso mantendo o mesmo “ambiente físico”.
  - Comparar desempenho entre validação local (curta) e online (média duração). 

  ## Dataset: citylearn_challenge_2023_phase_2_online_evaluation_2

- `central_agent: true` (SACBasicRBC) com exatamente os mesmos hiperparâmetros de RL do `online_evaluation_1`. 
- Horizonte de simulação: `0` a `2207` → 2208 passos de 1 h (≈ 3 meses). 
- Conjunto de observações **idêntico** ao `online_evaluation_1` (meteorologia e preços com previsões, `carbon_intensity`, e, por edifício, `indoor_dry_bulb_temperature`, `non_shiftable_load`, `solar_generation`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `cooling_demand`, `dhw_demand`, `occupant_count`, `power_outage`, `indoor_dry_bulb_temperature_cooling_set_point`). 
- Conjunto de ações também igual: `cooling_device`, `dhw_storage`, `electrical_storage` ativos; sem controlo de `cooling_storage` nem de aquecimento. 
- Todos os edifícios são `LSTMDynamicsBuilding` com:
  - `cooling_device = HeatPump` (`autosize: false`, nominal_power e efficiency definidos),
  - `dhw_device = ElectricHeater` + `dhw_storage = StorageTank`,
  - `electrical_storage = Battery` (4 kWh, 3.32 kW, η≈0.95, profundidade de descarga 0.8),
  - `pv = PV` com nominal_power ≈ 1.2–2.4, e `power_outage` estocástico via `ReliabilityMetricsPowerOutage`. 
- Em resumo: mesmo ambiente físico e estrutura de controlo do `online_1`, mas com outro “seed” de dados (ou outra instância dos CSV), pensado para avaliação online alternativa. 

## Dataset: citylearn_challenge_2023_phase_2_online_evaluation_3

- `central_agent: true` (SACBasicRBC) com a mesma configuração de RL. 
- Horizonte de simulação: também `0` a `2207` (≈ 3 meses). 
- Observações: mesma lista que `online_1` e `online_2` (meteorologia + previsões, `carbon_intensity`, preços + previsões, e, por edifício, variáveis de conforto, carga, PV, estados dos storages e `power_outage`). 
- Ações: `cooling_device`, `dhw_storage`, `electrical_storage` ativos; sem ações de aquecimento ou `cooling_storage`. 
- Edifícios:
  - Todos `LSTMDynamicsBuilding` com LSTM (`input_size: 13`, `hidden_size: 16`, `num_layers: 2`, `lookback: 12`), um por building (`Building_X.pth`). 
  - Mesmos tipos de assets: bomba de calor, termoacumulador de AQS com storage, bateria, PV fixo e modelo de falhas de rede `ReliabilityMetricsPowerOutage` com os mesmos parâmetros `saifi`/`caidi`. 
- Em resumo: terceira instância do mesmo cenário físico/estrutural, para avaliação online com outra realização dos dados. 