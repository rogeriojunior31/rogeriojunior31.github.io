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

Projects may own their display metadata in `docs/site.json`. The website reads it from the same revision as their docs and uses it in the catalog, page metadata and search. Older projects keep using the registry's `name` and `summary`; registration and the module mount are still required once per project. The shared workflow validates this optional file:

```json
{
  "schema": 1,
  "name": "My project",
  "requiredTranslations": ["pt-br"],
  "summary": {
    "en": "Project documentation.",
    "pt-br": "Documentação do projeto."
  }
}
```

Each configured website language needs a summary. Translations are detected by corresponding Markdown paths, not declared complete in the metadata. A translated index alone does not translate its linked pages. Check `/docs/traducoes/` for missing or outdated translations; source marks must only be refreshed after reviewing the translation.

To require complete translations, add `"requiredTranslations": ["pt-br"]` to the project's `docs/site.json`. Every public original must then have a reviewed translation with the current source mark; missing, unmarked or outdated translations fail the shared workflow and website build. The lazyagents project also enforces this contract in `go test ./docs`. Do not stamp a new hash on an unreviewed translation. HTML `id` anchors preserve section links in both the repository and the generated website.

Rules for a repository's `docs/`: plain GitHub Markdown, title = first `# H1`, `docs/README.md` is the project page and its link order is the sidebar order, relative links (`guide/x.md`, `../CONTRIBUTING.md`), images in `docs/assets/`. `docs/dev/` is not published.

Nested indexes such as `docs/guide/README.md` become sections and appear in the sidebar with their child pages. Root-relative site URLs (`/projects/`) and protocol-relative CDN URLs (`//example.org/...`) are preserved; relative links and images retain query parameters and fragments.

Docs titles have stable anchors based on the original English title, including translated pages. When translating other headings, preserve linked anchors with explicit IDs, e.g. `## Detalhes {#details}` for `## Details`. Content declares its actual language for screen readers. Regression checks also validate local HTML fragments in docs.

Docs use wrapping headings and larger sidebar touch targets on mobile. Print styles expand the content to the available width and wrap table cells. Reduced-motion preferences disable card movement and smooth scrolling.

Previous/next links follow the sidebar order within the current project and language. Search includes external documentation entries and content excerpts for imported docs, retaining the theme's fallback for untranslated pages. Results update when pasting or clearing text, including queries entered before the search index finishes loading.

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

### lazyagents showcase

The home and project pages use `{{< lazyagents >}}` (`placement="home"` on the home); the docs index uses the same `layouts/partials/lazyagents-showcase.html`. Copy is localized in the partial. The official logo is copied from the project's `docs/assets/logo.png` to `assets/img/lazyagents/logo.png`; Hugo generates WebP sizes for the showcase, docs cards and sidebar.

`static/media/lazyagents/demo.mp4` is the project's hero demo (`docs/assets/demos/hero.mp4`, recorded by `scripts/record-demo.sh` with fictitious data): a silent 13-second clip that enables a skill in every agent, reads a session as a log and shows the usage limits. It is 1904×1026 (2x), H.264, 30 fps with fast start, without a window frame because the showcase draws its own. `poster.webp` is the frame at 2.8s (the skill enabled in all agents). When updating the recording, review the duration label and aria labels in the partial, the aspect ratio in `custom.css` and the duration check in `scripts/check-search-browser.py`. Native video controls and `preload="none"` keep playback optional and avoid downloading the video before the visitor plays it.

### SP Night showcase

The SP Night project page and docs index use `{{< spnight >}}` / `layouts/partials/spnight-showcase.html`. Besides `docs/`, `config/_default/module.toml` mounts the project's `palette/sp_night.json`, `registry/ports.yml` and `registry/copy.yml` as `hugo.Data.spnight`, so the flavour swatches, flavour descriptions and port list come from the same module version as the docs. Nothing is copied by hand: a new port or a retuned colour appears with the next docs release.

Docs logos are read from each imported project's `docs/assets/logo.png` (resized to WebP) or `docs/assets/logo.svg` by `layouts/partials/docs/logo.html`, used by the docs cards and sidebar.

Preview SP Night docs that are not pushed yet:

```sh
HUGO_MODULE_REPLACEMENTS="github.com/sp-night/sp-night -> $HOME/Projects/SP-Night/sp-night" hugo server
```

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

Optional browser checks against a running preview: `uv run --with playwright python scripts/check-search-browser.py http://localhost:1313` (install Chromium first with `uv run --with playwright playwright install chromium`). Covers both languages at four viewport widths, reading links, search input changes, a delayed search index and print visibility.

Complete lazyagents and SP Night language checks: `python3 scripts/check-docs-language.py public` or `python3 scripts/check-docs-language.py https://rogeriojunior31.github.io`. Checks every public English doc and its Portuguese counterpart, rejecting English fallback, stale translations, identical untranslated bodies and duplicate HTML anchors. CI checks the built artifact before publication.
