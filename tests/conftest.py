"""Build the wiki once per test session and give tests the rendered pages."""

import subprocess
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("site")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--quiet",
         "-f", "config_local.yml", "-d", str(out)],
        check=True, cwd=ROOT,
    )
    return out


def page(site: Path, path: str) -> BeautifulSoup:
    """Parse a built page; path is "", "portal/allocation/" or "404.html"."""
    file = site / path if path.endswith(".html") else site / path / "index.html"
    return BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
