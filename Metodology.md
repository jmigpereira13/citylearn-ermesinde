# README — Metodologia de Cálculo para o Dataset CityLearn da Estação de Ermesinde

## Objetivo

Este ficheiro descreve a lógica usada para construir o dataset da estação de comboios de Ermesinde para simulação no **CityLearn**, incluindo:

- cálculo das potências de `non_shiftable_load`;
- separação entre cargas fixas e cargas dinâmicas;
- dimensionamento e perfil horário das **escadas rolantes**;
- parametrização do **HVAC** para o `schema.json`;
- perfil de ocupação e horários de maior utilização;
- dimensionamento preliminar do sistema **fotovoltaico (PV)**;
- lógica de conversão dos valores para o formato esperado pelo CityLearn.

***

## Estrutura geral do modelo

O edifício principal da estação é modelado como **Building_1** no CityLearn. Neste edifício são considerados três grandes blocos de consumo:

1. **Cargas fixas** → equipamentos sempre ligados ou quase sempre ligados.
2. **Cargas dinâmicas** → equipamentos cujo consumo depende da utilização, principalmente escadas rolantes e elevadores.
3. **HVAC** → sistema de climatização virtual introduzido apenas para efeitos de simulação.

A produção local de energia é representada por:

4. **PV** → geração fotovoltaica horária.
5. **BESS** → armazenamento elétrico, se aplicável no cenário.

***

## 1. Non-shiftable load

No CityLearn, a coluna `non_shiftable_load` representa a carga elétrica que **não pode ser controlada diretamente pelo agente**. No caso da estação, esta coluna inclui:

- displays informativos;
- televisões;
- placares eletrónicos;
- portas automáticas;
- caixas MB;
- terminais Andante;
- equipamento da bilheteira;
- escadas rolantes;
- elevadores.

A energia horária é calculada como:

$$
E_{nsl}(h) = \left(\sum_i P_i \cdot f_i(h)\right) \cdot 10^{-3}
$$

onde:
- $$P_i$$ = potência nominal do equipamento $$i$$, em W;
- $$f_i(h)$$ = fator de utilização do equipamento na hora $$h$$;
- o resultado final é convertido para **kWh por hora**.

Na prática, o Excel trabalha primeiro em **W** e no final converte para **kWh/h** dividindo por 1000.

***

## 2. Cargas fixas

As cargas fixas correspondem aos equipamentos com funcionamento constante ou quase constante, podendo apenas variar entre regime normal e standby noturno.

### Equipamentos considerados

| Equipamento | Quantidade | Potência unitária (W) | Potência total (W) |
|---|---:|---:|---:|
| Televisões Teleste | 4 | 120 | 480 |
| Display central grande | 1 | 350 | 350 |
| Displays médios plataforma | 8 | 100 | 800 |
| Displays curtos piso inferior | 4 | 60 | 240 |
| Cartaz/placar eletrónico | 1 | 150 | 150 |
| Caixas MB | 2 | 50 | 100 |
| Estações Andante | 3 | 80 | 240 |
| Equipamento bilheteira | 1 conjunto | 300 | 300 |
| **Total base fixa** |  |  | **2 660 W** |

### Regra de utilização horária

- **Período normal de funcionamento**: fator de utilização = **1.0**
- **Madrugada / estação praticamente fechada**: fator de utilização = **0.1**

Logo:

- carga fixa em funcionamento normal = **2660 W**
- carga fixa em standby = **266 W**

## 3. Cargas dinâmicas — escadas rolantes

As escadas rolantes são tratadas como **non_shiftable_load dinâmico**, porque não são controláveis, mas o seu consumo depende do fluxo de passageiros.

### Fórmula física de base

A potência mecânica é estimada por:

$$
P_{nom} = \frac{n \cdot M \cdot g \cdot V \cdot \sin(\theta)}{\eta}
$$

onde:

- $$n$$ = número médio de passageiros transportados em simultâneo;
- $$M$$ = massa média por passageiro = 75 kg;
- $$g$$ = 9.81 m/s²;
- $$V$$ = velocidade nominal = 0.5 m/s;
- $$\theta$$ = inclinação = 30°;
- $$\eta$$ = rendimento global = 0.70.

Com base na observação da estação e nas potências já definidas na folha **B. Cargas Dinâmicas**, as escadas foram divididas em dois grupos.

***

## 4. Perfil horário de ocupação

Como não existem ainda medições horárias reais de passageiros, foi definido um **perfil de ocupação proxy** baseado nos horários típicos de comboios suburbanos e no comportamento observado na estação.

### Dias úteis

| Período | Fator de ocupação |
|---|---:|
| 00h–06h | 0.1 |
| 06h–09h | 0.9 |
| 09h–16h | 0.4 |
| 16h–19h | 0.8 |
| 19h–23h | 0.4 |
| 23h–24h | 0.1 |

### Sábado

| Período | Fator de ocupação |
|---|---:|
| 00h–08h | 0.1 |
| 08h–20h | 0.4 |
| 20h–24h | 0.1 |

### Domingo / feriado

| Período | Fator de ocupação |
|---|---:|
| 00h–09h | 0.1 |
| 09h–19h | 0.2 |
| 19h–24h | 0.1 |

Este fator é usado para multiplicar a potência dinâmica nominal das escadas rolantes e, se necessário, também dos elevadores.

### Exemplo de fórmula Excel

Se a potência plena total das escadas estiver em `F20` e o fator horário estiver em `G20`:

```excel
=F20*G20/1000
```

Resultado: consumo horário das escadas em kWh.

***

## 5. Elevadores

Os elevadores também podem ser incluídos como carga dinâmica dentro do `non_shiftable_load`.

### Valores assumidos

| Equipamento | Quantidade | P eco (W/un) | P plena (W/un) |
|---|---:|---:|---:|
| Elevadores Schmitt+Sohn | 3 | 200 | 6000 |

Se necessário:

- potência total eco = `3 × 200 = 600 W`
- potência total plena = `3 × 6000 = 18 000 W`

O uso horário pode ser simplificado com o mesmo fator de ocupação das escadas, ou com um fator reduzido próprio.

***

## 6. HVAC virtual para o schema.json

Apesar de a estação real não possuir climatização total do espaço, foi decidido modelar um **HVAC virtual** para efeitos de simulação no contexto do projeto europeu.

O equipamento de referência adotado é o **Daikin EWYT040**, com potência térmica nominal próxima de 39.9 kW.

### Conceito de COP

O **COP (Coefficient of Performance)** é a razão entre a energia térmica fornecida e a energia elétrica consumida:

$$
COP = \frac{Q_{th}}{P_{el}}
$$

Se o sistema tiver COP = 3.16, significa que para fornecer 3.16 kW térmicos consome 1 kW elétrico.

Logo, para converter necessidade térmica em potência elétrica:

$$
P_{el,HVAC}(h) = \frac{Q_{cooling}(h)}{COP}
$$

### Parâmetros para o `schema.json`

```json
"cooling_device": {
  "type": "HeatPump",
  "nominal_power": 39.9,
  "efficiency": 3.16,
  "target_cooling_temperature": 24.0,
  "loss_coefficient": 0.0
},
"heating_device": {
  "type": "HeatPump",
  "nominal_power": 39.9,
  "efficiency": 3.41,
  "target_heating_temperature": 21.0,
  "loss_coefficient": 0.0
}
```

### Interpretação dos parâmetros
- `nominal_power` → potência térmica nominal do equipamento;
- `efficiency` → COP/EER usado na conversão entre energia térmica e elétrica;
- `target_cooling_temperature` → setpoint de arrefecimento;
- `target_heating_temperature` → setpoint de aquecimento;
- `loss_coefficient` → perdas adicionais assumidas no modelo.

### Nota prática
Se o CityLearn usar diretamente `cooling_demand` em kWh térmicos, então o consumo elétrico do equipamento será obtido internamente com base na eficiência definida no equipamento.

***

## 7. Perfil HVAC no Excel

Se for necessário construir um perfil simplificado no Excel, pode usar-se uma lógica sazonal:

### Verão
- HVAC ativo entre 09h e 21h
- carga relativa entre 0.3 e 1.0
- maior solicitação em dias úteis e nas horas centrais

### Inverno
- HVAC ativo entre 07h e 20h
- carga mais moderada
- foco em conforto térmico em vez de arrefecimento intenso

<!-- ### Fórmula Excel simplificada
Se a potência térmica máxima estiver em `B10`, o fator horário em `C10` e o COP em `D10`:

```excel
=(B10*C10)/D10
```

Resultado: potência elétrica horária estimada do HVAC.
-->
*** 

## 8. Sistema fotovoltaico (PV)
O sistema PV foi refinado para evitar uma estimativa excessivamente otimista da área disponível.

### Dados solares para Ermesinde

Foram considerados dados do **PVGIS** para a zona de Ermesinde / Porto, com:
- latitude: **41.18°**
- longitude: **-8.49°**
- inclinação: **35°**
- orientação: **Sul**
- perdas totais do sistema: **14%**

Resultado principal:
- produção anual específica = **1398.81 kWh/kWp/ano**

### Produção mensal específica

| Mês | Produção por 1 kWp (kWh) |
|---|---:|
| Janeiro | 72.34 |
| Fevereiro | 93.65 |
| Março | 118.47 |
| Abril | 126.53 |
| Maio | 144.88 |
| Junho | 142.36 |
| Julho | 157.88 |
| Agosto | 155.07 |
| Setembro | 140.04 |
| Outubro | 106.67 |
| Novembro | 74.14 |
| Dezembro | 66.78 |
| **Total anual** | **1398.81** |

***

## 9. Refinamento da área útil de cobertura

A área inicialmente atribuída ao PV foi considerada demasiado aproximada, pelo que foi adotada uma abordagem mais conservadora.

### Hipótese de cálculo
- área bruta estimada de cobertura principal = **600 m²**
- desconto por obstáculos, acessos técnicos, sombras e margens de segurança = **40%**

Logo:

$$
A_{útil} = 600 \cdot (1 - 0.40) = 360\ m^2
$$

### Painel de referência
Foi considerado um painel de aproximadamente:

- **400 Wp**
- área unitária ≈ **1.96 m²**

Como é necessário deixar espaçamento e acessibilidade, foi usado um fator adicional de ocupação de **1.1**.

### Número de painéis
$$
N_{painéis} = \frac{360}{1.96 \cdot 1.1} \approx 167
$$

### Potência instalada
$$
P_{instalada} = 167 \cdot 0.400 = 66.8\ kWp
$$

### Produção anual estimada
$$
E_{PV,anual} = 66.8 \cdot 1398.81 \approx 93\,440\ kWh/ano
$$

Assim, o cenário mais defensável neste momento é de aproximadamente:

- **167 painéis**
- **66.8 kWp**
- **~93.4 MWh/ano**

***

## 10. Parâmetros PV para o schema.json

Exemplo de parametrização:

```json
"pv": {
  "type": "PV",
  "nominal_power": 66800,
  "installed_capacity": 66.8,
  "efficiency": 0.204,
  "loss_coefficient": 0.14
}
```

### Interpretação
- `nominal_power` → potência instalada em Wp;
- `installed_capacity` → potência instalada em kWp;
- `efficiency` → eficiência nominal do módulo;
- `loss_coefficient` → perdas globais do sistema.

***

## 11. Conversão para séries horárias do CityLearn

No Excel, o objetivo final é obter uma série horária com pelo menos as seguintes componentes:

- `non_shiftable_load`
- `cooling_demand`
- `solar_generation`
- `occupant_count` (se existir)

### Estrutura recomendada

Para cada hora do ano:

1. calcular a carga fixa;
2. calcular a carga dinâmica das escadas rolantes;
3. adicionar elevadores, se aplicável;
4. calcular HVAC elétrico ou térmico conforme a folha usada;
5. calcular geração PV;
6. exportar os resultados para o formato CSV do CityLearn.

### Fórmula resumo

```text
non_shiftable_load = carga_fixa + escadas_rolantes + elevadores
```

```text
balanço_elétrico = non_shiftable_load + HVAC_elétrico - solar_generation
```

***

<!-- ## 12. Notas finais
- As escadas rolantes são o principal foco de intervenção do modelo.
- O HVAC é virtual e serve apenas para compatibilizar o caso de estudo com cenários europeus mais exigentes.
- A área PV deve ainda ser validada com melhor levantamento geométrico da cobertura.
- Se forem obtidas medições reais de passageiros/hora, o perfil de ocupação deve substituir os fatores proxy atualmente usados.
- As fórmulas do Excel devem referenciar sempre células de entrada, evitando hardcodes dentro das fórmulas finais.

***

## 13. Sugestão prática para organização do Excel

### Folha `Potencias_Nominais`

- valores base dos equipamentos;
- potências unitárias e totais;
- fontes e observações.

### Folha `Escadas_Rolantes`

- tabelas Tipo A e Tipo B;
- fatores horários;
- perfis úteis / sábado / domingo.

### Folha `HVAC`

- COP;
- potência térmica nominal;
- fator horário;
- consumo elétrico calculado.

### Folha `PV`

- área bruta;
- área útil;
- área por painel;
- número de painéis;
- potência instalada;
- produção mensal e anual.

### Folha `Simulação`

- série temporal horária final para exportação. -->