# EC_Ermesinde

Dataset horario de base para uma estacao ferroviaria em Ermesinde.

## Ficheiros

- `schema.json`: configuracao do simulador.
- `Building_1.csv`: cargas e estado termico da estacao, com 8760 passos horarios.
- `weather.csv`: meteorologia e previsoes, com 8760 passos horarios.
- `pricing.csv`: tarifa sintetica provisoria, com 8760 passos horarios.

## Ajustes de compatibilidade

O material de origem foi preservado, exceto nas correcoes necessarias para o
contrato do simulador:

1. O schema foi normalizado de `schema_baseline.json.json` para `schema.json`,
   para o dataset poder ser descoberto pelo nome `EC_Ermesinde`.
2. Foram adicionadas a `Building_1.csv` as colunas obrigatorias
   `dhw_demand` e `solar_generation`, ambas a zero. Nao foram fornecidas
   medicoes de AQS nem de producao fotovoltaica.
3. A referencia inicialmente inexistente a `pricing.csv` foi preenchida com
   uma tarifa sintetica provisoria e a observacao `electricity_pricing` ficou
   ativa.

## Tarifa sintetica provisoria

Os valores de `pricing.csv` nao representam um tarifario comercial real e nao
devem ser usados para tirar conclusoes economicas. Foram gerados de forma
deterministica, apenas para permitir testar observacoes, custos e algoritmos:

- 01:00-07:00: 0.120 EUR/kWh;
- 08:00-17:00 e 23:00-24:00: 0.180 EUR/kWh;
- 18:00-22:00: 0.260 EUR/kWh.

As colunas `electricity_pricing_predicted_1/2/3` sao previsoes perfeitas da
mesma tarifa sintetica a 6, 12 e 24 horas, respetivamente. Antes de uma analise
real, estes valores devem ser substituidos por uma tarifa contratada ou por
dados de mercado, com impostos e restantes componentes claramente definidos.

## Unidades e limitacoes conhecidas

- Resolucao: 3600 s por passo.
- Cargas e demandas: kWh por passo.
- Temperaturas: graus Celsius.
- Irradiancia: W/m2.
- Preco da eletricidade: EUR/kWh (sintetico e provisório).
- `non_shiftable_load` e constante em 0.328 kWh por hora (media de 0.328 kW).
  O valor e tecnicamente valido, mas deve ser confirmado: e muito baixo para
  representar a carga eletrica total de uma estacao ferroviaria e pode ser
  apenas uma carga parcial ou normalizada.
- `indoor_dry_bulb_temperature` acompanha quase exatamente a temperatura
  exterior (correlacao 0.999962 e diferenca absoluta media de 0.051 C). Isto
  pode fazer sentido para uma zona aberta/semiaberta, mas nao para um espaco
  interior climatizado sem justificacao adicional.
- O dataset atual nao tem qualquer acao ativa; e uma baseline de consumo, nao
  um caso de controlo energetico.

## Smoke test

```python
from citylearn.citylearn import CityLearnEnv

env = CityLearnEnv("EC_Ermesinde", episode_time_steps=24, render_mode="none")
observations, info = env.reset(seed=0)
env.close()
```
