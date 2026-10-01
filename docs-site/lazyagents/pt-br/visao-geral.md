---
weight: 1
---
# Visão geral

Cada agente de código guarda as próprias skills, sessões e configuração numa pasta diferente, num formato diferente. O lazyagents junta tudo num terminal só, no espírito do lazygit.

**Funciona com:** Claude Code, Codex, Gemini CLI, OpenCode e Hermes Agent.

| Aba | Para que serve |
|---|---|
| Skills | Instala de um repositório do GitHub, pasta ou zip, e ativa por agente com um symlink, sem copiar nada |
| Sessões | Retoma qualquer conversa no próprio CLI e na pasta certa, lê o transcript e busca em todos os agentes |
| Consumo | Limites da assinatura (janela de sessão e semanal) e tokens por dia, agente, projeto e modelo |
| Providers e hooks | Perfis de endpoint e hooks aplicados na configuração de cada agente, com confirmação e backup antes de escrever |
| Plugins | Qualquer executável vira uma aba e um comando novo, em qualquer linguagem |

## Instalar

```sh
go install github.com/rogeriojunior31/lazyagents@latest
```

Também há binários para Linux, macOS e Windows na [página de releases](https://github.com/rogeriojunior31/lazyagents/releases). O passo a passo completo está em [Primeiros passos](getting-started.md).
