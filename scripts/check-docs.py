#!/usr/bin/env python3
"""Build and regression checks for docs, using only the Python standard library."""
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
import shutil
import subprocess
import re
import os
import json
import hashlib


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.navs = []
        self.nav_stack = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "nav":
            nav = {"attrs": attrs, "links": []}
            self.navs.append(nav)
            self.nav_stack.append(nav)
        elif tag == "a":
            for nav in self.nav_stack:
                nav["links"].append(attrs)

    def handle_endtag(self, tag):
        if tag == "nav" and self.nav_stack:
            self.nav_stack.pop()


def build(source, output, succeeds=True, env=None):
    result = subprocess.run(
        ["hugo", "--minify", "--panicOnWarning", "--destination", str(output)],
        cwd=source, capture_output=True, text=True, env=env,
    )
    assert (result.returncode == 0) == succeeds, result.stdout + result.stderr
    return result.stdout + result.stderr


def replacements(local):
    """Fake lazyagents module, keeping replacements already set (e.g. unreleased SP Night docs)."""
    return ",".join(filter(None, (os.environ.get("HUGO_MODULE_REPLACEMENTS"), f"github.com/rogeriojunior31/lazyagents -> {local}")))


def check_fragments(output):
    documents = {file: HTML(file.read_text()) for file in output.rglob("*.html")}
    for file, html in documents.items():
        if "docs" not in file.relative_to(output).parts:
            continue
        for tag, attrs in html.tags:
            url = urlsplit(attrs.get("href", ""))
            if tag != "a" or not url.fragment or url.fragment == "cookies":
                continue  # The Cookies link is handled by the consent script.
            if url.scheme not in ("", "http", "https") or (url.netloc and url.netloc != "rogeriojunior31.github.io"):
                continue
            target = file if not url.path else ((output / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (file.parent / unquote(url.path)))
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if target.suffix == ".html":
                ids = {attrs.get("id") for _, attrs in documents[target].tags}
                assert unquote(url.fragment) in ids, f"{file}: missing anchor {attrs['href']}"


def check_site(output):
    files = list(output.rglob("*.html"))
    assert files, "No HTML generated"
    for file in files:
        html = HTML(file.read_text())
        for tag, attrs in html.tags:
            for attr in ("href", "src"):
                url = urlsplit(attrs.get(attr, ""))
                if url.netloc and url.netloc != "rogeriojunior31.github.io":
                    continue
                if not url.path or url.scheme not in ("", "http", "https"):
                    continue
                target = (output / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (file.parent / unquote(url.path))
                assert target.exists(), f"{file}: missing {attrs[attr]}"
        if any("docs-layout" in attrs.get("class", "").split() for _, attrs in html.tags):
            assert any(tag == "details" and "data-docs-nav" in attrs for tag, attrs in html.tags), file
            locale = next(attrs["lang"] for tag, attrs in html.tags if tag == "html")
            breadcrumb = next(attrs for tag, attrs in html.tags if tag == "nav" and attrs.get("class") == "docs-crumbs")
            assert breadcrumb["aria-label"] == ("Breadcrumb" if locale == "en" else "Caminho da página"), file
            description = next(attrs["content"] for tag, attrs in html.tags if tag == "meta" and attrs.get("name") == "description")
            assert not description.startswith(("Site pessoal", "Personal site")), file
    graph = subprocess.check_output(["hugo", "mod", "graph"], cwd=root, text=True)
    version = re.search(r"github.com/rogeriojunior31/lazyagents@(\S+)", graph).group(1).removesuffix("+incompatible")
    pseudo = re.search(r"-\d{14}-([0-9a-f]{12})$", version)
    ref = pseudo.group(1) if pseudo else version
    for lang in ("", "en/"):
        project = (output / lang / "docs/lazyagents/index.html").read_text()
        assert "docs-version" in project
        title_lang = next(attrs["lang"] for tag, attrs in HTML(project).tags if tag == "h1")
        source = "docs/pt-br/README.md" if title_lang == "pt-BR" else "docs/README.md"
        assert f"/blob/{ref}/{source}" in project
        assert f"/blob/main/{source}" in project, "Editing must still use the working branch"
        assert (output / lang / "docs/lazyagents/guide/skills/index.html").exists()
        sp_night = (output / lang / "docs/sp-night/index.html").read_text()
        assert "spn-palette" in sp_night, "SP Night docs index shows the palette"
    check_fragments(output)
    check_reading_navigation(output)
    for lang in ("", "en/"):
        search = json.loads((output / lang / "index.json").read_text())
        assert all("/docs/traducoes/" not in entry["permalink"] for entry in search)
        assert any(entry["permalink"] == f"/{lang}docs/sp-night/reference/cli/" for entry in search), "SP Night docs are imported"
        doc = next(entry for entry in search if entry["permalink"] == f"/{lang}docs/lazyagents/guide/skills/")
        assert doc["summary"], "Docs search results need context"
        assert any(entry["permalink"] == "/docs/lazyagents/visao-geral/" for entry in search), "Retain search fallback for pages without translations"
    print(f"OK: {len(files)} HTML files, local links/assets, metadata, versions and navigation")


def check_reading_navigation(output):
    for file in output.rglob("*.html"):
        html = HTML(file.read_text())
        sidebar = next((nav for nav in html.navs if nav["attrs"].get("aria-label") in ("Project documentation", "Documentação do projeto")), None)
        if not sidebar:
            continue
        order = [link["href"] for link in sidebar["links"]]
        canonical = next(attrs["href"] for tag, attrs in html.tags if tag == "link" and attrs.get("rel") == "canonical")
        current = order.index(urlsplit(canonical).path)
        pager = next((nav for nav in html.navs if "docs-pagination" in nav["attrs"].get("class", "").split()), None)
        if len(order) == 1:
            assert pager is None, file
            continue
        assert pager is not None, file
        previous = [link["href"] for link in pager["links"] if link.get("rel") == "prev"]
        following = [link["href"] for link in pager["links"] if link.get("rel") == "next"]
        assert previous == (order[current - 1:current] if current else []), file
        assert following == order[current + 1:current + 2], file


root = Path(__file__).resolve().parents[1]
with TemporaryDirectory(prefix="site-docs-check-") as temp:
    temp = Path(temp)
    output = temp / "public"
    build(root, output)
    check_site(output)

    source = temp / "site"
    shutil.copytree(root, source, ignore=shutil.ignore_patterns(".git", "public", "resources", ".hugo_build.lock"))
    registry = source / "data/docs.yaml"
    original = registry.read_text()
    registry.write_text(original + '\n- slug: external-test\n  name: External test\n  repo: example/external-test\n  url: https://example.org/docs/\n  summary:\n    en: "External summary fallback"\n')
    external = temp / "external"
    build(source, external)
    for lang, label in (("", "Documentação externa"), ("en/", "External documentation")):
        hub = (external / lang / "docs/index.html").read_text()
        assert "https://example.org/docs/" in hub and label in hub
        assert "External summary fallback" in hub
        assert not (external / lang / "docs/external-test").exists()
    print("OK: external docs in both languages, summary fallback, no local pages")

    registry.write_text(registry.read_text() + '\n  urlLanguage: en\n  urls:\n    pt-br: https://example.org/pt/docs/\n    en: https://example.org/en/docs/\n')
    build(source, external)
    for lang, url, label in (("", "https://example.org/pt/docs/", "Português"), ("en/", "https://example.org/en/docs/", "English")):
        hub = (external / lang / "docs/index.html").read_text()
        assert url in hub and label in hub
        search = json.loads((external / lang / "index.json").read_text())
        assert any(entry.get("externalUrl") == url for entry in search)
    registry.write_text(registry.read_text().replace("https://example.org/en/docs/", "javascript:alert(1)"))
    assert "URL HTTPS absoluta" in build(source, temp / "invalid-locale", succeeds=False)
    registry.write_text(original + '\n- slug: external-test\n  name: External test\n  repo: example/external-test\n  url: https://example.org/docs/\n  summary:\n    en: "External summary fallback"\n')
    print("OK: localized external URLs in hub/search; invalid translations rejected")

    # Test the updater without network access or changes to real module versions.
    mock_bin = temp / "bin"
    mock_bin.mkdir()
    mock = mock_bin / "hugo"
    mock.write_text('#!/bin/sh\nif [ "$*" = "mod graph" ]; then\n  printf "%s\\n" "site github.com/rogeriojunior31/lazyagents@v0.4.3"\nelse\n  printf "%s\\n" "$*"\nfi\n')
    mock.chmod(0o755)
    updated = subprocess.check_output(["bash", "scripts/docs-latest.sh"], cwd=source, text=True, env=os.environ | {"PATH": str(mock_bin) + os.pathsep + os.environ["PATH"]})
    assert "mod get github.com/rogeriojunior31/lazyagents@latest" in updated
    assert "example/external-test" not in updated
    print("OK: updater skips external documentation")

    registry.write_text(registry.read_text().replace("https://example.org/docs/", "javascript:alert(1)"))
    assert "URL HTTPS absoluta" in build(source, temp / "invalid", succeeds=False)
    registry.write_text(original + '\n- slug: missing-test\n  name: Missing docs\n  repo: example/missing-test\n')
    assert "docs/README.md ausente" in build(source, temp / "missing", succeeds=False)
    print("OK: invalid URLs and missing documentation fail the build")

    registry.write_text(original)
    local = temp / "local-module"
    (local / "docs").mkdir(parents=True)
    (local / "go.mod").write_text("module github.com/rogeriojunior31/lazyagents\n\ngo 1.27.1\n")
    (local / "docs/README.md").write_text("# Local preview\n\nUnreleased documentation.\n\n[Guides](guide/README.md)\n\n[Site projects](/projects/)\n\n[CDN docs](//example.org/docs/)\n\n[Download](assets/sample.svg?download=1#icon)\n\n![Site icon](/favicon-32x32.png)\n\n![CDN icon](//example.org/icon.png)\n")
    (local / "docs/guide").mkdir()
    (local / "docs/guide/README.md").write_text("# Guide index\n\n[Topic](topic.md#details)\n\n[Topic title](topic.md#guide-topic)\n")
    (local / "docs/guide/topic.md").write_text("# Guide topic\n\n## Details\n\nContent.\n")
    (local / "docs/assets").mkdir()
    (local / "docs/assets/sample.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" id="icon" viewBox="0 0 1 1"></svg>')
    with (local / "docs/README.md").open("a") as fixture:
        fixture.write("\n![Local asset](assets/sample.svg?color=orange#icon)\n\n[Top](README.md#local-preview)\n")
    (local / "docs/pt-br").mkdir()
    (local / "docs/pt-br/guide").mkdir()
    (local / "docs/pt-br/guide/topic.md").write_text("# Tópico traduzido\n\n## Detalhes {#details}\n\nConteúdo em português.\n")
    preview = temp / "preview"
    build(source, preview, env=os.environ | {"HUGO_MODULE_REPLACEMENTS": replacements(local)})
    page = (preview / "docs/lazyagents/index.html").read_text()
    assert "docs-version" not in page
    assert "/blob/main/docs/README.md" in page
    assert "/blob/v0.4.3/docs/README.md" not in page
    print("OK: local module previews do not claim a released version")
    for lang in ("", "en/"):
        page = HTML((preview / lang / "docs/lazyagents/index.html").read_text())
        links = [attrs["href"] for tag, attrs in page.tags if tag == "a"]
        images = [attrs["src"] for tag, attrs in page.tags if tag == "img"]
        assert "/projects/" in links and "//example.org/docs/" in links
        assert "/favicon-32x32.png" in images and "//example.org/icon.png" in images
        assert any(url.endswith("sample.svg?download=1#icon") for url in links)
        assert any(url.endswith("sample.svg?color=orange#icon") for url in images)
        assert f"/{lang}docs/lazyagents/guide/" in links
        assert f"/{lang}docs/lazyagents/guide/topic/" in links
        assert any(tag == "h1" and attrs.get("id") == "local-preview" and attrs.get("lang") == "en" for tag, attrs in page.tags)
        assert any("article-content" in attrs.get("class", "").split() and attrs.get("lang") == "en" for _, attrs in page.tags)
        guide = HTML((preview / lang / "docs/lazyagents/guide/index.html").read_text())
        assert any(attrs.get("href") == f"/{lang}docs/lazyagents/guide/topic/#details" for _, attrs in guide.tags)
    print("OK: nested README indexes, sidebar children, absolute/CDN URLs and asset query/fragment")
    translated = HTML((preview / "docs/lazyagents/guide/topic/index.html").read_text())
    assert any(tag == "h1" and attrs.get("lang") == "pt-BR" and attrs.get("id") == "guide-topic" for tag, attrs in translated.tags)
    assert any("article-content" in attrs.get("class", "").split() and attrs.get("lang") == "pt-BR" for _, attrs in translated.tags)
    check_fragments(preview)
    check_reading_navigation(preview)
    print("OK: title anchors and explicit content language for originals and translations")

    metadata = local / "docs/site.json"
    metadata.write_text(json.dumps({"schema": 1, "name": "Localized project", "summary": {"en": "Repository English summary", "pt-br": "Resumo vindo do projeto"}}))
    localized = temp / "localized"
    build(source, localized, env=os.environ | {"HUGO_MODULE_REPLACEMENTS": replacements(local)})
    for lang, summary in (("", "Resumo vindo do projeto"), ("en/", "Repository English summary")):
        hub = (localized / lang / "docs/index.html").read_text()
        assert "Localized project" in hub and summary in hub
        page = (localized / lang / "docs/lazyagents/index.html").read_text()
        assert "Localized project" in page and summary in page
    metadata.write_text(json.dumps({"schema": 1, "name": "Invalid", "summary": {"en": "English only"}}))
    assert "summary.pt-br" in build(source, temp / "invalid-metadata", succeeds=False, env=os.environ | {"HUGO_MODULE_REPLACEMENTS": replacements(local)})
    metadata.write_text(json.dumps({"schema": 2, "name": "Invalid", "summary": {"en": "English", "pt-br": "Portuguese"}}))
    assert "schema 1" in build(source, temp / "invalid-schema", succeeds=False, env=os.environ | {"HUGO_MODULE_REPLACEMENTS": replacements(local)})
    print("OK: versioned project metadata in both languages; missing summaries and unsupported schema fail the build")

    required = {"schema": 1, "name": "Strict translations", "summary": {"en": "English", "pt-br": "Portuguese"}, "requiredTranslations": ["pt-br"]}
    metadata.write_text(json.dumps(required))
    preview_env = os.environ | {"HUGO_MODULE_REPLACEMENTS": replacements(local)}
    assert "tradução obrigatória" in build(source, temp / "missing-translation", succeeds=False, env=preview_env)
    for original in (local / "docs").rglob("*.md"):
        rel = original.relative_to(local / "docs")
        if rel.parts[0] == "pt-br":
            continue
        translation = local / "docs/pt-br" / rel
        translation.parent.mkdir(parents=True, exist_ok=True)
        content = translation.read_text() if translation.exists() else original.read_text().replace("# Local preview", "# Prévia local").replace("# Guide index", "# Índice de guias")
        mark = hashlib.sha256(original.read_bytes()).hexdigest()[:12]
        translation.write_text(f"<!-- source: {mark} -->\n" + content)
    strict_output = temp / "strict"
    build(source, strict_output, env=preview_env)
    check_fragments(strict_output)
    translation = local / "docs/pt-br/guide/topic.md"
    translation.write_text(translation.read_text().replace(hashlib.sha256((local / "docs/guide/topic.md").read_bytes()).hexdigest()[:12], "000000000000"))
    assert "stale" in build(source, temp / "stale-translation", succeeds=False, env=preview_env)
    print("OK: strict translation coverage accepts reviewed docs and rejects missing or stale translations")
