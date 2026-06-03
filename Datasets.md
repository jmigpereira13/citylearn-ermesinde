
## Organização dos Datasets

> Referência oficial: https://www.citylearn.net/overview/dataset.html

Os datasets são um conjunto de **ficheiros de dados** (maioritariamente `.csv` e `.json`) que definem o ambiente de simulação e fornecem valores de observação ao agente.

---

### 1. Building Data File (`building_X.csv`)

Contém dados de séries temporais de um edifício. Existe **um ficheiro por edifício** no ambiente.

Os dados podem provir de:
- Simulação em software de modelação energética (ex.: [EnergyPlus](https://energyplus.net/))
- Sensor/medidor inteligente (*smart meter*)
- *Building Automation System* (BAS) — ex.: [referência BAS](https://em360tech.com/top-10/building-automation-systems-bas)

#### Estrutura das colunas

As colunas do ficheiro de edifício agrupam-se nas seguintes categorias:

| Categoria | Colunas | Descrição |
|---|---|---|
| **Calendário** | `month`, `hour`, `day_type`, `daylight_savings_status` | Variáveis temporais que identificam o instante de simulação. `day_type` distingue dia de semana (1–5) de fim de semana/feriado (6–7). |
| **Cargas de uso final** | `non_shiftable_load`, `dhw_demand`, `cooling_demand`, `heating_demand` | Consumos energéticos do edifício em kWh. `non_shiftable_load` é a carga elétrica não deslocável (iluminação, equipamentos). `dhw_demand` é a procura de água quente sanitária. |
| **Geração solar** | `solar_generation` | Energia fotovoltaica gerada pelo edifício (kWh). Valor ≥ 0. |
| **Ocupação** | `occupant_count` | Número de ocupantes no edifício no instante de tempo. Relevante para modelos de conforto e HVAC. |
| **Ambiente interno** | `indoor_dry_bulb_temperature`, `average_unmet_cooling_setpoint_difference`, `indoor_relative_humidity`, `indoor_dry_bulb_temperature_cooling_set_point`, `indoor_dry_bulb_temperature_heating_set_point`, `hvac_mode` | Variáveis de conforto térmico interior. `hvac_mode` indica o modo de operação do sistema AVAC (0 = desligado, 1 = arrefecimento, 2 = aquecimento). |

#### Exemplo de dados

```csv
month,hour,day_type,daylight_savings_status,indoor_dry_bulb_temperature,average_unmet_cooling_setpoint_difference,indoor_relative_humidity,non_shiftable_load,dhw_demand,cooling_demand,heating_demand,solar_generation,occupant_count,indoor_dry_bulb_temperature_cooling_set_point,indoor_dry_bulb_temperature_heating_set_point,hvac_mode
6,1,1,1,28.121962,0.0,49.774185,0.5676419,0.0,0.0,0.0,0.0,0.0,30.0,30.0,0
6,2,1,1,27.939466,0.0,49.843094,0.5676419,0.0,0.0,0.0,0.0,0.0,30.0,30.0,0
```

---

### 2. Weather Data File (`weather.csv`)

Contém variáveis meteorológicas externas (séries temporais) para a localização geográfica da simulação. É a fonte das observações relacionadas com clima pelo ambiente CityLearn.

Os dados podem ser do tipo:
- **TMY** (*Typical Meteorological Year*) — ano meteorológico típico
- **AMY** (*Actual Meteorological Year*) — dados meteorológicos reais

Fontes habituais: [EnergyPlus Weather Data](https://energyplus.net/weather), [Climate.OneBuilding.Org](http://climate.onebuilding.org/).

| Coluna (exemplos típicos) | Descrição |
|---|---|
| `outdoor_dry_bulb_temperature` | Temperatura de bolbo seco exterior (°C) |
| `outdoor_relative_humidity` | Humidade relativa exterior (%) |
| `diffuse_solar_irradiance` | Irradiância solar difusa (W/m²) |
| `direct_solar_irradiance` | Irradiância solar direta (W/m²) |
| `wind_speed` | Velocidade do vento (m/s) |
| `wind_direction` | Direção do vento (graus) |
| `outdoor_dry_bulb_temperature_predicted_Xh` | Previsão de temperatura a X horas (usado por agentes preditivos) |

> **Nota para Ermesinde:** É possível obter dados TMY para Portugal (zona Porto/Ermesinde) a partir do EnergyPlus Weather ou do PVGIS (https://re.jrc.ec.europa.eu/pvg_tools/).

---

### 3. Carbon Intensity Data File (`carbon_intensity.csv`)

Contém a taxa de emissão de CO₂ associada à eletricidade da rede ao longo do tempo (kg CO₂/kWh). É a fonte da observação `carbon_intensity`.

Fontes habituais: operadores de rede (ex.: [REN — Redes Energéticas Nacionais](https://www.ren.pt/)) ou agregadores de terceiros (ex.: [Electricity Maps](https://www.electricitymaps.com/)).

| Coluna | Descrição |
|---|---|
| `kg_CO2_per_kWh` | Intensidade carbónica da eletricidade da rede (kg CO₂/kWh) |

---

### 4. Pricing Data File (`pricing.csv`)

Contém os preços da eletricidade no instante atual e previsões para instantes futuros. É a fonte das observações de preço (`electricity_pricing` e variantes previstas).

Fontes habituais: comercializadores de energia (ex.: tarifas ERSE/E-REDES para Portugal).

| Coluna (exemplos típicos) | Descrição |
|---|---|
| `electricity_pricing` | Preço atual da eletricidade (€/kWh ou unidade adimensional normalizada) |
| `electricity_pricing_predicted_Xh` | Previsão de preço a X horas à frente |

> **Nota:** Para o caso de Ermesinde (estação de comboios), o perfil de tarifa pode seguir a estrutura de BTE/BTN da ERSE, com distinção de períodos de vazio, cheio e ponta.

---

### 5. LSTM Model Files (opcional)

Os ficheiros de modelo LSTM são **dicionários de estado PyTorch** (`.pt`) opcionais que inicializam os modelos de dinâmica de temperatura interior (`cooling_dynamics` e `heating_dynamics`) dos edifícios.

**Vale a pena incluir?**
- **Sim**, se o objetivo é simular com rigor o comportamento térmico do edifício (temperatura interior como função das ações AVAC), tornando a simulação mais realista.
- **Não é obrigatório** para estudos focados em gestão de energia elétrica (carga, armazenamento, PV), onde as séries temporais do `.csv` já fornecem os valores de temperatura pré-calculados.
- Para o caso de Ermesinde, dado que o foco inicial é dimensionamento PV + armazenamento, **pode ser omitido numa primeira fase**.

| Atributo | Descrição |
|---|---|
| `cooling_dynamics` | Modelo LSTM para dinâmica de arrefecimento (modo cooling) |
| `heating_dynamics` | Modelo LSTM para dinâmica de aquecimento (modo heating) |

---

### 6. Schema Data File (`schema.json`)

> Referência oficial: https://www.citylearn.net/overview/schema.html

O `schema.json` é o **ficheiro central** que referencia todos os outros ficheiros de dados e define completamente o ambiente de simulação CityLearn. É análogo ao ficheiro `.idf` do EnergyPlus — sem ele, o ambiente não pode ser instanciado.

#### Estrutura do schema e relação com os ficheiros de dados

```json
{
  "root_directory": null,
  "simulation_start_time_step": 0,
  "simulation_end_time_step": null,
  "episode_time_steps": 8760,
  "rolling_episode_split": false,
  "random_episode_split": false,
  "seconds_per_time_step": 3600,
  "observations": { ... },
  "actions": { ... },
  "agent": {
    "type": "citylearn.agents.rbc.BasicRBC",
    "attributes": { ... }
  },
  "reward_function": {
    "type": "citylearn.reward_function.RewardFunction",
    "attributes": { ... }
  },
  "buildings": {
    "Building_1": {
      "include": true,
      "energy_simulation": "Building_1.csv",      // → building data file
      "weather": "weather.csv",                   // → weather data file
      "carbon_intensity": "carbon_intensity.csv", // → carbon intensity file
      "pricing": "pricing.csv",                   // → pricing file
      "inactive_observations": [],
      "inactive_actions": [],
      "electrical_storage": {
        "type": "citylearn.energy_model.Battery",
        "autosize": false,
        "attributes": {
          "capacity": 6.4,
          "efficiency": 0.9
        }
      },
      "cooling_system": { ... },
      "heating_system": { ... },
      "dhw_system": { ... },
      "pv": { ... },
      "dynamics": {
        "cooling": {
          "type": "citylearn.dynamics.LSTMDynamics",
          "attributes": { "filename": "cooling_lstm.pt" }  // → LSTM model file (opcional)
        }
      },
      "power_outage": {
        "allow_grid_unavailability": false,
        "stochastic": false
      }
    }
  }
}
```

#### Chaves principais do schema

| Chave | Tipo | Descrição |
|---|---|---|
| `root_directory` | string / null | Caminho absoluto para a pasta com todos os ficheiros de dados. `null` usa o diretório do schema. |
| `simulation_start_time_step` | int | Passo temporal de início da simulação (índice do CSV). |
| `simulation_end_time_step` | int / null | Passo temporal de fim. `null` usa o fim do ficheiro. |
| `episode_time_steps` | int / list | Número de passos por episódio, ou lista de pares [start, end]. |
| `rolling_episode_split` | bool | Se `true`, qualquer passo pode ser início de episódio. |
| `random_episode_split` | bool | Se `true`, episódios são selecionados aleatoriamente (útil em treino RL). |
| `seconds_per_time_step` | int | Resolução temporal (3600 = 1 hora). |
| `observations` | object | Define o espaço de observação global (quais colunas são expostas ao agente). |
| `actions` | object | Define o espaço de ação global. |
| `agent` | object | Controlador a usar (classe Python + hiperparâmetros). |
| `reward_function` | object | Função de recompensa (classe Python + atributos). |
| `buildings` | object | Dicionário de edifícios; cada entrada liga ao respetivo `.csv` e define dispositivos. |

#### Relação schema ↔ ficheiros de dados

```
schema.json
 ├── buildings["Building_1"]["energy_simulation"]  →  Building_1.csv   (calendário, cargas, ocupação, PV, ambiente interno)
 ├── buildings["Building_1"]["weather"]            →  weather.csv       (temperatura, irradiância, humidade exterior)
 ├── buildings["Building_1"]["carbon_intensity"]   →  carbon_intensity.csv  (kg CO₂/kWh)
 ├── buildings["Building_1"]["pricing"]            →  pricing.csv       (€/kWh, previsões)
 └── buildings["Building_1"]["dynamics"]["cooling"]["attributes"]["filename"]  →  cooling_lstm.pt  (opcional)
```

> Cada edifício pode apontar para ficheiros distintos de `weather`, `carbon_intensity` e `pricing`, ou partilhar os mesmos — habitualmente partilham-se os ficheiros de contexto externo e apenas o `energy_simulation` é único por edifício.

---

<!-- ## Próximos Passos

- [ ] Organizar dependências em `requirements.txt`
- [ ] Separar testes exploratórios de scripts finais/aplicados
- [ ] Criar datasets próprios do caso Ermesinde (`Building_Ermesinde.csv`, `weather_porto.csv`, etc.)
- [ ] Adaptar `schema.json` ao caso de Ermesinde (estação de comboios + PV + armazenamento)
- [ ] Documentar pipeline completo de simulação (geração de dados → schema → treino → avaliação)
- [ ] Avaliar necessidade de LSTM dynamics para modelação térmica da estação 

## Caso de Estudo: Estação de Comboios de Ermesinde

### Metodologia de Levantamento e Estimação de Cargas

1. **Levantamento in situ**: identificação e inventário de todos os equipamentos eléctricos
   (displays, escadas rolantes, elevadores, portas automáticas, terminais, HVAC).
2. **Classificação por categoria CityLearn**: separação em `non_shiftable_load` (cargas fixas
   e dinâmicas) e `cooling_demand`/`heating_demand` (HVAC virtual).
3. **Estimação de potências**: fichas técnicas dos fabricantes onde disponíveis (Teleste, Ditec,
   Daikin, Schmitt+Sohn); estimativas fundamentadas em literatura para equipamentos sem ficha.
4. **Perfil horário**: factores de ocupação derivados do horário CP Porto–Ermesinde
   (pico 06h–09h e 16h–19h em dias úteis); distinção de 3 tipos de dia (`day_type` 1/2/3).
5. **AC virtual**: Daikin EWYT040 (39.9 kW frio, COP 3.1) adicionado para cenário europeu
   conforme requisito do projecto; não existe fisicamente na estação.
6. **PV e BESS**: 190 kWp (área medida via Google Earth Pro ~949 m²);
   bateria BYD C130 (131 kWh, 88 kW AC, LFP).

 ### Resultado — Ficheiros para o Tiago

| Ficheiro | Conteúdo |
|---|---|
| `Building_Ermesinde.csv` | 8760 linhas horárias: `non_shiftable_load`, `cooling_demand`, `solar_generation`, `occupant_count` |
| `weather_porto.csv` | Dados TMY Porto (PVGIS/EnergyPlus Weather) |
| `schema.json` | Parâmetros `HeatPump`, `Battery` (BYD C130), `PV` (190 kWp) | -->
