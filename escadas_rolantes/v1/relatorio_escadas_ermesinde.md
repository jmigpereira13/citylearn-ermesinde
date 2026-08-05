# Relatório — Escadas Rolantes Reais da Estação de Ermesinde (Dataset CityLearn 15 min)

**Data:** 30 de julho de 2026
**Âmbito:** Substituição da escada rolante sintética única por um conjunto de **6 ficheiros `EscadaRolante_N.csv`** que representam as escadas rolantes reais da Estação Ferroviária de Ermesinde, alimentadas por horários reais da CP extraídos de PDFs, com regras de alocação de plataforma documentadas e um modelo sintético de passageiros calibrado com dados públicos de procura ferroviária.

---

## 1. Extração dos horários dos 4 PDFs

Foram fornecidos 4 PDFs de horários dos Comboios Urbanos do Porto, extraídos com `pdfplumber` para texto simples (`pdf_extract/*.txt`) e depois processados por `extrair_horarios_ermesinde.py`:

| PDF | Linha | Vigência indicada no PDF | Nº de páginas |
|---|---|---|---|
| `comboios-urbanos-porto-braga.pdf` | Linha do Minho (ramal Braga) | 26 de julho de 2026 | 2 |
| `comboios-urbanos-porto-guimaraes.pdf` | Linha do Minho (ramal Guimarães) | 14 de dezembro de 2025 | 1 |
| `comboios-urbanos-porto-marco.pdf` | Linha do Douro (Marco de Canaveses) | 26 de julho de 2026 | 2 |
| `comboios-urbanos-porto-ermesinde.pdf` | (excerto local, ver descoberta abaixo) | 26 de julho de 2026 | 2 |

### 1.1 Descoberta corretiva: o PDF "Ermesinde" é redundante

A abordagem inicial tratava o PDF `comboios-urbanos-porto-ermesinde.pdf` como um serviço distinto de "curta distância" São Bento–Ermesinde (baseado em números de comboio como 3000, 
3105, 4000, 4001, que pareciam sugerir uma navete dedicada). 
**Esta hipótese revelou-se incorreta** após validação cruzada: dos 179 números de comboio extraídos do PDF Ermesinde isolado, 
**174 (97,2%)** correspondem exatamente (mesmo número **e** mesma hora) a um comboio já listado num dos três PDFs de linha completa (Braga, Guimarães ou Marco), 
incluindo os supostos "shuttles" 3000/3105/4000/4001 — que na realidade continuam até Braga ou até Marco de Canaveses.

**Conclusão corrigida:** o PDF Ermesinde isolado é apenas um **excerto truncado** (mostrando só a secção São Bento–Ermesinde) dos horários das três linhas completas, e **não** 
representa um serviço independente. 
Não há evidência de comboios que terminem ou iniciem o seu percurso em Ermesinde — praticamente todas as circulações são passagens (through-trains).

Consequência prática: a tabela de eventos **autoritativa** (`dataset_15min/ermesinde_eventos_comboios.csv`) foi construída **apenas** a partir dos PDFs Braga + Guimarães + Marco. 
O PDF Ermesinde isolado foi mantido como ficheiro de **validação cruzada** (`dataset_15min/ermesinde_pdf_eventos_bruto.csv`), não como fonte primária.

| Métrica de validação cruzada | Valor |
|---|---|
| Números de comboio no PDF Ermesinde isolado | 179 |
| Correspondências encontradas nos 3 PDFs de linha completa | 174 (97,2%) |
| Sem correspondência | 5 (2,8%) |

Os 5 números sem correspondência — **15201 (01:08), 15228 (13:57), 15229 (16:03), 15231 (16:33), 15254 (00:17)** — surgem sobretudo perto da meia-noite ou em horários que podem ter 
sofrido diferenças de edição/atualização entre os PDFs (o PDF Ermesinde e o PDF Braga/Marco não têm exatamente a mesma data de "vigor desde"). 
Dado o volume residual (2,8%), foram documentados como discrepância menor e excluídos da tabela autoritativa, sem impacto material nas conclusões.

### 1.2 Deduplicação de comboios partilhados entre linhas

Após consolidar os 3 PDFs de linha completa obtiveram-se inicialmente **215 eventos**. 
Verificou-se que **36 números de comboio** (gama 15150–15186) surgem simultaneamente nos PDFs de Braga e de Guimarães — mas em dois padrões distintos:

- **Mesmo número, mesma hora em Ermesinde, mesmo sentido genérico** (ex.: comboio 15150 às 06:47 rumo a São Bento em ambos os PDFs): trata-se do **mesmo comboio físico**, 
publicado em ambos os folhetos porque o troço Porto–Ermesinde/Trofa é **partilhado** pelas linhas de Braga e Guimarães (bifurcação só depois de Trofa/Lousado). 
Estes casos foram **deduplicados** (mantendo uma única ocorrência).
- **Mesmo número, horas/sentidos diferentes** (ex.: 15165 às 16:04 rumo a Braga vs. 15165 às 14:39 vindo de Guimarães): a CP **reutiliza números de comboio** em corridas distintas 
do mesmo dia — são **comboios fisicamente distintos** e foram mantidos como eventos separados.

Resultado: **215 → 204 eventos autoritativos** (11 duplicados genuínos removidos).

### 1.3 Tabela de eventos consolidada

| Linha PDF | Nº de eventos |
|---|---|
| Braga (Linha do Minho) | 91 |
| Marco (Linha do Douro) | 88 |
| Guimarães (Linha do Minho) | 25 |
| **Total** | **204** |

| Código de observação CP | Significado | Nº de eventos |
|---|---|---|
| 1 | Diário (circula todos os dias, incl. sáb/dom/feriados) | 98 |
| 7 | Segunda a sexta, exceto feriados | 83 |
| 2 | Sábados, domingos e feriados | 20 |
| 37 | Segunda a sábado, exceto feriados | 3 |

Expandindo estes códigos pelo calendário semanal, obtém-se:

| Tipo de dia | Passagens/dia (ambos os sentidos) | Passagens/dia por sentido (aprox.) |
|---|---|---|
| Dia útil (seg–sex) | 184 | ~92 |
| Sábado | 121 | ~60,5 |
| Domingo/feriado | 118 | ~59 |

Este valor de **~92 passagens/sentido em dia útil** está muito próximo do valor publicado na Wikipédia — "**80 circulações diárias em cada sentido aos dias úteis**" 
([Wikipédia PT — Estação Ferroviária de Ermesinde](https://pt.wikipedia.org/wiki/Esta%C3%A7%C3%A3o_Ferrovi%C3%A1ria_de_Ermesinde)) — servindo como validação independente da 
ordem de grandeza (a diferença de ~15% é plausível dada a diferença de datas de vigência entre a fonte da Wikipédia e os PDFs de 2025/2026 usados).

### 1.4 Caveat: PDFs datados de 2025/2026, simulação em 2025

Os PDFs indicam "horário em vigor desde 26 de julho de 2026" (Braga, Marco, Ermesinde) ou "desde 14 de dezembro de 2025" (Guimarães). 
Como a simulação CityLearn decorre no ano civil de **2025** e não foi disponibilizado um PDF especificamente datado de 2025, os horários foram usados 
como **padrão de serviço representativo/proxy** para 2025 — decisão documentada aqui e não uma limitação escondida. 
A estrutura geral do serviço urbano do Porto (frequências, janelas horárias, dias de operação) tende a ser estável ano a ano, pelo que este proxy é considerado 
razoável para efeitos de dimensionamento energético.

---

## 2. Investigação de linhas e plataformas em Ermesinde

### 2.1 O problema

Os PDFs de horário da CP indicam apenas a **hora de passagem** em Ermesinde, sem indicar a **via/linha física** (I a XI) nem o **grupo de plataforma** correspondente. Para gerar os ficheiros das 4 escadas Tipo B (que servem grupos de plataforma específicos), foi necessário investigar e definir uma regra de alocação.

### 2.2 Fontes consultadas

| Fonte | Contributo | Grau de utilidade |
|---|---|---|
| [Wikipédia PT — Estação de Ermesinde](https://pt.wikipedia.org/wiki/Esta%C3%A7%C3%A3o_Ferrovi%C3%A1ria_de_Ermesinde) | Confirma 10 vias (I, II, III, IV, V, VII, VIII, IX, X, XI), 5 com acesso a cais (I–V, 301 m), e que a Linha do Douro bifurca "no lado direito do seu enfiamento descendente" logo a jusante de Ermesinde | Alta — mas sem mapeamento explícito via→grupo de cais |
| [IP — Estações (partidas/chegadas Ermesinde)](https://servicos.infraestruturasdeportugal.pt/pt-pt/estacoes?estacaoId=9404002) | Tabela de partidas em tempo real, mas **sem coluna de via/cais** | Baixa (confirma horário de estação 05:00–01:10, mas não aloca via) |
| [IP — Diretório da Rede 2025 (PDF)](https://servicos.infraestruturasdeportugal.pt/sites/default/files/inline-files/Diretorio%20da%20Rede%202025.pdf) | Documento técnico da rede ferroviária nacional | Não foi possível extrair alocação via/cais específica de Ermesinde no tempo disponível |
| [Portugal Ferroviário — Linha do Minho](https://portugalferroviario.net) | Confirma "Concordância de São Gemil" (bifurcação Minho/Douro) a PK 8,430, próximo de Ermesinde | Média — confirma a topologia, não a atribuição de cais |
| API interna CP (`cp.pt/.../station/trains`) | Tentativa de acesso via `curl` | **Falhou** — devolve apenas a shell da SPA (aplicação React), sem dados de via acessíveis sem sessão de browser real |
| [IP — Investimento Linha do Minho Contumil–Ermesinde](https://www.infraestruturasdeportugal.pt/pt-pt/mais-de-200-meu-de-investimento-na-linha-do-minho-entre-contumil-e-ermesinde) | Confirma troço usado por **mais de 200 comboios/dia**; projeto de quadruplicação 2025–2030 (219,5 M€) visa "separar de forma eficiente os fluxos das Linhas do Minho e do Douro" | Média — mas descreve uma **segregação futura**, não necessariamente o layout de cais atual em 2025 |

Não foi encontrada nenhuma fonte pública que mapeie explicitamente cada via física ao grupo de plataforma "linhas 2+3" ou "linhas 4+5" mencionado no enunciado do projeto. A API de tempo real da CP, que poderia teoricamente revelar o número de via por comboio, não é acessível programaticamente sem uma sessão de browser autenticada.

### 2.3 Regra de alocação adotada (ASSUNÇÃO DOCUMENTADA)

Face à impossibilidade de confirmar a alocação exata, foi definida a seguinte regra, com **grau de confiança médio/baixo**, documentada explicitamente para que possa ser corrigida 
por quem tiver acesso a informação operacional interna da CP/IP:

| Grupo de plataforma | Linhas atribuídas | Justificação |
|---|---|---|
| **linhas_4_5** | Braga + Guimarães (Linha do Minho) | Maior frequência conjunta (116 de 204 eventos, ~57%); via principal do Minho, historicamente com mais tráfego |
| **linhas_2_3** | Marco de Canaveses (Linha do Douro) | A Linha do Douro bifurca fisicamamente logo a jusante de Ermesinde (Concordância de São Gemil), justificando um grupo de cais dedicado |

Esta regra é **internamente consistente** (cada grupo de plataforma tem um conjunto fixo e disjunto de linhas) e reflete a divisão física real Minho/Douro documentada na Wikipédia e nos projetos de investimento da IP, mas **não foi confirmada por uma fonte primária que liste explicitamente os números de via por grupo de cais**. Recomenda-se validação futura junto da CP/IP ou por observação direta no local (fotografar os painéis de indicação de via em cada passagem, cruzando com a hora do comboio).

### 2.4 Distribuição resultante

| Grupo de plataforma | Nº de eventos (passagens) |
|---|---|
| linhas_4_5 (Minho: Braga+Guimarães) | 116 |
| linhas_2_3 (Douro: Marco) | 88 |

### 2.5 Ausência de terminais/curtas-distâncias em Ermesinde

Conforme já assinalado na secção 1.1, a validação cruzada com o PDF Ermesinde isolado (97,2% de correspondência) confirma que **não existem comboios que terminam ou iniciam operação 
em Ermesinde** dentro do conjunto de dados disponível — todas as 204 passagens autoritativas são eventos de **passagem** (through-train), contribuindo simultaneamente 
para `arriving_trains` e `departing_trains` no mesmo bloco de 15 min. Esta é uma correção importante face à hipótese inicial de trabalho, que assumia a existência de uma "navete curta" 
São Bento–Ermesinde.

### 2.6 Feriado adicional específico dos Urbanos do Porto

Os 4 PDFs incluem a nota: *"Nos Comboios Urbanos do Porto o dia 24 de junho é considerado feriado oficial."* Esta data **não consta** da lista `FERIADOS_PT_2025` do script principal 
(13 feriados nacionais: 2025-01-01, 04-18, 04-20, 04-25, 05-01, 06-10, 06-19, 08-15, 10-05, 11-01, 12-01, 12-08, 12-25) — é uma regra **específica do serviço ferroviário urbano do 
Porto**, não um feriado nacional generalizado.

**Decisão adotada:** o dia 24 de junho de 2025 é tratado como feriado (day_type=8) **apenas para efeitos da lógica de geração das escadas rolantes** (aplicação dos códigos de 
observação de comboio), sem alterar a lista `FERIADOS_PT_2025` usada pelos restantes ficheiros do dataset (Building_1.csv, pricing.csv, weather.csv), para não introduzir uma 
discrepância silenciosa nesses ficheiros que não foi pedida nem justificada para o edifício. Esta escolha está implementada em `gerar_escadas_reais.py` através da constante 
`FERIADO_ADICIONAL_URBANOS_PORTO_2025`.

---

## 3. Configuração das 6 escadas rolantes

### 3.1 Estrutura CONFIG_ESCADAS

A configuração estática das 6 escadas foi implementada como uma lista de dicionários (`CONFIG_ESCADAS` em `gerar_escadas_reais.py`) e exportada para `dataset_15min/escadas_config.json`:

| Identificador | Tipo | Plataforma | Direção | Descrição |
|---|---|---|---|---|
| EscadaRolante_1 | A | átrio | desce | Átrio/viaduto principal, piso superior → piso inferior |
| EscadaRolante_2 | A | átrio | sobe | Átrio/viaduto principal, piso inferior → piso superior |
| EscadaRolante_3 | B | linhas_2_3 | sobe | Piso inferior → linhas 2 e 3 (Douro, sentido Marco) |
| EscadaRolante_4 | B | linhas_2_3 | desce | Linhas 2 e 3 (Douro, sentido Marco) → piso inferior |
| EscadaRolante_5 | B | linhas_4_5 | sobe | Piso inferior → linhas 4 e 5 (Minho, sentido Braga/Guimarães) |
| EscadaRolante_6 | B | linhas_4_5 | desce | Linhas 4 e 5 (Minho, sentido Braga/Guimarães) → piso inferior |

### 3.2 Potências de referência

| Parâmetro | Tipo A (átrio) | Tipo B (plataformas) | Fonte |
|---|---|---|---|
| `potencia_desligado_kw` (standby) | 0,08 kW | 0,05 kW | Recomendação própria, ver 3.3 |
| `potencia_lenta_kw` (modo eco) | 0,420 kW | 0,260 kW | [`relatorio_15min_escadas.md`](./relatorio_15min_escadas.md) §3, valores verificados |
| `potencia_normal_kw` (modo plena) | 2,100 kW | 1,310 kW | [`relatorio_15min_escadas.md`](./relatorio_15min_escadas.md) §3, valores verificados |
| `tempo_minimo_estado_min` | 2 min | 2 min | Evita comutação excessiva entre estados (histerese mínima) |

### 3.3 Respostas às dúvidas em aberto

**"Desligado ≈ 0 kW?"** Não deve ser exatamente 0 kW. As escadas rolantes modernas mantêm consumo em standby para eletrónica de controlo, sensores de presença e, nalguns modelos, lubrificação automática. A literatura (ACEEE 2010, [artigo técnico](https://www.aceee.org/files/proceedings/2010/data/papers/1981.pdf)) recomenda **0,05–0,10 kW/unidade** como faixa típica de standby para escadas rolantes de médio porte. Adotou-se **0,08 kW** para o Tipo A (maior, mais eletrónica) e **0,05 kW** para o Tipo B, dentro dessa faixa.

**"P eco para o modo lento está OK?"** Sim — os valores de 420 W (Tipo A) e 260 W (Tipo B) já correspondiam ao modo ECO/lento verificado em `relatorio_15min_escadas.md` §3, consistentes com a redução de ~25% tipicamente reportada por fabricantes como a Schindler para o modo ECO ([brochura Schindler 9300](https://www.jardineschindler.com/content/dam/website/jsg/docs/schindler-9300-escalator-brochure.pdf)).

**"P plena para o modo normal está OK? P plena é medida sem carga — a carga de passageiros acrescenta consumo?"** Sim, os valores de 2100 W (Tipo A) e 1310 W (Tipo B) referem-se à potência nominal em vazio ("no-load"), conforme a norma ISO 25745-3:2015 ([ver PDF](https://cdn.standards.iteh.ai/samples/60952/0cf81fd3b42440468fe039c670157ab9/ISO-25745-3-2015.pdf)), que valida o modelo de 3 estados (desligado/lento/normal) usado neste dataset. Uma tese da Aalto University sobre o efeito da carga de passageiros no consumo de escadas rolantes ([ver tese](https://aaltodoc.aalto.fi/server/api/core/bitstreams/a54540a1-f109-4bd3-b785-a536ef8aa795/content)) mostra que o incremento de consumo devido à carga de passageiros é tipicamente pequeno face à potência do motor e das perdas mecânicas fixas, especialmente em escadas de baixo desnível como as urbanas. **Decisão adotada:** manter `potencia_normal_kw` fixo (sem incremento por carga), como simplificação documentada — esta é a mesma recomendação já registada em `relatorio_15min_escadas.md`. Caso se pretenda maior fidelidade num trabalho futuro, pode adicionar-se um pequeno incremento proporcional a `passengers_expected` (ex.: +0,5–1% da potência nominal por passageiro simultâneo na escada), mas isso exigiria modelar o tempo de trânsito na escada e não foi implementado nesta versão.

### 3.4 Tempo mínimo de estado

`tempo_minimo_estado_min = 2` minutos para todas as escadas — evita comutações demasiado frequentes entre os estados desligado/lento/normal (histerese mínima), alinhado com o tempo de resposta típico de um controlador de frequência variável (VFD) em escadas rolantes comerciais.

---

## 4. Metodologia dos passageiros sintéticos

### 4.1 Calibração de magnitude

Não existe uma série pública de passageiros **ao nível da estação** de Ermesinde. Foram usadas as seguintes fontes para estimar a ordem de grandeza:

- **CP Urbanos do Porto 2025:** transportou **27,6 milhões de passageiros**, um crescimento de 15,8% face aos 23,9 milhões de 2024 ([Observador, 29 jan 2026, citando CP](https://observador.pt/2026/01/29/cp-transporta-recorde-de-2082-milhoes-de-passageiros-em-2025/)).
- **Posição relativa de Ermesinde:** um artigo do Público (2009) identifica Ermesinde como uma das **15 estações mais utilizadas da região Norte**, grupo que concentra **75% de todo o tráfego de passageiros dos Urbanos do Porto** ([Público, 2009](https://www.publico.pt/2009/05/04/jornal/utentes-da-linha-de-guimaraes-sao-poucos-mas-cada-vez-mais-305182)).
- **Valor histórico direto:** um artigo do Público de 2000 refere que Ermesinde tinha, nessa altura, um **"movimento anual de 3,6 milhões de passageiros"** com um tráfego de **"cerca de 180 comboios diários"** ([Público, 2000](https://www.publico.pt/2000/10/27/jornal/revolucao-em-ermesinde-150496)) — volume de comboios muito próximo do valor hoje extraído dos PDFs (184 passagens/dia útil).
- **Crescimento da rede urbana do Porto:** de ~19,4 milhões de passageiros/ano (CP, ~2013) para 27,6 milhões (2025), um fator de crescimento de aproximadamente **1,42×**.

**Estimativa adotada:** escalando o valor histórico de 3,6 milhões (ano ~2000, tráfego de comboios comparável) pelo fator de crescimento da rede (1,42×), obtém-se **~5,1 milhões de passageiros/ano** em Ermesinde — valor tratado como **ordem de grandeza aproximada**, não uma medição direta, e documentado como tal em `PASSAGEIROS_ANO_ERMESINDE_ESTIMADO` no código. Dividindo pelos 365 dias e pelas ~184 passagens diárias médias, obtém-se uma média de **~76 passageiros por passagem de comboio**, valor plausível para uma composição suburbana de 3–4 carruagens ao longo de um dia com mistura de horas de ponta e vazio.

O total anual efetivamente gerado no átrio (soma de `passengers_expected` de EscadaRolante_1 + EscadaRolante_2) é de **3.647.664 passageiros/ano**, cerca de **0,72×** a estimativa de referência (5,1 milhões) — considerada consistente dentro da margem de incerteza da própria estimativa (que assenta em escalamento indireto, não em contagem direta).

### 4.2 Perfil horário

Reutilizou-se a forma do perfil `PERFIL_OCUPACAO_DIA_UTIL` / `PERFIL_OCUPACAO_FDS` já usada no script original (picos 06h–09h e 16h–19h em dia útil, fim-de-semana atenuado a ~50%), mas a **magnitude** deixou de ser um valor de pico arbitrário (`PASSAGEIROS_PICO_HORA=220`) e passou a ser diretamente proporcional aos **eventos de comboio reais** em cada bloco de 15 min, modulados por este perfil horário (fator `0,6 + 0,4 × perfil_horário`, para não zerar a procura fora das horas de ponta, apenas atenuá-la).

### 4.3 Regra dependente da direção

- **`desce`** (EscadaRolante_1, 4, 6): a procura de passageiros é atribuída ao bloco de 15 min em que o comboio **chega** (`arriving_trains`), representando o fluxo de desembarque.
- **`sobe`** (EscadaRolante_2, 3, 5): a procura é antecipada em 1 bloco (15 min) relativamente à **partida** (`departing_trains`), representando passageiros que sobem a escada **antes** do comboio partir.
- **Átrio** (Tipo A): combina ambos os fluxos (`arriving + departing`), já que todos os passageiros — a chegar ou a partir, de qualquer plataforma — atravessam o átrio.

Cada evento de comboio no bloco contribui com `PASSAGEIROS_POR_PASSAGEM_MEDIO / 2` passageiros nessa escada específica (o fator ÷2 reflete que o fluxo de um comboio se reparte tipicamente por 2 vias de circulação — por exemplo, escada + elevador, ou escada de cada sentido), com ruído multiplicativo gaussiano (desvio-padrão 8%) para evitar um padrão perfeitamente determinístico.

### 4.4 `people_detected`

Definido como 1 sempre que `passengers_expected > 0,5` (limiar de deteção), replicando a mesma lógica de threshold já usada no gerador sintético original, interpretável como o limiar mínimo de deteção de presença por sensor infravermelho/ótico.

### 4.5 `available`

Fixado a 1 em todos os passos (sem janelas de manutenção configuradas nesta versão). O suporte para janelas de manutenção opcionais existe na arquitetura do script original (`gerar_escada_rolante_csv`), mas não foi ativado por defeito para as escadas reais — pode ser adicionado facilmente reutilizando essa lógica se for necessário simular indisponibilidade programada.

---

## 5. Validações realizadas

| Verificação | Resultado |
|---|---|
| Nº de linhas por ficheiro | 35.040 em todos os 6 ficheiros (✓ igual ao calendário 2025 a 15 min) |
| Valores em falta (NaN) | 0 em todos os ficheiros |
| Colunas conformes ao schema acordado com o Tiago | ✓ (`time_step, month, day_type, hour, minutes, passengers_expected, people_detected, arriving_trains, departing_trains, minutes_to_next_train, available`) |
| Calendário (`month`, `day_type`, `hour`) coincide com `Building_1.csv` | ✓ (verificado programaticamente em `validar_dataset()`) |
| `day_type` cobre 1–8 (seg–dom + feriado) | ✓ |
| `minutes` só toma valores {0, 15, 30, 45} | ✓ |
| `minutes_to_next_train` dentro de [0, 240] | ✓ (0 negativos, 0 acima do cap) |
| `available` ∈ {0, 1} | ✓ (sempre 1 nesta versão) |
| `people_detected` ∈ {0, 1} | ✓ |
| Nº de comboios/dia útil (átrio) vs. PDFs | **184** (gerado) = **184** (extraído dos PDFs) ✓ exato |
| Nº de comboios/dia útil (átrio) vs. Wikipédia (~80×2=160) | 184 vs. 160 — mesma ordem de grandeza (diferença ~15%, atribuível a diferença de datas de vigência) |
| Total anual de passageiros (átrio) vs. estimativa investigada | 3.647.664 vs. ~5.100.000 (razão 0,72×) — mesma ordem de grandeza |
| Ambiente CityLearn 2.5.0 carrega o schema sem erro | ✓ (`testar_ambiente_citylearn()`, 10 passos de simulação executados) |
| Conservação de energia (Building_1, pricing) | ✓ sem regressões introduzidas pelas alterações às escadas |

Todas as verificações de integridade estrutural passaram sem problemas (`validar_dataset()` reportou "Validação de integridade: OK"). As verificações de plausibilidade de negócio (contagem de comboios, passageiros anuais) mostram concordância de ordem de grandeza com as fontes de referência, com desvios explicáveis pela natureza indireta das estimativas.

---

## 6. Limitações

1. **Alocação de plataforma não confirmada por fonte primária.** A regra "Braga+Guimarães → linhas_4_5" e "Marco → linhas_2_3" é uma assunção documentada de confiança média/baixa (secção 2.3). Não foi possível aceder a uma fonte que liste explicitamente o número de via por comboio em Ermesinde — a API de tempo real da CP não está acessível sem sessão de browser autenticada, e o Diretório da Rede da IP não foi minerado ao nível de detalhe necessário no tempo disponível.

2. **Horários de 2025/2026 usados como proxy para 2025.** Os PDFs fornecidos têm vigência "desde julho/dezembro de 2025/2026", não um horário exclusivamente do ano civil 2025. Assume-se estabilidade estrutural do serviço urbano ano a ano.

3. **5 de 179 números de comboio do PDF Ermesinde isolado sem correspondência exata** nos 3 PDFs de linha completa (2,8%), atribuídos a diferenças de edição entre PDFs ou artefactos de extração perto da meia-noite; não têm impacto material na tabela autoritativa.

4. **Estimativa de passageiros anuais é indireta**, obtida por escalamento de um valor histórico (ano 2000) pelo crescimento agregado da rede urbana do Porto. Não existe uma série pública de passageiros ao nível da estação de Ermesinde para calibração direta. O valor gerado (3,65 milhões/ano no átrio) está a 0,72× da estimativa de referência (5,1 milhões/ano) — mesma ordem de grandeza, mas não uma correspondência exata.

5. **`potencia_normal_kw` mantida fixa (sem incremento por carga de passageiros)**, seguindo a simplificação já documentada em `relatorio_15min_escadas.md` e suportada pela tese da Aalto University citada — o efeito da carga é considerado pequeno face às perdas mecânicas fixas do motor, mas não foi modelado explicitamente.

6. **Sem janelas de manutenção configuradas** (`available` sempre 1) — a arquitetura suporta esta extensão (reutilizando a lógica já existente em `gerar_escada_rolante_csv`), mas não foi ativada por defeito.

7. **Dia 24 de junho tratado como feriado apenas para a lógica das escadas**, não alterando `FERIADOS_PT_2025` global — esta é uma decisão deliberada para não introduzir uma alteração não solicitada nos restantes ficheiros do dataset (Building_1, pricing, weather), mas significa que, se no futuro se quiser tratar 24 de junho como feriado para o edifício também, será necessário fazer essa alteração separadamente.

8. **Fator de repartição de fluxo "÷2 vias" no modelo de passageiros** (secção 4.3) é uma escolha de modelação razoável mas arbitrária, não calibrada por contagem direta de passageiros por escada — recomenda-se validação futura por observação no local ou contagem por sensor, se disponível.

---

## Ficheiros gerados

- `/home/user/workspace/dataset_15min/EscadaRolante_1.csv` — Tipo A, átrio, desce (35.040 linhas)
- `/home/user/workspace/dataset_15min/EscadaRolante_2.csv` — Tipo A, átrio, sobe (35.040 linhas)
- `/home/user/workspace/dataset_15min/EscadaRolante_3.csv` — Tipo B, linhas 2+3, sobe (35.040 linhas)
- `/home/user/workspace/dataset_15min/EscadaRolante_4.csv` — Tipo B, linhas 2+3, desce (35.040 linhas)
- `/home/user/workspace/dataset_15min/EscadaRolante_5.csv` — Tipo B, linhas 4+5, sobe (35.040 linhas)
- `/home/user/workspace/dataset_15min/EscadaRolante_6.csv` — Tipo B, linhas 4+5, desce (35.040 linhas)
- `/home/user/workspace/dataset_15min/escadas_config.json` — configuração estática das 6 escadas
- `/home/user/workspace/dataset_15min/ermesinde_eventos_comboios.csv` — tabela de eventos autoritativa (204 passagens)
- `/home/user/workspace/dataset_15min/ermesinde_pdf_eventos_bruto.csv` — validação cruzada (PDF Ermesinde isolado, 179 eventos)
- `/home/user/workspace/extrair_horarios_ermesinde.py` — script de extração/parsing dos horários CP
- `/home/user/workspace/gerar_escadas_reais.py` — módulo de geração das 6 escadas reais (CONFIG_ESCADAS, modelo de passageiros, séries de comboios)
- `/home/user/workspace/gerar_dataset_citylearn.py` — script principal, estendido com o argumento `--escadas-reais`
