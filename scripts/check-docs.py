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


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def build(source, output, succeeds=True, env=None):
    result = subprocess.run(
        ["hugo", "--minify", "--panicOnWarning", "--destination", str(output)],
        cwd=source, capture_output=True, text=True, env=env,
    )
    assert (result.returncode == 0) == succeeds, result.stdout + result.stderr
    return result.stdout + result.stderr


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
            description = next(attrs["content"] for tag, attrs in html.tags if tag == "meta" and attrs.get("name") == "description")
            assert not description.startswith(("Site pessoal", "Personal site")), file
    graph = subprocess.check_output(["hugo", "mod", "graph"], cwd=root, text=True)
    version = re.search(r"github.com/rogeriojunior31/lazyagents@(\S+)", graph).group(1).removesuffix("+incompatible")
    pseudo = re.search(r"-\d{14}-([0-9a-f]{12})$", version)
    ref = pseudo.group(1) if pseudo else version
    for lang in ("", "en/"):
        project = (output / lang / "docs/lazyagents/index.html").read_text()
        assert "docs-version" in project
        assert f"/blob/{ref}/docs/README.md" in project
        assert "/blob/main/docs/README.md" in project, "Editing must still use the working branch"
        assert (output / lang / "docs/lazyagents/guide/skills/index.html").exists()
    print(f"OK: {len(files)} HTML files, local links/assets, metadata, versions and navigation")


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
    (local / "docs/guide/README.md").write_text("# Guide index\n\n[Topic](topic.md#details)\n")
    (local / "docs/guide/topic.md").write_text("# Guide topic\n\n## Details\n\nContent.\n")
    (local / "docs/assets").mkdir()
    (local / "docs/assets/sample.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" id="icon" viewBox="0 0 1 1"></svg>')
    with (local / "docs/README.md").open("a") as fixture:
        fixture.write("\n![Local asset](assets/sample.svg?color=orange#icon)\n")
    preview = temp / "preview"
    build(source, preview, env=os.environ | {"HUGO_MODULE_REPLACEMENTS": f"github.com/rogeriojunior31/lazyagents -> {local}"})
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
        guide = HTML((preview / lang / "docs/lazyagents/guide/index.html").read_text())
        assert any(attrs.get("href") == f"/{lang}docs/lazyagents/guide/topic/#details" for _, attrs in guide.tags)
    print("OK: nested README indexes, sidebar children, absolute/CDN URLs and asset query/fragment")
