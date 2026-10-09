---
title: "Vults"
date: 2026-10-05
summary: "Um app de desktop em Rust e Tauri para quem roda vários agentes de código ao mesmo tempo: cada sessão é um urubu 8-bit no topo da tela, com aprovações, chat e um companheiro chamado Zeca."
showcase: "vults"
tags: ["Desktop", "Rust", "Tauri", "IA", "Open Source"]
---

{{< vults >}}

Quem roda vários agentes de código ao mesmo tempo perde a conta: um terminou, outro falhou, outro está há dez minutos esperando uma permissão num terminal que você não acha. O Vults coloca todos no seu desktop. Cada sessão do Claude Code, Codex, Gemini CLI ou Antigravity vira um vult, um urubu 8-bit numa ilha no topo da tela, fazendo o que a sessão está fazendo.

**Funciona com:** Claude Code, Codex, Gemini CLI e Antigravity, no Linux (primeiro KDE Plasma e outros compositores com layer-shell).

- **Aprovações num lugar só:** o card mostra o comando, o arquivo ou o diff inteiro; Permitir, Negar ou um atalho global. Nada é aprovado sem o seu clique.
- **Diffs ao vivo e pulo para o terminal:** cada edição mostra as linhas adicionadas e removidas, e um clique foca o painel do tmux, kitty, wezterm ou herdr da sessão.
- **Novidades do GitHub e consumo do plano:** checks com falha, reviews e os limites do Claude e do Codex, pelos CLIs que você já usa.
- **Zeca, o companheiro:** um urubu-de-cabeça-preta que conversa pelo CLI `claude` ou `codex`, escuta quando você segura uma tecla e fala (whisper.cpp, no seu computador) e recebe os arquivos que você solta nele. Um botão desliga ele.
- **Seguro por padrão:** o hook nunca trava o agente, a configuração dos agentes só muda depois de um backup e de um diff que você aprova, segredos ficam no chaveiro do sistema, sem telemetria.

Baixe o `.deb` ou o `.rpm` da última release, ou gere o pacote do Arch com `makepkg`.

{{< button href="/docs/vults/" >}}Documentação{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/Vults/releases/latest" target="_blank" >}}Baixar{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/Vults" target="_blank" >}}github.com/rogeriojunior31/Vults{{< /button >}}
