---
title: "Fine-tuning Gemma with LoRA"
date: 2024-04-26
summary: "Notebook fine-tuning Gemma models in Keras using LoRA."
tags: ["LLM", "Keras", "LoRA"]
---

{{< github repo="rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA" showThumbnail=false >}}

## The goal

Explore instruction tuning of Gemma 2B with Keras and LoRA without training every model parameter. The notebook uses Databricks Dolly 15k and the JAX backend.

## The experiment

- Load and prepare instruction examples.
- Generate responses before tuning for comparison.
- Train for one epoch with LoRA rank 4 and sequences up to 512 tokens.
- Generate responses to the same prompts after tuning.

This is a qualitative comparison, not a benchmark establishing a general improvement in model quality.

## Explore it

Open the [notebook on GitHub](https://github.com/rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA/blob/main/Fine_tune_Gemma_model_with_Keras_using_LoRA.ipynb) to read the full workflow. To run it, follow its installation and Kaggle configuration cells in an environment with enough resources to load and train the model, preferably with a GPU.

Gemma access requires credentials and the model's terms. Do not publish your `kaggle.json` or tokens. This is a 2024 experiment; check dependency compatibility before running it in a current environment.

[View repository and instructions](https://github.com/rogeriojunior31/Fine-tune-Gemma-models-in-Keras-using-LoRA)
