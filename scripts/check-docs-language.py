#!/usr/bin/env python3
"""Check every lazyagents doc, locally or on the published website (stdlib only)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen
import json
import sys


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.content_lang = None
        self.content = []
        self.depth = 0
        self.ids = []
        self.stale = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        classes = attrs.get("class", "").split()
        self.stale |= "docs-stale" in classes
        if "article-content" in classes:
            self.content_lang = attrs.get("lang")
            self.depth = 1
        elif self.depth and tag not in ("img", "br", "hr", "input", "meta", "link", "source", "wbr"):
            self.depth += 1

    def handle_endtag(self, tag):
        if self.depth and tag not in ("img", "br", "hr", "input", "meta", "link", "source", "wbr"):
            self.depth -= 1

    def handle_data(self, text):
        if self.depth:
            self.content.append(text)


base = sys.argv[1] if len(sys.argv) > 1 else "public"


def read(path):
    if base.startswith(("https://", "http://")):
        with urlopen(base.rstrip("/") + path, timeout=30) as response:
            return response.read().decode("utf-8")
    return (Path(base) / path.lstrip("/") / "index.html").read_text() if path.endswith("/") else (Path(base) / path.lstrip("/")).read_text()


search = json.loads(read("/en/index.json"))
pages = sorted({entry["permalink"] for entry in search if entry["permalink"].startswith("/en/docs/lazyagents/")})
assert len(pages) >= 19, f"Expected all 19 public docs, found {len(pages)}"
for english_path in pages:
    portuguese_path = english_path.removeprefix("/en")
    en = Document(read(english_path))
    pt = Document(read(portuguese_path))
    assert en.content_lang == "en", english_path
    assert pt.content_lang == "pt-BR", f"English fallback instead of Portuguese: {portuguese_path}"
    assert not pt.stale, f"Outdated translation: {portuguese_path}"
    assert "".join(pt.content).strip() != "".join(en.content).strip(), f"Untranslated body: {portuguese_path}"
    for path, document in ((english_path, en), (portuguese_path, pt)):
        assert len(document.ids) == len(set(document.ids)), f"Duplicate HTML anchor: {path}"
print(f"OK: {len(pages)}/{len(pages)} public docs translated, current, with PT/EN content and unique anchors")
