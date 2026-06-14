# CityLearn 2023 Phase 3_1

## Visão geral
Este dataset usa `central_agent: true`, por isso a política controla o conjunto dos edifícios como um único agente central.  A simulação decorre de `time_step` 0 até 2207, com passos de 3600 s, o que corresponde a 2208 horas de simulação. 

## Estrutura do cenário
O schema inclui 6 edifícios (`Building1` a `Building6`), todos do tipo `citylearn.building.LSTMDynamicsBuilding`.  Cada edifício liga um ficheiro `BuildingX.csv`, além de `weather.csv`, `carbonintensity.csv` e `pricing.csv`, o que confirma a separação entre configuração estrutural no schema e séries temporais nos CSV. 

## O que existe no dataset
Em todos os edifícios há `coolingdevice` com `citylearn.energymodel.HeatPump`, `dhwdevice` com `citylearn.energymodel.ElectricHeater`, `dhwstorage` com `StorageTank`, `electricalstorage` com `Battery` e `pv` com `PV`.  Não aparecem `heatingdevice`, `heatingstorage` nem `coolingstorage` ativos, por isso este dataset está orientado para arrefecimento, AQS, bateria elétrica e produção fotovoltaica. 

## Observações e ações
As observações ativas incluem variáveis meteorológicas atuais e previstas, `carbon_intensity`, `non_shiftable_load`, `solar_generation`, `dhw_storage_soc`, `electrical_storage_soc`, `net_electricity_consumption`, `electricity_pricing`, `cooling_demand`, `dhw_demand`, `occupant_count`, `power_outage` e temperatura interior.  As ações ativas são `dhw_storage`, `electrical_storage` e `cooling_device`, o que significa que o controlo atua sobre AQS, bateria e climatização de arrefecimento. 

## Dinâmica e controlo
O agente definido é `citylearn.agents.sac.SACBasicRBC` e a reward function é `citylearn.rewardfunction.ComfortReward`, com banda de conforto de 1.0.  Todos os edifícios usam `citylearn.dynamics.LSTMDynamics` com `lookback: 12`, `input_size: 13`, `hidden_size: 16` e ficheiros `.pth`, portanto a evolução térmica não vem diretamente de EnergyPlus durante a simulação, mas de modelos LSTM treinados previamente. 

## Escala técnica
As potências nominais de arrefecimento (`coolingdevice.nominal_power`) estão aproximadamente entre 2.25 kW e 5.81 kW nos seis edifícios.  As baterias elétricas têm capacidades entre 3.3 kWh e 4.0 kWh, com potência nominal entre 1.61 kW e 3.32 kW, enquanto os sistemas PV variam entre 1.2 kW e 2.8 kW. 

## Power outages
O schema ativa `power_outage` como observação e, em cada edifício, `simulate_power_outage: true` com modelo `ReliabilityMetricsPowerOutage`.  Em `phase_3_1`, o `random_seed` do modelo de outage é 65647, com `saifi: 1.436` e `caidi: 331.2`. 

## Leitura prática para comparação com Ermesinde
Este dataset é útil para estudar coordenação centralizada entre vários edifícios com AC, AQS, PV e bateria, incluindo falhas de rede.  Em escala, está muito abaixo de Ermesinde nas potências de AC, PV e bateria, por isso serve melhor como referência estrutural e de arquitetura de controlo do que como referência direta de dimensionamento. 