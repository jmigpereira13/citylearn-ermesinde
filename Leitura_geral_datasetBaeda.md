# Dataset `baeda_3dem` – Tabela preenchida das variáveis

## Enquadramento

O dataset `baeda_3dem` usa quatro ficheiros de edifício (`Building_1.csv` a `Building_4.csv`), um ficheiro meteorológico comum (`weather.csv`) e um ficheiro de preços (`pricing.csv`).  As colunas dos quatro `Building_X.csv` são iguais, mas os valores mostram perfis de carga, ocupação e procura térmica bastante diferentes entre edifícios, o que é útil para perceber a diversidade do bairro simulado. 

As tabelas abaixo já incluem exemplos de valores reais retirados dos CSV enviados, para que o ficheiro sirva não só como glossário mas também como referência prática do comportamento do dataset. 

## Variáveis dos edifícios

| Campo | Categoria | Interpretação prática | Exemplos reais observados | Leitura para o cenário |
|---|---|---|---|---|
| `month` | Tempo | Mês da série temporal. | Nos excertos mostrados, o valor é `6`, indicando junho.  | Útil para sazonalidade e alinhamento com clima e preços.  |
| `hour` | Tempo | Hora do dia no time step atual. | Nos excertos vê-se a progressão `1` a `24`.  | Essencial para padrões diários de carga, ocupação e solar.  |
| `day_type` | Calendário | Tipo de dia, normalmente usado para distinguir dias úteis/fim de semana/feriado conforme o dataset. | Nos excertos aparecem valores `1` e `2`.  | Bom indicador para perfis distintos de ocupação e consumo.  |
| `daylight_savings_status` | Calendário | Indica estado de horário de verão. | Nos excertos enviados o valor é `1`.  | Ajuda a alinhar perfis horários com clima e irradiância.  |
| `indoor_dry_bulb_temperature` | Estado interior | Temperatura interior do edifício. | Building 1 varia de cerca de `27.53` a `29.57` °C no primeiro dia mostrado; Building 3 começa perto de `24.` °C e aproxima-se de `26.0` °C; Building 4 sobe até cerca de `29.5` °C.  | Dá uma noção direta de conforto térmico e resposta do edifício ao controlo.  |
| `average_unmet_cooling_setpoint_difference` | Conforto | Diferença média entre a temperatura interior e o setpoint de arrefecimento quando há desconforto. | Nos excertos visíveis está sempre em `0.0`.  | Indica que, nessas horas, o setpoint de cooling não estava a ser violado.  |
| `indoor_relative_humidity` | Estado interior | Humidade relativa interior. | Building 1 ronda `4.65`–`50.04`%; Building 2 começa perto de `43.2`–`49.99`%; Building 4 ronda `57.43`–`61.70`%.  | Pode ajudar a caracterizar conforto, embora nem sempre esteja ativa no schema como observação.  |
| `non_shiftable_load` | Carga elétrica | Consumo elétrico não controlável do edifício. | Building 1 tem valores baixos, por exemplo `0.5676` e `3.3253`; Building 3 chega a `24.333`; Building 4 atinge `56.7299` num excerto de ocupação elevada.  | É uma das variáveis centrais para comparar perfis reais de consumo entre edifícios.  |
| `dhw_demand` | Demanda térmica | Procura de AQS (Domestic Hot Water). | Building 1 mostra `0.0` no excerto inicial; Building 2 tem valores pequenos como `0.3507`, `1.1417` e `1.5540`; Building 3 apresenta picos maiores como `10.7`, `12.3` e `13.23`.  | Ajuda a perceber se o dataset tem comportamento residencial ou mais intensivo em AQS.  |
| `cooling_demand` | Demanda térmica | Procura de arrefecimento do edifício. | Building 1 passa de `0.0` para cerca de `9.42`–`13.7`; Building 2 sobe até `3.1532`; Building 3 atinge cerca de `40.9492`; Building 4 mostra picos elevados como `142.242` e `137.314`.  | Esta variável é muito relevante para identificar edifícios com comportamento forte de AC.  |
| `heating_demand` | Demanda térmica | Procura de aquecimento. | Nos excertos mostrados está sempre em `0.0`.  | Isto sugere um período dominado por cooling, coerente com o facto de as amostras estarem em junho.  |
| `solar_generation` | Geração local | Produção solar no edifício. | A série diária mostrada é igual entre edifícios nos excertos: `0.0` de noite, `12.0745` às 6h, `253.607` às h, `676.939` perto do meio-dia e volta a `0.0` ao fim do dia.  | Mesmo vendo a coluna em todos os CSV, a interpretação final deve ser cruzada com o schema para confirmar onde existe asset `pv`.  |
| `occupant_count` | Ocupação | Número de ocupantes no edifício. | Building 1 passa de `0.0` para `30.14749`; Building 2 mostra `0.0`, `37.041706`, `74.0341`, `14.1662`; Building 3 chega a `201.3674`; Building 4 atinge `254.75693`.  | É uma variável muito útil para comparar uso efetivo dos edifícios e proximidade a perfis como uma estação.  |
| `indoor_dry_bulb_temperature_cooling_set_point` | Controlo / conforto | Setpoint de arrefecimento. | Nos excertos alterna sobretudo entre `30.0`, `2.0` e `26.0`.  | Quando o setpoint desce para `26.0`, costuma coincidir com horas de operação HVAC.  |
| `indoor_dry_bulb_temperature_heating_set_point` | Controlo / conforto | Setpoint de aquecimento. | Também aparece sobretudo como `30.0`, `2.0` e `26.0` nos excertos.  | No período mostrado não parece ser a variável dominante, porque não há `heating_demand`.  |
| `hvac_mode` | Operação HVAC | Estado/modo de operação do HVAC. | Nos excertos aparecem `0` e `1`; tipicamente `1` coincide com horas de maior ocupação e cooling.  | Útil para perceber quando o edifício está em regime ativo de climatização.  |

## Variáveis de `pricing.csv`

| Campo | Categoria | Interpretação prática | Exemplos reais observados | Leitura para o cenário |
|---|---|---|---|---|
| `electricity_pricing` | Preço | Preço da eletricidade no time step atual. | Nos excertos aparecem principalmente dois patamares: `0.03025` e `0.06605`.  | O dataset parece usar um tarifário horário discreto simples, útil para testar shifting.  |
| `electricity_pricing_predicted_1` | Previsão de preço | Preço previsto para 1 passo à frente. | Exemplo: quando o preço atual ainda é `0.03025`, a previsão seguinte já pode subir para `0.06605`.  | Dá ao agente capacidade de antecipar a subida de custo.  |
| `electricity_pricing_predicted_2` | Previsão de preço | Preço previsto para 2 passos à frente. | Há linhas em que a sequência é `0.03025, 0.03025, 0.06605, 0.06605`.  | Permite planeamento com pequeno horizonte de previsão.  |
| `electricity_pricing_predicted_3` | Previsão de preço | Preço previsto para 3 passos à frente. | Também se observam transições como `0.03025, 0.03025, 0.03025, 0.06605`.  | Ajuda a preparar storage ou deslocar consumo antes do pico tarifário.  |

## Variáveis de `weather.csv`

| Campo | Categoria | Interpretação prática | Exemplos reais observados | Leitura para o cenário |
|---|---|---|---|---|
| `outdoor_dry_bulb_temperature` | Clima | Temperatura exterior atual. | Nos excertos varia aproximadamente entre `12.675` °C e `30.35` °C. 9 | Mostra um dia quente com forte potencial de cooling durante as horas centrais. 9 |
| `outdoor_relative_humidity` | Clima | Humidade relativa exterior atual. | Nos excertos varia de cerca de `13.3`% a `53.75`%. 9 | Pode afetar conforto e dinâmica térmica do edifício. 9 |
| `diffuse_solar_irradiance` | Clima / solar | Irradiância solar difusa atual. | Vai de `0.0` de noite até cerca de `102.166664`. 9 | Relevante para ganhos solares e parte da produção PV. 9 |
| `direct_solar_irradiance` | Clima / solar | Irradiância solar direta atual. | Vai de `0.0` até valores perto de `1001.1667`. 9 | É uma das variáveis mais importantes para explicar a forma da geração solar. 9 |
| `outdoor_dry_bulb_temperature_predicted_1` | Previsão clima | Temperatura exterior prevista a 1 passo. | Nos excertos aparecem valores como `14.690469`, `25.043474` e `30.43691`. 9 | Dá visão de curto prazo ao agente. 9 |
| `outdoor_dry_bulb_temperature_predicted_2` | Previsão clima | Temperatura exterior prevista a 2 passos. | Exemplos como `26.923693`, `30.13996` e `1.16422`. 9 | Útil para antecipar subida e descida térmica. 9 |
| `outdoor_dry_bulb_temperature_predicted_3` | Previsão clima | Temperatura exterior prevista a 3 passos. | Exemplos como `1.775156`, `32.59702` e `19.4339`. 9 | Alarga o horizonte de controlo preditivo. 9 |
| `outdoor_relative_humidity_predicted_1` | Previsão clima | Humidade exterior prevista a 1 passo. | Valores como `53.792732`, `2.49036` e `51.04264`. 9 | Complementa a leitura climática futura. 9 |
| `outdoor_relative_humidity_predicted_2` | Previsão clima | Humidade exterior prevista a 2 passos. | Exemplos `24.0047`, `14.701359` e `21.474209`. 9 | Pode ajudar em dinâmicas de conforto. 9 |
| `outdoor_relative_humidity_predicted_3` | Previsão clima | Humidade exterior prevista a 3 passos. | Exemplos `34.70524`, `53.44525` e `37.06449`. 9 | Variável auxiliar de previsão ambiental. 9 |
| `diffuse_solar_irradiance_predicted_1` | Previsão solar | Irradiância difusa prevista a 1 passo. | Exemplos `74.5601`, `1023.9264` não; cuidado, esse valor é da direta, enquanto na difusa surgem `74.5601`, `91.62056`, `114.249916`. 9 | Serve para antecipar a componente difusa da radiação. 9 |
| `diffuse_solar_irradiance_predicted_2` | Previsão solar | Irradiância difusa prevista a 2 passos. | Exemplos `95.26697`, `51.526196`, `114.249916` não; neste campo veem-se valores como `95.26697`, `51.526196`, `101.2692`. 9 | Útil em estratégias com previsão meteorológica. 9 |
| `diffuse_solar_irradiance_predicted_3` | Previsão solar | Irradiância difusa prevista a 3 passos. | Exemplos `0.0`, `25.03523`, `249.3142`. 9 | Ajuda a perceber transições entre noite, manhã e pico solar. 9 |
| `direct_solar_irradiance_predicted_1` | Previsão solar | Irradiância direta prevista a 1 passo. | Aparecem valores como `603.2702`, `1023.9264`, `0.0` e `39.4447`. 9 | Muito relevante para prever produção PV futura. 9 |
| `direct_solar_irradiance_predicted_2` | Previsão solar | Irradiância direta prevista a 2 passos. | Exemplos `974.1035`, `616.6733`, `33.169426`, `973.0609`. 9 | Mostra bem a evolução intradiária do recurso solar. 9 |
| `direct_solar_irradiance_predicted_3` | Previsão solar | Irradiância direta prevista a 3 passos. | Exemplos `0.0`, `421.9993`, `1033.972`, `942.7974`. 9 | Dá um horizonte útil para controlo preditivo de PV e storage. 9 |

## Leitura comparativa rápida entre edifícios

| Edifício | Sinais visíveis no excerto | Interpretação inicial |
|---|---|---|
| `Building_1` | Carga base baixa (`0.5676`), pouca ou nenhuma procura de AQS, cooling moderado quando entra em operação e ocupação até `30.14749`.  | Perfil relativamente leve e mais simples, possivelmente útil como referência de edifício com baixa carga.  |
| `Building_2` | Carga elétrica intermédia, AQS pequena mas frequente, cooling até `3.153175`, ocupação até `14.1662`.  | Perfil mais ativo que o Building 1, com mistura de consumo base e procura térmica relevante.  |
| `Building_3` | Cooling forte até `40.94921`, AQS com picos altos (`13.23`), ocupação até `201.3674`, carga base significativa.  | Perfil denso e interessante para estudar gestão combinada de ocupação, AQS e climatização.  |
| `Building_4` | Carga muito elevada, cooling muito forte com picos acima de `140`, ocupação até `254.75693`.  | É o edifício mais intenso dos excertos e pode ser o mais comparável a um uso fortemente concentrado como uma infraestrutura com grande afluência.  |

## Notas para comparação futura com Ermesinde

O `baeda_3dem` já mostra diversidade suficiente para criar uma grelha de comparação com Ermesinde baseada em cinco eixos: perfil de carga não deslocável, intensidade de cooling, presença/ausência e peso da ocupação, dependência solar e sensibilidade ao preço.  Em particular, `Building_4` e `Building_3` parecem mais promissores como ponto de partida para um cenário com atividade concentrada e procura térmica marcada, enquanto `Building_1` parece mais leve e menos exigente. 

Para a fase seguinte, vale a pena transformar esta tabela textual numa tabela de comparação quantitativa com mínimos, máximos, médias e presença de zeros por coluna, para depois a cruzar com o `phase_3_1`. 
