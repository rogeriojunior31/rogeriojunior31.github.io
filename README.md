# rogeriojunior31.github.io

Site pessoal feito com [Hugo](https://gohugo.io) e o tema [Blowfish](https://blowfish.page) (importado como Hugo Module). Bilíngue: PT-BR (padrão) e EN (`/en/`).

## Rodar localmente

```sh
mise install          # instala o hugo-extended fixado em mise.toml (requer Go para os módulos)
hugo server -D        # http://localhost:1313
```

## Conteúdo

```sh
hugo new content posts/meu-post/index.pt-br.md
hugo new content projects/meu-projeto/index.pt-br.md   # usa archetypes/projects.md
```

Para a versão em inglês, crie o `index.en.md` ao lado. Coloque um `feature.jpg` na pasta do post/projeto para aparecer como capa.
A página Sobre (`content/about/`) usa os shortcodes `fastfetch` e `units` (systemctl). As animações ficam em `layouts/partials/extend-footer.html`. O currículo vem de `data/experience.yaml` (experiência) e `data/stack.yaml` (stack).
As cores são o SP Night, flavor **Pico do Jaraguá** (`assets/css/schemes/sp-night.css`), com os valores oficiais de `sp-night/palette/sp_night.json`; o realce de código segue `roles.json` (em `assets/css/custom.css`).

Atualizar o tema: `hugo mod get -u && hugo mod tidy`.

## CI/CD

| Workflow | Quando | O que faz |
|---|---|---|
| `build.yml` | reutilizável | instala Hugo e Go pelo `mise.toml`, build com `--panicOnWarning` e checa links internos (lychee) |
| `ci.yml` | todo PR | roda o build |
| `deploy.yml` | push na `main` | roda o build e publica no GitHub Pages |

O Dependabot (`.github/dependabot.yml`) abre PRs semanais para as actions e para o tema Blowfish.
As versões de Hugo e Go ficam só no `mise.toml`, usado localmente e no CI.

No GitHub, em Settings → Pages, a Source deve ser **GitHub Actions**.
