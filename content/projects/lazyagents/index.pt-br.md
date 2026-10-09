---
title: "lazyagents"
date: 2026-09-28
summary: "Uma TUI em Go para gerenciar, num lugar só, o que seus agentes de código com IA usam: skills, sessões, consumo, providers e hooks."
showcase: "lazyagents"
tags: ["CLI", "TUI", "Go", "IA", "Open Source"]
---

{{< lazyagents >}}

Cada agente de código guarda as próprias skills, sessões e configuração numa pasta diferente, num formato diferente. O lazyagents junta tudo num terminal só, no espírito do lazygit: uma biblioteca de skills que você liga por agente com uma tecla, o histórico de sessões de todos os agentes num lugar, e o consumo da assinatura sempre à vista.

**Funciona com:** Claude Code, Codex, Gemini CLI, OpenCode e Hermes Agent.

- **Skills:** instala de um repositório do GitHub, pasta ou zip, e ativa por agente com um symlink, sem copiar nada.
- **Sessões:** retoma qualquer conversa no próprio CLI e na pasta certa, lê o transcript e busca em todos os agentes.
- **Consumo:** limites da assinatura (janela de sessão e semanal) e tokens por dia, agente, projeto e modelo.
- **Providers e hooks:** perfis de endpoint e hooks aplicados na configuração de cada agente, com confirmação e backup antes de escrever.
- **Plugins:** qualquer executável vira uma aba e um comando novo, em qualquer linguagem.

```sh
go install github.com/rogeriojunior31/lazyagents@latest
```

Também há binários para Linux, macOS e Windows na página de releases.

{{< button href="/docs/lazyagents/" >}}Documentação{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/lazyagents" target="_blank" >}}github.com/rogeriojunior31/lazyagents{{< /button >}}

> A TUI usa a paleta do SP Night.
