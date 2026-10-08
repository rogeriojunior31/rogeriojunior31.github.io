---
title: "Previsor de preço de imóveis"
date: 2024-02-04
summary: "Modelo de machine learning em Python para estimar preços de imóveis."
tags: ["Python", "Machine Learning"]
---

{{< github repo="rogeriojunior31/house_price_predictor" showThumbnail=false >}}

## O problema

Estimar valores de imóveis a partir de características do California Housing Dataset e entender como essas características se relacionam com o preço. É um projeto de estudo de machine learning, não uma ferramenta de avaliação imobiliária para uso comercial.

## Como funciona

- Python e scikit-learn para carregar os dados e separar treino e teste.
- Regressão linear como modelo inicial; Ridge, validação cruzada e `GridSearchCV` na versão ampliada.
- RMSE para avaliar as previsões no conjunto de teste.
- Matplotlib e Seaborn para visualizar características dos dados e comparar valores reais com previstos.

## Como executar

Com Python 3.9 ou superior (para as dependências fixadas no repositório), em um ambiente virtual:

```sh
git clone https://github.com/rogeriojunior31/house_price_predictor.git
cd house_price_predictor
python -m venv .venv
# Linux/macOS; no Windows, use .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

A execução apresenta o RMSE e gráficos de análise. O carregamento inicial do dataset pode precisar de acesso à internet. Os resultados dependem da execução; não há aqui uma métrica publicada que permita afirmar desempenho em dados de outros mercados.

[Ver código e instruções no GitHub](https://github.com/rogeriojunior31/house_price_predictor)
