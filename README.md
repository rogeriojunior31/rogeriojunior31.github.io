# rogeriojunior31.github.io

Personal site built with [Hugo](https://gohugo.io) and [Blowfish](https://blowfish.page), themed with [SP Night](https://sp-night.github.io) (Pico do Jaraguá). Available in Portuguese (default) and English (`/en/`).

## Run locally

```sh
mise install     # Hugo and Go, versions pinned in mise.toml
hugo server -D   # http://localhost:1313
```

## Content

| What | Where |
|---|---|
| Pages | `content/` (`index.pt-br.md` + `index.en.md`) |
| Projects | `content/projects/<name>/` (`feature.png` becomes the card cover) |
| Resume | `data/experience.yaml`, `data/stack.yaml` |
| Menus | `config/_default/menus.*.toml` |

New project: `hugo new content projects/<name>/index.pt-br.md`.
Posts are hidden until the first one exists: add `posts` back to the menus.

## Theme

- Colors: `assets/css/schemes/sp-night.css`, taken from the official SP Night palette
- Styles and syntax highlighting: `assets/css/custom.css`
- Terminal shortcodes (`fastfetch`, `units`, `experience`, `stack`): `layouts/shortcodes/`
- Animations and tmux bar: `layouts/partials/extend-footer.html`

Update Blowfish: `hugo mod get -u && hugo mod tidy`.

## CI/CD

- `ci.yml`: builds every pull request
- `deploy.yml`: deploys to GitHub Pages on push to `main`
- `build.yml`: shared build (`--panicOnWarning` plus an internal link check)
- Dependabot keeps the actions and Blowfish up to date

Requires Settings → Pages → Source set to **GitHub Actions**.
