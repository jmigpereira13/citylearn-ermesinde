# Comparação de datasets CityLearn face a Ermesinde

## Critério de comparação
A comparação abaixo foi feita olhando para os elementos mais relevantes para o teu caso: tipo de agente, número de edifícios, presença de AC/arrefecimento, PV, AQS, bateria, falhas de rede e ordem de grandeza dos ativos.  Para Ermesinde, a referência funcional no teu Excel inclui `nonshiftableload`, `coolingdemand`, PV recomendado de 70 a 190 kWp, e BESS recomendada de 131 kWh úteis com 88 kW AC; o AC virtual recomendado aparece como 39.9 kW de frio. 

## Matriz comparativa
| Dataset | Agente | Horizonte | Buildings | AC / cooling | DHW | PV | Bateria | Outages | Proximidade a Ermesinde |
|---|---|---:|---:|---|---|---|---|---|---|
| `baeda_3dem` | Descentralizado (`central_agent: false`)  | 2928 h  | 4  | Sim, `HeatPump`  | Sim  | Muito limitada, no resumo anterior só `Building4` tinha PV ativo  | Não aparece bateria elétrica ativa no schema anterior  | Não destacado no schema analisado  | Útil para perceber estrutura base; fraco para reproduzir Ermesinde  |
| `phase_local_2` | Centralizado  | 720 h  | Pelo menos 3 no resumo recuperado; segue a família dos benchmarks 2023  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim  | Bom para testes curtos e validação, mas muito pequeno para Ermesinde  |
| `phase2_online_1` | Centralizado  | 2208 h  | Benchmark da família 2023  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim  | Útil como benchmark estável; escala muito abaixo de Ermesinde  |
| `online_ev2` | Centralizado  | 2208 h  | Benchmark da mesma família  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim  | Bom para estudar a variante EV/online, mas continua longe da escala real de Ermesinde  |
| `online_ev3` | Centralizado  | 2208 h  | Benchmark da mesma família  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim  | Semelhante ao anterior; útil para variantes de estudo, não para escala  |
| `phase_3_1` | Centralizado  | 2208 h  | 6  | Sim, `HeatPump`  | Sim, `ElectricHeater`  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim, seed 65647  | Muito bom para estudar coordenação central + outages; fraco para dimensionamento direto  |
| `phase_3_2` | Centralizado  | 2208 h  | 6  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim, seed 42647  | Praticamente igual a `phase_3_1`, muda a realização estocástica dos outages  |
| `phase_3_3` | Centralizado  | 2208 h  | 6  | Sim  | Sim  | Sim, 1.2 a 2.8 kW  | Sim, 3.3 a 4.0 kWh  | Sim, seed 57841  | Igual em arquitetura às outras duas phases 3; serve como terceira realização de outages  |
| **Ermesinde** | A definir por ti no schema final  | Idealmente 8760 h no caso base anual  | Pode ser 1 building equivalente ou decomposição por zonas/serviços  | AC virtual recomendado 39.9 kW, alternativa 88.8 kW  | Não é o foco principal do Excel atual  | 70 a 190 kWp recomendados  | 131 kWh úteis, 88 kW AC recomendados  | Pode ser incluído depois, mas não é o foco atual do dimensionamento  | Caso-alvo  |

## Diferenças de escala
A diferença mais forte entre os benchmarks CityLearn 2023 e Ermesinde está na ordem de grandeza dos ativos: nos datasets 2023, o PV típico vai apenas de 1.2 a 2.8 kW por edifício e a bateria de 3.3 a 4.0 kWh, enquanto em Ermesinde estás a trabalhar com 70 a 190 kWp de PV e 131 kWh de BESS.  Também o AC de Ermesinde é muito maior, com referência recomendada de 39.9 kW, ao passo que os `coolingdevice.nominal_power` dos benchmarks andam aproximadamente entre 2.25 kW e 5.81 kW. 

## O que estudar em cada família
`baeda_3dem` é útil para perceber a lógica base do schema e a leitura do `schema.json` quando tens menos edifícios e um caso mais simples, incluindo a distinção entre observações globais e locais.  Já a família `phase_local_2`, `phase2_online_1`, `online_ev2`, `online_ev3` e `phase_3_x` é mais útil para estudar um cenário CityLearn mais completo, com agente central, bateria, PV, AQS, arrefecimento, `power_outage`, reward e dinâmica LSTM. 

## O que reutilizar para Ermesinde
Para Ermesinde, o que mais te compensa reutilizar não são as potências nominais, mas sim a **arquitetura de dataset**: estrutura de `schema.json`, convenção de observações, ações, ligação `Building.csv` + `weather.csv` + `pricing.csv` + `carbonintensity.csv`, e parametrização de `electricalstorage`, `pv` e `coolingdevice`.  Em particular, `phase_3_1` é uma boa referência principal porque junta central agent, PV, BESS, AQS, cooling e outages; `phase_3_2` e `phase_3_3` devem ser vistos apenas como repetições do mesmo caso com seeds diferentes de interrupção da rede. 

## Recomendação final
Se o objetivo é aprender CityLearn de forma eficiente para depois montar Ermesinde, a sequência mais útil é: primeiro `baeda_3dem` para aprender o schema, depois `phase_3_1` para aprender um benchmark completo, e só depois olhar para `phase_3_2` e `phase_3_3` como variantes de robustez.  Para construir o caso de Ermesinde, usa os teus próprios valores de carga, AC, PV e BESS do Excel, mas copia a organização estrutural e semântica dos schemas da família `phase_3_x`, porque é aí que tens o melhor compromisso entre completude funcional e clareza de modelação. 