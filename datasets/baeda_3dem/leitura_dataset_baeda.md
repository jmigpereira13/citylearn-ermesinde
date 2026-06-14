## Leitura de schema.json do dataset baeda_3dem [observações -> linhas 11 a 200]

No bloco inicial do `schema.json` do `baeda_3dem`, o que aparece antes de `actions` corresponde à configuração global e à lista de `observations`. Isto significa que esta parte ainda não descreve os equipamentos por edifício, mas sim **que informação o ambiente pode observar** ao longo do tempo. 

As observações ativas misturam:
- variáveis de calendário, 
- variáveis meteorológicas, 
- previsões de curto horizonte, 
- estados internos do edifício 
- sinais energéticos. 

Entre as observações ativas neste bloco estão:
- `month`, `day_type`, `hour`, temperatura exterior atual e prevista, irradiância solar direta atual e prevista;
- `carbon_intensity`, `non_shiftable_load`, `solar_generation`;
- estados de carga de alguns armazenamentos, preço da eletricidade atual e previsto;
- eficiência do dispositivo de arrefecimento, número de ocupantes e variáveis ligadas ao setpoint de arrefecimento. 

## Como interpretar `shared_in_central_agent`

O campo `shared_in_central_agent` indica se uma observação pode ser partilhada com um agente central quando a simulação usa controlo centralizado. Como neste dataset `central_agent` está a `false`, este campo não altera o facto de o controlo estar distribuído por building, mas continua a ser útil para perceber que observações são globais e quais são locais ao edifício.  

Em termos práticos, observações meteorológicas, temporais e de preço aparecem frequentemente como partilháveis, enquanto grandezas como temperatura interior, carga não deslocável, estado de carga dos armazenamentos e variáveis de conforto tendem a ser locais ao building. Essa distinção ajuda bastante quando se quer separar sinais exógenos do ambiente de estados internos do edifício. 

## Leitura prática das observações deste bloco

As observações deste bloco podem ser agrupadas assim:

- **Tempo e calendário:** `month`, `day_type`, `hour`, `daylight_savings_status`. 
- **Meteorologia atual e prevista:** temperatura exterior, humidade exterior, irradiância difusa e irradiância direta, incluindo vários horizontes previstos. 
- **Sinais energéticos externos:** `carbon_intensity` e `electricity_pricing` com previsões. 
- **Estados internos do edifício:** temperatura interior, humidade interior, carga não deslocável, ocupação e variáveis de conforto. 
- **Estados de sistemas energéticos:** `solar_generation`, `cooling_storage_soc`, `dhw_storage_soc`, `electrical_storage_soc`, eficiências dos equipamentos e deltas face ao setpoint.  

Esta organização é útil porque permite perceber logo se um dataset está mais orientado para controlo térmico, controlo de storage, arbitragem com preço, autoconsumo fotovoltaico ou uma mistura destes objetivos. 
No `baeda_3dem`, este bloco já sugere um cenário com foco relevante em arrefecimento, AQS, preço e pelo menos alguma integração potencial com PV e armazenamento, embora a confirmação final dos assets venha mais à frente na secção `buildings`. 

## Actions, agente e Building_1

### Secção `actions` [linhas 201 a 223]

A secção `actions` define o conjunto de comandos que o agente **pode tentar aplicar** no ambiente. Nesta fase ainda se trata de um catálogo global; depois, em cada building, a lista de `inactive_actions` pode desligar algumas dessas ações localmente.

No bloco enviado, as ações globalmente ativas são:
- `cooling_storage`;
- `dhw_storage`;
- `cooling_device`;
enquanto `heating_storage`, `electrical_storage`, `heating_device` e `cooling_or_heating_device` estão globalmente inativas. 

**Isto sugere que o dataset foi montado sobretudo para controlo de arrefecimento e, em princípio, de AQS, mas não para controlo de bateria elétrica nem para um modo de aquecimento ativo.**

Em leitura prática:

| Ação | Significado operacional |
|---|---|
| `cooling_storage` | Controla carga/descarga do armazenamento térmico de frio. |
| `dhw_storage` | Controla carga/descarga do armazenamento de AQS. |
| `cooling_device` | Atua diretamente no equipamento de arrefecimento, neste caso o sistema equivalente ao AC. |
| `heating_storage` | Seria controlo de armazenamento térmico de aquecimento, mas está desligado. |
| `electrical_storage` | Seria controlo de bateria/BESS, mas está desligado. |
| `heating_device` | Seria controlo direto do sistema de aquecimento, mas está desligado. |
| `cooling_or_heating_device` | Seria uma ação para equipamento reversível calor/frio, mas não está a ser usada aqui. |

### Secção `agent`[linhas 224 a 243]

O agente configurado é do tipo `citylearn.agents.sac.SAC`, ou seja, um agente baseado em *Soft Actor-Critic*. Isto significa que o dataset está preparado para uma abordagem de controlo por reforço contínuo e não apenas para regras fixas ou otimização determinística.

Os atributos do agente mostram uma rede escondida com:
- duas camadas de 256 neurónios;
- `discount` de 0.9;
- `lr` de 0.001;
- `batch_size` de 512 
- `replay_buffer_capacity` de 100000.0. 

**Em termos práticos, esta secção não descreve o edifício nem os equipamentos; descreve **como o controlador aprende** a partir das observações, ações e recompensas do ambiente.**

### Secção `reward_function` [linhas 243 a 247]

A reward function é `citylearn.reward_function.ComfortReward`. Isto indica que o objetivo principal do treino está centrado no conforto térmico, e não diretamente em custo, emissões ou redução de pico, embora esses objetivos pudessem ser usados noutros schemas.
Como `attributes` está a `null`, não aparecem aqui parâmetros adicionais a ajustar para esta reward. 

**Na prática, este bloco deve ser lido como a definição do critério de desempenho que o agente tenta otimizar ao longo da simulação.**

### Secção `buildings` e entrada `Building_1` [linhas 248 a 356]

A entrada `Building_1` é o primeiro caso concreto onde o schema junta ficheiros, equipamentos, ações locais e dinâmica térmica. É aqui que o dataset deixa de ser apenas um catálogo global e passa a descrever **um edifício operacional dentro do ambiente**.

O `Building_1` está incluído na simulação com `include: true`, usa `Building_1.csv` como ficheiro principal de energia, `weather.csv` como fonte meteorológica e `pricing.csv` como sinal de preço. O campo `carbon_intensity` está a `null`, pelo que este edifício não está ligado a um ficheiro próprio de intensidade carbónica neste schema.

### Equipamentos do `Building_1`

O `Building_1` tem um `cooling_device` do tipo `citylearn.energy_model.HeatPump`, com `autosize: true`, `efficiency: 0.2`, `target_cooling_temperature: 8` e `target_heating_temperature: 45`. Em leitura prática, isto corresponde ao sistema de arrefecimento principal do edifício, modelado como bomba de calor, com potência nominal a ser dimensionada automaticamente pelo ambiente em vez de ser fixada manualmente no schema.

Também existe um `dhw_device` do tipo `citylearn.energy_model.ElectricHeater`, igualmente com `autosize: true` e `efficiency: 0.9`. Isto confirma que o edifício tem AQS elétrica, mesmo que esse subsistema não fique totalmente exposto ao agente em todas as observações ou ações locais.

Além dIsto, o edifício tem `cooling_storage` do tipo `citylearn.energy_model.StorageTank`, com `autosize: true`, `safety_factor: 3.0`, `capacity: null` e `loss_coefficient: 0.006`. Em termos práticos, há armazenamento térmico associado ao arrefecimento, com capacidade a ser calculada automaticamente e com perdas térmicas modeladas pelo coeficiente indicado.

Até este ponto, o `Building_1` **não mostra** `pv`, `electrical_storage`, `heating_device` nem `heating_storage`. Portanto, para este building específico, o cenário é de arrefecimento com storage térmico e AQS elétrica, mas sem PV e sem bateria elétrica visíveis nesta configuração.

### Observações e ações realmente disponíveis no `Building_1`

A lista `inactive_observations` é muito importante porque corta localmente parte das observações que estavam globalmente ativas. No `Building_1`, ficam desativadas observações como `dhw_storage_soc`, `solar_generation`, várias previsões e medições ligadas a irradiância difusa e direta, `heating_storage_soc`, `electrical_storage_soc` e `carbon_intensity`.

Isto significa, por exemplo, que mesmo que `solar_generation` exista no catálogo global de observações, ela não é entregue ao agente neste edifício. Da mesma forma, a presença de `dhw_device` não implica que o agente observe o `dhw_storage_soc`, porque essa observação foi explicitamente desligada para o `Building_1`.

A lista `inactive_actions` faz o mesmo para as ações. No `Building_1`, as ações `dhw_storage`, `heating_storage` e `electrical_storage` ficam localmente desligadas, pelo que, na prática, este edifício fica com foco de controlo no `cooling_device` e no `cooling_storage`, mesmo que globalmente `dhw_storage` estivesse ativa.

### Secção `dynamics`

O `Building_1` usa uma dinâmica do tipo `citylearn.dynamics.LSTMDynamics`, com `input_size: 11`, `hidden_size: 8`, `num_layers: 2`, `lookback: 12` e o ficheiro `Building_1.pth`. Isto significa que o comportamento térmico do edifício não é apenas lido diretamente dos CSV, mas passa por um modelo LSTM treinado que tenta representar a evolução dinâmica do edifício ao longo do tempo.

Os vetores `input_normalization_minimum` e `input_normalization_maximum` servem para normalizar as entradas antes de estas serem usadas pela rede. Já `input_observation_names` mostra exatamente que sinais alimentam a dinâmica: irradiância solar direta, temperatura exterior, ocupação, `cooling_demand`, codificação cíclica da hora, do tipo de dia e do mês, e ainda a temperatura interior.

Há aqui uma nota importante: `cooling_demand` aparece como input da dinâmica apesar de, no catálogo global de observações, estar marcada como inativa. Isto não quer dizer necessariamente erro; quer dizer que uma variável pode não estar exposta ao agente como observação e, ainda assim, ser usada internamente pelo modelo dinâmico do building.[3]

### Leitura prática do `Building_1`

Em resumo operacional, o `Building_1` deste dataset representa um edifício com bomba de calor para arrefecimento, aquecimento de AQS por resistência elétrica e armazenamento térmico de frio. O agente não controla PV, bateria elétrica nem aquecimento, e a reward está orientada para conforto térmico.

Isto faz do `Building_1` um bom exemplo de dataset orientado para estudar controlo de arrefecimento e conforto com alguma flexibilidade térmica, mas não um caso completo de comunidade energética com todos os DERs típicos ativos ao mesmo tempo. Para essa leitura comunitária, será importante verificar os restantes buildings e ver em que medida aparece PV, storage elétrico e sinais energéticos úteis para autoconsumo ou coordenação entre edifícios.

## baeda_3dem – Edifícios 2 a 4 (schema.json)

Esta secção descreve os edifícios 2 a 4 do dataset `baeda_3dem` tal como definidos no `schema.json`, traduzindo as chaves técnicas de CityLearn para linguagem mais próxima de AC, AQS, PV, storages e modelo dinâmico.  

### Building_2

- **Ficheiros ligados**
  - `energy_simulation`: `Building_2.csv` – série temporal de cargas e estados térmicos deste edifício.
  - `weather`: `weather.csv` – condições exteriores comuns ao dataset.
  - `pricing`: `pricing.csv` – tarifa horária de eletricidade.
  - `carbon_intensity`: `null` – não há sinal explícito de intensidade carbónica neste dataset.

- **Tipo de edifício / dinâmica**
  - `type`: `citylearn.building.LSTMDynamicsBuilding` – edifício cuja evolução interna (temperaturas, cargas, etc.) é aproximada por um modelo LSTM em vez de um modelo físico detalhado.
  - `dynamics.type`: `citylearn.dynamics.LSTMDynamics` – dinâmica atrás de cada passo de tempo é dada por uma rede LSTM com:
    - `input_size: 11`, `hidden_size: 8`, `num_layers: 2`, `lookback: 12`.
    - `filename`: `Building_2.pth` – ficheiro de pesos PyTorch do modelo.
    - `input_observation_names`:  
      `direct_solar_irradiance`, `outdoor_dry_bulb_temperature`, `occupant_count`, `cooling_demand`, `hour_sin`, `hour_cos`, `day_type_sin`, `day_type_cos`, `month_sin`, `month_cos`, `indoor_dry_bulb_temperature`.  
      Isto quer dizer que o LSTM “vê” essencialmente radiação solar direta, temperatura exterior, ocupação, pedido de arrefecimento e encoding periódico de hora/dia/mês, mais a temperatura interior, para prever as próximas variáveis de estado.

- **Arrefecimento (AC)**
  - `cooling_device.type`: `citylearn.energy_model.HeatPump`.  
    É o “AC” do edifício, modelado como bomba de calor.
  - `cooling_device.autosize: true` com `safety_factor: 1.0`.  
    A potência nominal é dimensionada automaticamente a partir dos dados de carga, sem margem extra (1.0).
  - `cooling_device.attributes`:
    - `nominal_power: null` – deixa ao CityLearn o cálculo da potência nominal.
    - `efficiency: 0.21` – eficiência elétrica do equipamento (entrada→saída térmica) para o lado de arrefecimento.
    - `target_cooling_temperature: 9` – temperatura alvo do lado frio (por exemplo, água gelada a 9 °C).
    - `target_heating_temperature: 45` – temperatura de ida no lado quente (se usado em modo aquecimento).

- **Água Quente Sanitária (DHW)**
  - `dhw_device.type`: `citylearn.energy_model.ElectricHeater`.
  - `dhw_device.autosize: true`, com:
    - `nominal_power: null` – também dimensionada automaticamente.
    - `efficiency: 0.92` – resistência elétrica relativamente eficiente.

- **Storages**
  - `cooling_storage`:
    - `type`: `citylearn.energy_model.StorageTank`.
    - `autosize: true`, `safety_factor: 3.0` – depósito de frio dimensionado automaticamente com margem de 3x face ao dimensionamento base (mais flexibilidade de armazenamento).
    - `attributes.capacity: null` – capacidade calculada pelo autosizing.
    - `loss_coefficient: 0.006` – perdas térmicas do depósito por passo de tempo.
  - `dhw_storage`:
    - `type`: `citylearn.energy_model.StorageTank`.
    - `autosize: true`, `safety_factor: 3.0`.
    - `capacity: null`, `loss_coefficient: 0.008` – perdas ligeiramente superiores às do depósito de frio.
  - **Sem bateria elétrica**: não existe `electrical_storage` definido no `Building_2`.

- **Observações inativas**
  - Lista de `inactive_observations` inclui:
    - `solar_generation`, `diffuse_solar_irradiance` e todas as variantes `*_predicted_*`.
    - `direct_solar_irradiance_predicted_1/2/3`.
    - `heating_storage_soc`, `electrical_storage_soc`.
    - `carbon_intensity`.  
  - Isto significa:
    - Não há PV associado a este edifício (logo `solar_generation` não aparece na observação local).
    - Não existe armazenamento de aquecimento nem armazenamento elétrico activo no edifício 2.
    - A intensidade carbónica, embora exista globalmente no ambiente, não é usada nem observada localmente aqui.

- **Ações inativas**
  - `inactive_actions`: `["heating_storage", "electrical_storage"]`.  
  - O agente deste edifício só pode atuar sobre os depósitos de frio e de AQS e sobre o dispositivo de arrefecimento, não tem ações sobre aquecimento nem sobre bateria elétrica.

---

### Building_3

O edifício 3 é quase um “clone estrutural” do 2, com pequenas diferenças nos parâmetros dos equipamentos e na dinâmica.

- **Ficheiros ligados**
  - `energy_simulation`: `Building_3.csv`
  - `weather`: `weather.csv`
  - `pricing`: `pricing.csv`
  - `carbon_intensity`: `null`

- **Tipo de edifício / dinâmica**
  - `type`: `citylearn.building.LSTMDynamicsBuilding`.
  - `dynamics`:
    - `input_size: 11`, `hidden_size: 8`, `num_layers: 2`, `lookback: 12` (igual ao B2).
    - `filename`: `Building_3.pth`.
    - `input_observation_names`: idêntico ao B2 (mesmo conjunto de inputs para o LSTM).
    - Difere apenas nos intervalos de normalização (`input_normalization_minimum`/`maximum`), adaptados às gamas reais das variáveis neste edifício.

- **Arrefecimento (AC)**
  - `cooling_device` também é uma `HeatPump`, `autosize: true`, `safety_factor: 1.0`.
  - `efficiency: 0.23` – ligeiramente mais eficiente que no B2.
  - `target_cooling_temperature: 8` °C – temperatura alvo ainda mais baixa no lado frio.
  - `target_heating_temperature: 45` °C – igual ao B2.

- **DHW**
  - `dhw_device`: `ElectricHeater`, `autosize: true`.
  - `efficiency: 0.87` – ligeiramente abaixo da eficiência do B2.

- **Storages**
  - `cooling_storage`: `StorageTank`, `autosize: true`, `safety_factor: 3.0`, `loss_coefficient: 0.006`.
  - `dhw_storage`: `StorageTank`, `autosize: true`, `safety_factor: 3.0`, `loss_coefficient: 0.008`.
  - Tal como no B2, não há `electrical_storage`.

- **Observações inativas**
  - A lista é praticamente igual à do B2:
    - `solar_generation`, `diffuse_solar_irradiance` e variantes preditivas.
    - `direct_solar_irradiance_predicted_1/2/3`.
    - `heating_storage_soc`, `electrical_storage_soc`, `carbon_intensity`.  
  - Interpretação: este edifício também não tem PV nem bateria elétrica, e não usa observações ligadas a aquecimento.

- **Ações inativas**
  - `["heating_storage", "electrical_storage"]` – igual ao B2.

---

### Building_4

O edifício 4 segue o mesmo padrão de LSTM + bomba de calor + DHW + storages, mas é o único com PV explícito no schema.

- **Ficheiros ligados**
  - `energy_simulation`: `Building_4.csv`
  - `weather`: `weather.csv`
  - `pricing`: `pricing.csv`
  - `carbon_intensity`: `null`

- **Tipo de edifício / dinâmica**
  - `type`: `citylearn.building.LSTMDynamicsBuilding`.
  - `dynamics`:
    - `input_size: 11`, `hidden_size: 50`, `num_layers: 1`, `lookback: 12`.
    - `filename`: `Building_4.pth`.
    - `input_observation_names`: idêntico aos anteriores (mesmo conjunto de 11 inputs).
    - A diferença principal está na dimensão do estado oculto (50 em vez de 8) e no número de camadas (1 em vez de 2), sugerindo um modelo LSTM mais “largo” mas menos profundo para este edifício.

- **Arrefecimento (AC)**
  - `cooling_device`: `HeatPump`, `autosize: true`, `safety_factor: 1.0`.
  - `efficiency: 0.22` – entre os valores de B2 e B3.
  - `target_cooling_temperature: 9` °C, `target_heating_temperature: 45` °C.

- **DHW**
  - `dhw_device`: `ElectricHeater`, `autosize: true`.
  - `efficiency: 0.9` – aqui a resistência é ligeiramente mais eficiente do que no B2 e B3.

- **Storages**
  - `cooling_storage`: `StorageTank`, `autosize: true`, `safety_factor: 3.0`, `loss_coefficient: 0.006`.
  - `dhw_storage`: `StorageTank`, `autosize: true`, `safety_factor: 3.0`, `loss_coefficient: 0.008`.
  - Tal como nos outros edifícios, não há `electrical_storage` definido.

- **PV (fotovoltaico)**
  - `pv.type`: `citylearn.energy_model.PV`.
  - `autosize: false` – aqui a potência é explicitamente definida, não dimensionada pelo CityLearn.
  - `attributes.nominal_power: 120` – sistema PV fixo de 120 (kW, assumindo a convenção usual do pacote), ligado a este edifício.
  - Como não há `solar_generation` na lista de `inactive_observations` do B4, a geração fotovoltaica deste edifício aparece na observação local e é usada pelo modelo/controlo.

- **Observações inativas**
  - `inactive_observations`: `["heating_storage_soc", "electrical_storage_soc", "carbon_intensity"]`.
  - Face a B2/B3, nota‑se que não se desativa `solar_generation` nem as irradiâncias, compatível com a presença de PV.

- **Ações inativas**
  - `["heating_storage", "electrical_storage"]`.
  - O agente pode atuar sobre storages de frio e AQS e sobre o equipamento de arrefecimento, mas não tem ações de aquecimento nem de bateria.

---

### Resumo rápido por edifício

| Edifício | AC (HeatPump) | DHW (ElectricHeater) | Cooling storage | DHW storage | PV | Bateria elétrica | Modelo LSTM |
|---------|----------------|----------------------|-----------------|-------------|----|------------------|-------------|
| B2 | Sim, autosize, η=0.21 | Sim, autosize, η=0.92 | Sim, autosize, SF=3.0 | Sim, autosize, SF=3.0 | Não | Não | LSTM, 2 camadas, hidden=8 |
| B3 | Sim, autosize, η=0.23 | Sim, autosize, η=0.87 | Sim, autosize, SF=3.0 | Sim, autosize, SF=3.0 | Não | Não | LSTM, 2 camadas, hidden=8 |
| B4 | Sim, autosize, η=0.22 | Sim, autosize, η=0.90 | Sim, autosize, SF=3.0 | Sim, autosize, SF=3.0 | Sim, 120 kW | Não | LSTM, 1 camada, hidden=50 |