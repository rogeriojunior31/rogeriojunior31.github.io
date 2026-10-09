---
title: "SP Night"
date: 2026-08-02
summary: "Um tema escuro com São Paulo como referência: três variações, cores com contraste medido e ports gerados da mesma paleta para terminais, editores e CLIs."
showcase: "spnight"
tags: ["Tema", "Open Source", "Go", "Astro"]
---

{{< spnight >}}

Um esquema de cores escuro inspirado em São Paulo: o poste de sódio, o concreto aparente, o vão livre do MASP, a garoa antes da chuva. São três variações, todas escuras por decisão: `noite`, `garoa` e `jaragua`, três jeitos de olhar a mesma cidade.

O projeto é um contrato e uma ferramenta. O contrato é a paleta e uma camada de papéis que diz qual cor significa o quê. A ferramenta, `spn`, transforma o mapeamento de cada app em arquivos de tema prontos e se recusa a gerar quando a paleta não passa nos pisos de contraste.

- **Nenhum hex escolhido à mão:** temas, READMEs e previews saem da paleta, então não mostram uma cor que você não vai receber.
- **Contraste como portão:** cada par de cores é medido a cada build; comentário ilegível não passa.
- **Acentos separados entre si:** pares vizinhos precisam se distinguir pela luminosidade, não só pelo matiz.
- **Ports reproduzíveis:** a suíte renderiza os ports publicados e compara byte a byte com o que foi instalado.

Para usar um tema, escolha uma variação, copie o arquivo do port para o caminho do app e ative com uma linha. Os guias de cada port estão em [sp-night.github.io/ports](https://sp-night.github.io/ports/).

{{< button href="/docs/sp-night/" >}}Documentação{{< /button >}}
{{< button href="https://sp-night.github.io" target="_blank" >}}sp-night.github.io{{< /button >}}
{{< button href="https://github.com/sp-night/sp-night" target="_blank" >}}github.com/sp-night/sp-night{{< /button >}}

> Este site usa a variação Pico do Jaraguá.
