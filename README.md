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

## Docs

`/docs/` lists project documentation. It publishes Markdown from each repository's `docs/` folder via Hugo Modules, or links to an existing documentation website.

| What | Where |
|---|---|
| Registered projects | `data/docs.yaml` (slug, repo, branch, summary per language) |
| Import of each repo's `docs/` | `config/_default/module.toml` (mount `docs` → `assets/docs/<slug>`) |
| Page generation | `content/docs/_content.gotmpl` (content adapter) |
| Site layer: translations and site-only pages | `docs-site/<slug>/<lang>/` |
| Layout, sidebar, hub | `layouts/docs/`, `layouts/partials/docs/` |
| Links and images written for GitHub | `layouts/docs/_markup/render-link.html`, `render-image.html` |

For an existing docs website (MkDocs, Docusaurus, etc.), add an entry to `data/docs.yaml` with an absolute HTTPS `url`. No module import or generated local pages are needed. `repo` is optional for external entries, and the English summary is used when the visitor's language has no summary:

```yaml
- slug: my-project
  name: My project
  url: https://example.org/docs/
  summary:
    pt-br: "Documentação do projeto."
    en: "Project documentation."
```

Imported projects require `docs/README.md`; a missing index fails the build instead of silently hiding the project. Pages and cards show the resolved module version. Source links, fallback images and repository references use that version (or its commit for a Go pseudo-version); editing links still use the working branch. Local module replacements use the working branch and do not display a released version.

Rules for a repository's `docs/`: plain GitHub Markdown, title = first `# H1`, `docs/README.md` is the project page and its link order is the sidebar order, relative links (`guide/x.md`, `../CONTRIBUTING.md`), images in `docs/assets/`. `docs/dev/` is not published.

Nested indexes such as `docs/guide/README.md` become sections and appear in the sidebar with their child pages. Root-relative site URLs (`/projects/`) and protocol-relative CDN URLs (`//example.org/...`) are preserved; relative links and images retain query parameters and fragments.

Docs titles have stable anchors based on the original English title, including translated pages. When translating other headings, preserve linked anchors with explicit IDs, e.g. `## Detalhes {#details}` for `## Details`. Content declares its actual language for screen readers. Regression checks also validate local HTML fragments in docs.

Docs use wrapping headings and larger sidebar touch targets on mobile. Print styles expand the content to the available width and wrap table cells. Reduced-motion preferences disable card movement and smooth scrolling.

Site layer (`docs-site/<slug>/<lang>/`, written here, not in the project repo):
- a file with the same path as a repository page translates that page for `<lang>` (e.g. `docs-site/lazyagents/pt-br/README.md`); the page links back to the English original;
- any other path is a page that exists only on the site, in that language (e.g. `visao-geral.md`);
- optional front matter: `title`, `weight` (repository pages get 10, 20, 30… in the README link order; `weight: 1` puts a site page first).

Translations are optional: an untranslated page shows the English text with a notice. They live where `translations:` in `data/docs.yaml` says: `repo` (default, `docs/pt-br/<same path>` in the project, versioned with the code and readable on GitHub) or `site` (`docs-site/<slug>/pt-br/`). A repository translation always wins.

Translations: each one records `<!-- source: <mark> -->` under its title (invisible on GitHub; `source:` in front matter also works), the mark of the English original it was made from: `sha256sum docs/<path> | cut -c1-12`. Links inside `docs/pt-br/` are written for GitHub (`../configuration.md` for a page not translated yet, `../../CONTRIBUTING.md` outside `docs/`) and the site maps them to its pages. The project's docs workflow warns on the PR when a translation falls behind. When the original changes, the page shows an "original changed" notice. `/docs/traducoes/` (not linked, not indexed) lists every page with its state and current mark.

### Publishing flow

1. A project's PR changes `docs/` with the feature. Its `.github/workflows/docs.yml` calls `project-docs.yml` (in this repo), which checks that every page starts with `# H1` and that relative links exist.
2. The project tags a release (`vX.Y.Z`). The same workflow sends a `docs-release` dispatch to this repo (secret `SITE_DISPATCH_TOKEN` in the project: a fine-grained token for this repository only, Contents read and write).
3. `deploy.yml` runs; `scripts/docs-latest.sh` updates imported projects in `data/docs.yaml`, and the site is published after validation. External documentation entries are skipped. Without the token, the daily scheduled deploy picks the update up.

Go's `@latest` resolution is used: stable semantic versions take precedence; repositories without release tags may resolve to a commit. The displayed version always comes from the resolved module.

Add an imported project: an `[[imports]]` block in `module.toml`, an entry in `data/docs.yaml`, and the caller workflow in the project (see the header of `.github/workflows/project-docs.yml`). `scripts/docs-latest.sh` discovers registered module imports automatically.

PR builds use pinned `go.mod`/`go.sum` versions. Deploys explicitly enable `update_docs` and keep automatic updates. To reproduce a deployed docs version locally, pin the version shown on its page with `hugo mod get github.com/<owner>/<repo>@<version>`.

Preview docs that are not pushed yet:

```sh
HUGO_MODULE_REPLACEMENTS="github.com/rogeriojunior31/lazyagents -> $HOME/Projects/lazyagents" hugo server
```
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
- `project-docs.yml`: reusable workflow for every project's `docs/` (validate, then notify this site on a release tag)
- `deploy.yml` also runs on a project's `docs-release` dispatch and once a day
- Dependabot keeps the actions and Blowfish up to date

Requires Settings → Pages → Source set to **GitHub Actions**.

Local docs regression checks: `python scripts/check-docs.py` (Python standard library only). Builds both languages, checks local links/assets, metadata and version links, and exercises external docs plus invalid configurations in a temporary copy.
