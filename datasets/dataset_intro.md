# baeda_3dem — leitura inicial do `schema.json`

## Papel do `schema.json`

No CityLearn, o `schema.json` funciona como a configuração estrutural do ambiente. É nele que ficam definidos os parâmetros gerais da simulação, as observações disponíveis, as ações possíveis, os edifícios incluídos, os assets energéticos associados a cada edifício, o tipo de agente, a reward function e, quando aplicável, a dinâmica térmica usada pelo building.  

Os ficheiros `Building_X.csv`, `weather.csv` e `pricing.csv` fornecem as séries temporais que alimentam essa estrutura. Ou seja, o `schema.json` diz ao CityLearn **o que existe e como está ligado**, enquanto os CSV fornecem os dados temporais que o ambiente vai ler ao longo da simulação.  

## Estrutura lógica de leitura

Uma forma simples de ler um dataset CityLearn é dividir o `schema.json` em três níveis:

1. **Configuração global do ambiente** — inclui horizonte temporal, granularidade, tipo de controlo e opções gerais da simulação.
2. **Catálogo global de observações e ações** — define tudo o que o ambiente pode disponibilizar ao agente e tudo o que o agente pode controlar.
3. **Configuração por building** — indica que ficheiros cada edifício usa, que equipamentos tem, que observações e ações ficam efetivamente ativas nesse edifício e que modelo dinâmico foi associado. 

No dataset `baeda_3dem`, a configuração mostra `central_agent: false`, o que significa que o controlo está organizado por building e não por um agente central único. Além dIsto, cada building aponta para o seu próprio `BuildingX.csv`, usando em paralelo `weather.csv` e `pricing.csv` como fontes comuns de clima e preço. 

## Como identificar os principais equipamentos

No schema, os equipamentos aparecem por nomes técnicos e não por rótulos informais. Para leitura prática, a correspondência principal é esta:

| Chave no schema | Interpretação prática |
|---|---|
| `coolingdevice` | Sistema de arrefecimento, normalmente o equivalente prático ao “AC”.  |
| `heatingdevice` | Sistema de aquecimento. |
| `dhwdevice` | Sistema de AQS (*Domestic Hot Water*). |
| `pv` | Sistema fotovoltaico.  |
| `coolingstorage` | Armazenamento térmico de frio.   |
| `heatingstorage` | Armazenamento térmico de aquecimento.   |
| `dhwstorage` | Armazenamento térmico de AQS.   |
| `electricalstorage` | Bateria elétrica / BESS.   |

Assim, quando o objetivo é perceber rapidamente se um dataset tem AC, PV, AQS ou bateria, basta procurar estas chaves dentro de cada building. A presença da chave indica que o asset existe; os atributos internos dizem depois como ele foi parametrizado. 

Dentro de alguns datasets, existe um .md para tentar ler o que "compõe" o dataset. 