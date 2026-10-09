---
title: "Vults"
date: 2026-10-05
summary: "A Rust and Tauri desktop app for people who run several coding agents at once: every session is an 8-bit vulture at the top of the screen, with approvals, chat and a companion named Zeca."
showcase: "vults"
tags: ["Desktop", "Rust", "Tauri", "AI", "Open Source"]
---

{{< vults >}}

Running several coding agents at once means losing track of them: one finished, one failed, one has been waiting for a permission for ten minutes in a terminal you cannot find. Vults puts them on your desktop. Every Claude Code, Codex, Gemini CLI or Antigravity session becomes a vult, an 8-bit vulture on an island at the top of the screen, doing what its session does.

**Works with:** Claude Code, Codex, Gemini CLI and Antigravity, on Linux (KDE Plasma and other layer-shell compositors first).

- **Approvals in one place:** the card shows the whole command, file or diff; Allow, Deny or a global shortcut. Nothing is approved without your click.
- **Live diffs and jump to the terminal:** each edit shows its lines added and removed, and one click focuses the session's tmux, kitty, wezterm or herdr pane.
- **News from GitHub and plan usage:** failed checks, reviews and your Claude and Codex limits, through the CLIs you already use.
- **Zeca, the companion:** a black vulture who chats through the `claude` or `codex` CLI, listens when you hold a key and speak (whisper.cpp, on your computer) and takes the files you drop on him. One switch turns him off.
- **Safe by design:** the hook never blocks your agent, agent configs change only after a backup and a diff you approve, secrets live in the OS keyring, no telemetry.

Download the `.deb` or `.rpm` from the latest release, or build the Arch package with `makepkg`.

{{< button href="/en/docs/vults/" >}}Documentation{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/Vults/releases/latest" target="_blank" >}}Download{{< /button >}}
{{< button href="https://github.com/rogeriojunior31/Vults" target="_blank" >}}github.com/rogeriojunior31/Vults{{< /button >}}
