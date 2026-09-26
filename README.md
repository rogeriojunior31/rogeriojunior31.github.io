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
O terminal da home é o shortcode `terminal` (em `content/_index.*.md`); os links do `ls` ficam em `data/links.yaml`. A página Sobre (`content/about/`) usa os shortcodes `fastfetch` e `units` (systemctl). As animações ficam em `layouts/partials/extend-footer.html`. O currículo vem de `data/experience.yaml` (experiência) e `data/stack.yaml` (stack).
As cores são o SP Night, flavor **Pico do Jaraguá** (`assets/css/schemes/sp-night.css`), com os valores oficiais de `sp-night/palette/sp_night.json`; o realce de código segue `roles.json` (em `assets/css/custom.css`).

Atualizar o tema: `hugo mod get -u && hugo mod tidy`.

## Deploy

Push na `main` → GitHub Actions (`.github/workflows/hugo.yml`) → GitHub Pages.
Em Settings → Pages, a Source deve ser **GitHub Actions**.
