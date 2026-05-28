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
├── .venv/                  # ambiente virtual local (não versionado)
├── tests/                  # scripts de teste e experimentação
│   ├── baseline.py
│   ├── central_rbc.py
│   ├── check_all_params.py
│   ├── inspect_params.py
│   ├── decentral_marlisa.py
│   ├── decentral_sac.py
│   ├── multiagent_rllib.py
│   ├── singleagent_rllib.py
│   └── stable_baseline_rla.py
└── README.md
```

## Ambiente

### Criar ambiente virtual
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Desativar ambiente virtual
```powershell
deactivate
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

## Utilização

Exemplos:
```powershell
python .\tests\check_all_params.py
python .\tests\inspect_params.py
python .\tests\baseline.py
```

## Notas

- Este repositório é o workspace local de desenvolvimento e experimentação.
- A interface gráfica/visualização está num projeto separado: `citylearn_UI/citylearn-ui`.
- O motor oficial do CityLearn encontra-se no repositório upstream do projeto CityLearn.

## Próximos passos

- organizar dependências em `requirements.txt`;
- separar testes exploratórios de scripts finais;
- adicionar datasets e schemas próprios do caso Ermesinde;
- documentar pipeline completo de simulação.