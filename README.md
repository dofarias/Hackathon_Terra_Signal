# Hackathon_Terra_Signal
Materiais da empresa Terra Signal para o Hackathon da Databricks!

> **🚀 Começando? Leia primeiro o [SETUP.md](SETUP.md)**
> para criar o workspace, fazer o fork, conectar o Git, adicionar a equipe, rodar o
> notebook e entregar.

Aquivos importantes:
- SETUP.md: Guia passo-a-passo de configuração inicial
- NOTEBOOK.ipynb: Notebook inicial, com código de exemplo para carregar dataset, treinar modelo placeholder, e exportar prediction.csv
- history.csv: Dados históricos, devem ser usados para treinamento do modelo. A coluna que deve ser predita é a coluna "Churn"
- inference.csv: Arquivo com dados novos, sem coluna "Churn". Seu objetivo é gerar a previsão para cada linha desse arquivo, e salvar esse resultado em um arquivo .csv, como exemplificado em [NOTEBOOK.ipynb](NOTEBOOK.ipynb)

> ⚠️ **Free Edition tem crédito limitado.** Não deixe Apps/endpoints ligados sem uso
> e não rode tarefas pesadas (o dataset é pequeno). Detalhes no [SETUP.md](SETUP.md).

---

## Equipe

> Preencha antes de começar (edite este bloco no seu fork), depois faça commit + push.

- **Nome/ID da equipe:** `Grupo 6`
- **Integrantes:**
  - `Aleônia Oliveira — aleonia.oliveira@gmail.com`
  - `Daniele Farias — dofarias@gmail.com`
  - `Marcelo Caroprezo — marcelo.caroprezo2@gmail.com`
  - `Patrícia Nascimento — pathilink@gmail.com`

---

## 📋 Sobre o Projeto

Predição de **churn** (cancelamento) de clientes de telecomunicações. O modelo é treinado com os dados históricos de [history.csv](history.csv) (coluna alvo: `Churn`) e gera previsões para cada linha de [inference.csv](inference.csv), exportadas em um arquivo `.csv` no padrão exemplificado em [NOTEBOOK.ipynb](NOTEBOOK).

## 📁 Estrutura do Repositório

```text
Hackathon_Terra_Signal/
├── SETUP.md                        # Guia de configuração inicial
├── NOTEBOOK.ipynb                  # Notebook inicial de exemplo
├── history.csv                     # Dados históricos (treinamento, alvo: Churn)
├── inference.csv                   # Dados novos para previsão
├── LICENSE                         # Licença do projeto
├── assets/                         # GIFs do guia de setup
├── Analise Exploratoria/           # Notebooks de EDA
├── ABT/                            # Construção da base analítica (exercício replicado no notebook de Treino)
├── Treino/                         # Treinamento e seleção do modelo, além de avaliação de modelos intermediários
├── Inferencia/                     # Inferência e ações recomendadas
├── apps/churn-prediction-acoes-app # App para informar os dados do Clientes e retornar a probabilidade de Churn e recomendação de ações
└── Apresentacao/                   # Apresentação e vídeo de demonstração do App
```

## 🛠️ Tecnologias Utilizadas

- **Databricks** — notebooks, compute serverless e Unity Catalog
- **SQL / PySpark** — preparação e transformação dos dados
- **XGBoost + MLflow** — treinamento, rastreamento e registro do modelo no Unity Catalog
- **Databricks Apps / Model Serving** — demonstração e consumo do modelo

## ✅ Pré-requisitos

- Conta e workspace Databricks (ver instruções no [SETUP.md](SETUP.md))
- Fork deste repositório conectado a um Git folder do workspace
- Permissões de acesso aos dados e compute da equipe

## 📄 Licença

Distribuído sob a licença descrita em [LICENSE](LICENSE).