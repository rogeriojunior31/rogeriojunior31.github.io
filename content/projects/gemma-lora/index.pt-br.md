---
title: "Fine-tuning do Gemma com LoRA"
date: 2024-04-26
summary: "Notebook de fine-tuning de modelos Gemma no Keras usando LoRA."
tags: ["LLM", "Keras", "LoRA"]
---

{{< github repo="rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA" showThumbnail=false >}}

## O objetivo

Explorar a adaptação do Gemma 2B a instruções usando Keras e LoRA, sem treinar todos os parâmetros do modelo. O notebook usa o dataset Databricks Dolly 15k e o backend JAX.

## O experimento

- Carregamento e preparação dos exemplos de instrução.
- Geração de respostas antes do ajuste para comparação.
- LoRA com rank 4, sequências de até 512 tokens e uma época de treinamento.
- Nova geração com os mesmos prompts após o ajuste.

Essa comparação é qualitativa: o projeto não apresenta um benchmark que comprove melhoria geral do modelo.

## Como explorar

Abra o [notebook no GitHub](https://github.com/rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA/blob/main/Fine_tune_Gemma_model_with_Keras_using_LoRA.ipynb) para ler o fluxo completo. Para executar, siga as células de instalação e configuração do Kaggle em um ambiente com os recursos necessários para carregar e treinar o modelo, preferencialmente com GPU.

O acesso ao Gemma exige a configuração de credenciais e os termos do modelo. Não publique seu `kaggle.json` nem tokens. Como o notebook é um experimento de 2024, confira a compatibilidade das dependências antes de executar em um ambiente atual.

[Ver repositório e instruções](https://github.com/rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA)
