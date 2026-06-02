# CityLearn Ermesinde

Projeto de estudo e desenvolvimento com base no CityLearn para modelação, simulação e avaliação da viabilidade de uma comunidade de energia renovável na estação de comboios de Ermesinde.

## Objetivo

Este repositório reúne:
- testes e scripts de exploração do CityLearn;
- experiências com diferentes controladores e abordagens RL;
- geração e inspeção de parâmetros/datasets;
- trabalho aplicado ao caso de estudo de Ermesinde.

## Estrutura

```text
CityLearn/
├── .citylearn-env/         # ambiente virtual local (não versionado)
├── tests/                  # scripts de teste e experiências
│   ├── baseline.py     # No control agent
│   ├── central_rbc.py # Centralized Rule Based Control
│   ├── check_all_params.py # Tentativa comparação datasets
│   ├── inspect_params.py # Tentativa leitura datasets
│   ├── decentral_marlisa.py # Decentralized MARLISA (Multi-Agent Reinforcement Learning with Iterative Sequential Action)
│   ├── decentral_sac.py # Decentralized Soft-Actor Critic
│   ├── multiagent_rllib.py # Multiagent Reinforcement Learning Lib
│   ├── singleagent_rllib.py # Singleagent Reinforcement Learning Lib
│   └── stable_baseline_rla.py # Static Baseline Reinforcement Learning Agent
└── README.md
```

## Instalação

Instalar o CityLearn via pip:
```powershell
pip install CityLearn
```

Se necessário, instalar dependências adicionais usadas nos testes:
```powershell
pip install -r requirements.txt
```

## Notas

- Este repositório é o workspace local de desenvolvimento e experimentação.
- A interface gráfica/visualização está num projeto separado: `citylearn_UI/citylearn-ui`.
- O motor oficial do CityLearn encontra-se no repositório upstream do projeto CityLearn.

<!-- ## Próximos passos

- organizar dependências em `requirements.txt`;
- separar testes exploratórios de scripts finais;
- adicionar datasets e schemas próprios do caso Ermesinde;
- documentar pipeline completo de simulação. -->

## A minha perceção de organização dos datasets

https://www.citylearn.net/overview/dataset.html 

Os datasets são um conjunto de *ficheiros de dados* que constituem x Buildings, mediante o estudo pretendido para a simulação.
Existem 
