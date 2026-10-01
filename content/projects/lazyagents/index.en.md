---
title: "lazyagents"
date: 2026-09-28
summary: "A Go TUI to manage, in one place, what your AI coding agents use: skills, sessions, usage, providers and hooks."
tags: ["CLI", "TUI", "Go", "AI", "Open Source"]
---

{{< github repo="rogeriojunior31/lazyagents" showThumbnail=false >}}

Every AI coding agent keeps its skills, sessions and settings in its own folder, in its own format. lazyagents brings them into one terminal, in the spirit of lazygit: one skill library you enable per agent with a keypress, every agent's session history in one place, and your subscription usage always in sight.

**Works with:** Claude Code, Codex, Gemini CLI, OpenCode and Hermes Agent.

- **Skills:** install from a GitHub repository, a folder or a zip, and enable per agent with a symlink, nothing copied.
- **Sessions:** resume any conversation in its own CLI and folder, read the transcript, search across every agent.
- **Usage:** subscription limits (session and weekly windows) and tokens by day, agent, project and model.
- **Providers and hooks:** endpoint profiles and hooks applied to each agent's config, confirmed and backed up before writing.
- **Plugins:** any executable becomes a new tab and command, in any language.

```sh
go install github.com/rogeriojunior31/lazyagents@latest
```

Binaries for Linux, macOS and Windows are on the releases page too.

{{< button href="/en/docs/lazyagents/" >}}Documentation{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/lazyagents" target="_blank" >}}github.com/rogeriojunior31/lazyagents{{< /button >}}

> The TUI uses the SP Night palette.
