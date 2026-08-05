# Notas de Revisão v2 — Resposta aos 4 pontos levantados

**Data:** 5 de agosto de 2026
**Âmbito:** Resposta às notas de revisão sobre `relatorio_escadas_ermesinde.md` (30 jul 2026), antes da integração no simulador.

Todos os pontos foram verificados diretamente nos dados (não apenas no texto do relatório). Ficheiros corrigidos anexados: `EscadaRolante_1.csv` a `EscadaRolante_6.csv` e `ermesinde_eventos_comboios.csv`.

---

## 1. Direção das escadas do átrio — CONFIRMADO E CORRIGIDO

A suspeita estava certa. Reconstrui o layout físico implícito na configuração:

```
átrio (piso superior)  --[Escada 1, desce]-->  piso inferior  --[Escada 3/5, sobe]--> plataforma
plataforma  --[Escada 4/6, desce]-->  piso inferior  --[Escada 2, sobe]-->  átrio (piso superior)
```

Ou seja, o piso inferior funciona como um **passadiço/túnel intermédio** entre o átrio e as plataformas (2 lanços em série, tal como descrito no ponto 4). Isso significa:

- Um passageiro **a partir** percorre: átrio → Escada 1 (desce) → piso inferior → Escada 3/5 (sobe) → plataforma. Todo este percurso acontece **antes** da partida do comboio.
- Um passageiro **a chegar** percorre: plataforma → Escada 4/6 (desce) → piso inferior → Escada 2 (sobe) → átrio. Todo este percurso acontece **no momento/depois** da chegada.

O código aplicou a mesma regra ("desce" = chegada no bloco atual, "sobe" = partida antecipada 1 bloco) a **todas** as 6 escadas. Essa regra está certa para as escadas Tipo B (3,4,5,6) — confirmei isto isolando 64 blocos com um único comboio e sem vizinhos próximos: a procura de Escada 3/5 aparece 1 bloco *antes* do evento, a de Escada 4/6 aparece *no* bloco do evento. Mas para o Tipo A a regra está **trocada**, porque a convenção "desce/sobe" do átrio tem o sentido oposto (entrar vs. sair da estação) ao das plataformas (ir para vs. vir de comboio).

**Correção aplicada:** troquei as séries de passageiros entre `EscadaRolante_1.csv` e `EscadaRolante_2.csv` (a série que antes estava em 2 passou para 1, e vice-versa). Verifiquei o resultado com o mesmo teste de blocos isolados — agora a Escada 1 (desce) tem procura no bloco *anterior* ao comboio e a Escada 2 (sobe) tem procura *no* bloco do comboio, como esperado.

Escadas 3, 4, 5 e 6 **não foram alteradas** neste ponto — já estavam corretas.

---

## 2. Fluxo pedonal de fundo no átrio — ADICIONADO (sintético, documentado)

Separei, só para as escadas do átrio (1 e 2), em 3 colunas:

```
passengers_from_trains_15min   — igual ao antigo passengers_expected (após correção do ponto 1)
background_pedestrians_15min   — novo, sintético
passengers_expected_15min      — soma das duas (substitui a antiga passengers_expected)
```

Por consistência de schema entre os 6 ficheiros, as escadas Tipo B (3–6) também passaram a ter as 3 colunas, mas com `background_pedestrians_15min = 0` (fazem sentido apenas como escadas de plataforma, não como atalho urbano).

**Modelo sintético usado** (claramente não calibrado com dados reais, a rever se surgirem contagens):
- Perfil horário próprio (mais achatado que o perfil ligado a comboios — gente a atravessar a estação não está tão concentrada nas horas de ponta): praticamente zero durante o encerramento (~01h10–05h00), sobe ao longo do dia com dois reforços ligeiros (manhã e final da tarde).
- Fator por tipo de dia: dia útil = 1,0 · sábado = 0,75 · domingo/feriado = 0,55 (mesma lógica de atenuação já usada no modelo de comboios).
- Pico de referência: 50 passageiros/15min (~200/h) em hora de ponta de dia útil; ruído gaussiano multiplicativo de 15%.
- Parâmetro `BG_PEAK` isolado no código — fácil de recalibrar depois.

**Resultado:** ~718.600 passageiros/ano em cada escada do átrio (~1,44M combinados). Total anual do átrio passa de 3.647.664 → **5.085.491**, muito próximo da estimativa de referência de ~5,1M passageiros/ano mencionada na secção 4.1 do relatório original (a estimativa que antes ficava a 0,72× passa a ficar a ~1,0×). Isto é uma coincidência interessante, não uma calibração deliberada — mas reforça que a ordem de grandeza escolhida para o fluxo de fundo é plausível.

---

## 3. Eventos duplicados de Guimarães — CONFIRMADO E CORRIGIDO (parcialmente)

Confirmei exatamente o que descreveste. Os 4 números (15167, 15169, 15171, 15173) aparecem cada um **duas vezes** na tabela — uma vez como evento `minho_braga` (`SB_para_Braga`) e outra como `minho_guimaraes` (`Guimaraes_para_SB`), com o mesmo número, hora e grupo de plataforma. É o mesmo comboio físico, apanhado pelos dois PDFs (tronco partilhado Porto–Ermesinde/Trofa) — exatamente o padrão descrito na secção 1.2 do relatório para os outros 36 casos —, mas escapou à deduplicação porque os campos `sentido_fisico` ficaram contraditórios (um diz "a partir de SB", o outro diz "a chegar a SB" — fisicamente impossível para o mesmo comboio à mesma hora).

Também confirmei um problema mais amplo: **os 25 eventos `minho_guimaraes` têm todos, sem exceção, `sentido_fisico = "Guimaraes_para_SB"`** — zero casos do sentido oposto. Isso não é plausível para um serviço bidirecional (Braga e Marco têm uma divisão quase 50/50 entre sentidos). Isto sugere que a extração do PDF de Guimarães atribuiu sempre a mesma direção por omissão, independentemente do sentido real de cada comboio.

**Correção aplicada:**
- Removi a linha `minho_guimaraes` duplicada de cada um dos 4 pares (mantendo 1 evento em vez de 2) → **204 → 200 eventos autoritativos**.
- Corrigi a linha/sentido do evento mantido para `linha=minho_guimaraes`, `sentido_fisico=SB_para_Guimaraes`, com base na tua confirmação do horário real da CP para o 15167 (16:39, SB→Guimarães). Assumi o mesmo padrão para os outros 3 (17:39, 18:44, 19:27) por analogia — **isto não está confirmado individualmente por ti nem por mim**, é a hipótese mais plausível mas fica marcado como assunção.
- Propaguei a correção às escadas 5 e 6 (linhas_4_5): nos blocos de 15 min afetados, `arriving_trains`/`departing_trains` estavam inflacionados em +1 (o comboio duplicado contava a dobrar). Corrigi as contagens e reduzi proporcionalmente `passengers_from_trains_15min` nesses blocos específicos (365 dias/ano para os 2 eventos "diário", ~250 dias/ano para os 2 "seg-sex"). Efeito no total anual: Escada 5 passou de 1.081.162 → 1.041.465 passageiros/ano; Escada 6 de 1.077.516 → 1.037.994. É um efeito pequeno (~3,7%) mas real.

**O que NÃO ficou resolvido:** não tenho os textos extraídos dos PDFs originais (`pdf_extract/*.txt`) neste projeto, por isso não consigo re-derivar o sentido físico correto para os outros 21 eventos `minho_guimaraes` que não fazem parte de nenhum par duplicado. Como esses eventos são todos do tipo "passagem" (contam para chegada e partida em simultâneo, independentemente do `sentido_fisico`), este problema **não afeta os números de energia/procura** gerados — é uma questão de qualidade de metadados, não de simulação. Recomendo reprocessar o PDF de Guimarães isolado para confirmar as direções reais, se isso for necessário para outro fim (ex. relatórios operacionais).

---

## 4. Potência das escadas Tipo B — RESPOSTA: os 1,31 kW são por LANÇO FÍSICO, não pelo conjunto

Encontrei a resposta na própria folha `Escadas_Rolantes` do `EC_Ermesinde_CityLearn_Dataset.xlsx`, que não tinha sido cruzada com esta questão antes:

| | Tipo A | Tipo B |
|---|---|---|
| N.º de escadas rolantes (físicas) | **2** | **8** |
| Pot. p/unidade — carga plena | 2100 W | **1310 W** |
| Pot. total — carga plena | 4200 W (= 2100×2) | **10480 W (= 1310×8)** |

A folha confirma exatamente a tua descrição: há **8 lanços físicos** de Tipo B, agrupados nos **4 ficheiros CSV** (`EscadaRolante_3` a `_6`), cada um representando **2 lanços em série**. O valor "Pot p/unidade" de 1310 W é explicitamente por **uma unidade física** das 8 — a própria folha faz a conta `1310 × 8 = 10480` para chegar ao total da estação, o que só bate certo se 1310 W for o valor de um único lanço.

Também procurei a documentação pública da Schindler 9300 (citada como fonte na secção 3.3 do relatório): os fabricantes cotam sempre a potência **por máquina/motor individual**; quando a Schindler dá um valor "para um par sobe+desce" fá-lo explicitamente à parte, nunca como default. Isto reforça a mesma conclusão.

**Implicação prática:** o `gerar_escadas_reais.py` usou `potencia_normal_kw = 1,310 kW` e `potencia_lenta_kw = 0,260 kW` diretamente como a potência de **cada ficheiro CSV** (ou seja, de cada par de lanços), quando deveria ser o **dobro**, porque os dois lanços em série têm de estar ligados em simultâneo sempre que alguém percorre esse caminho — não há forma de um passageiro usar só metade do trajeto. Isto subestima a potência (e portanto a energia) das 4 escadas Tipo B em ~2×.

**Valores corrigidos recomendados** (para `escadas_config.json`, que não está entre os ficheiros deste projeto — não pude editá-lo diretamente):

| Parâmetro | Tipo B atual | Tipo B corrigido | Confiança |
|---|---|---|---|
| `potencia_normal_kw` | 1,310 | **2,620** | Alta — confirmado pela folha "N.º escadas rolantes: 8" |
| `potencia_lenta_kw` | 0,260 | **0,520** | Alta — mesma fonte/lógica |
| `potencia_desligado_kw` | 0,05 | 0,05 ou 0,10 (?) | Baixa — este valor nunca esteve na folha, foi uma recomendação à parte (ACEEE); pode fazer sentido manter 0,05 se representar só a eletrónica de um controlador partilhado, ou subir para 0,10 se cada lanço tiver controlo próprio |

Isto **não é um erro nos ficheiros CSV** que te enviei (eles não guardam potências, só séries de procura/comboios) — é um parâmetro do ficheiro de configuração estática que gera as leituras de energia a partir das ações do agente. Recomendo corrigir isso antes de correr qualquer comparação de controladores, porque duplica a energia associável às 4 escadas de plataforma e muda de forma material a poupança calculada entre "sempre ligado" e os outros controladores.

Tipo A não tem este problema — 2 escadas físicas, 2 ficheiros CSV, correspondência 1:1.

---

## Resumo do que mudou nos ficheiros

| Ficheiro | Alterações |
|---|---|
| `ermesinde_eventos_comboios.csv` | 204 → 200 eventos; 4 duplicados Guimarães/Braga removidos; direção do comboio 15167 corrigida (e por analogia 15169/15171/15173, não confirmado individualmente) |
| `EscadaRolante_1.csv` | Série de passageiros trocada com a Escada 2 (ponto 1); +fluxo de fundo; novo schema 3 colunas |
| `EscadaRolante_2.csv` | Série de passageiros trocada com a Escada 1 (ponto 1); +fluxo de fundo; novo schema 3 colunas |
| `EscadaRolante_3.csv` | Só schema (3 colunas, fundo=0) — sem alteração de valores |
| `EscadaRolante_4.csv` | Só schema (3 colunas, fundo=0) — sem alteração de valores |
| `EscadaRolante_5.csv` | Contagens de comboios corrigidas nos 4 blocos duplicados (ponto 3); schema 3 colunas |
| `EscadaRolante_6.csv` | Contagens de comboios corrigidas nos 4 blocos duplicados (ponto 3); schema 3 colunas |
| `escadas_config.json` | **Não alterado** (não está neste projeto) — ver recomendação do ponto 4 acima |

Validações repetidas em todos os 6 ficheiros: 35.040 linhas, 0 NaN, `minutes` ∈ {0,15,30,45}, `available` e `people_detected` ∈ {0,1}, `arriving_trains == departing_trains` linha a linha (mantém-se, como no original).

## Pontos em aberto para ti

1. Confirmar (ou desconfirmar) o sentido real dos comboios 15169, 15171 e 15173 — assumi o mesmo padrão do 15167 por analogia.
2. Decidir se aplicas a correção de potência do ponto 4 ao `escadas_config.json` (recomendo que sim, com confiança alta para plena/lenta).
3. O fluxo de fundo do ponto 2 é sintético — se houver forma de obter uma contagem real, mesmo aproximada (ex. observação no local em algumas horas), o parâmetro `BG_PEAK` pode ser recalibrado rapidamente.
