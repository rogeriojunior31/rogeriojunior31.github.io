---
title: "SP Night"
date: 2026-08-02
summary: "A dark colour scheme with São Paulo as its reference: three flavours, contrast-checked colours and ports generated from one palette for terminals, editors and CLIs."
tags: ["Theme", "Open Source", "Go", "Astro"]
---

{{< spnight >}}

A dark colour scheme with São Paulo as its reference: the sodium street lamp, exposed concrete, the free span of the MASP, the drizzle before the rain. Three flavours, all dark by decision: `noite`, `garoa` and `jaragua`, three ways of looking at the same city.

The project is a contract and a tool. The contract is the palette and a role layer that says which colour means what. The tool, `spn`, turns each app's mapping into finished theme files and refuses to build when the palette falls below its contrast floors.

- **No hex picked by hand:** themes, READMEs and previews come from the palette, so they cannot show a colour you will not get.
- **Contrast is a gate:** every colour pair is measured on every build; an unreadable comment does not ship.
- **Accents kept apart:** neighbouring pairs must differ in lightness, not only in hue.
- **Reproducible ports:** the suite renders the published ports and compares them byte for byte with what was installed.

To use a theme, pick a flavour, copy the port's file to the app's config path and activate it with one line. Every port's guide is at [sp-night.github.io/ports](https://sp-night.github.io/ports/).

{{< button href="/en/docs/sp-night/" >}}Documentation{{< /button >}}
{{< button href="https://sp-night.github.io" target="_blank" >}}sp-night.github.io{{< /button >}}
{{< button href="https://github.com/sp-night/sp-night" target="_blank" >}}github.com/sp-night/sp-night{{< /button >}}

> This site uses the Pico do Jaraguá flavour.
