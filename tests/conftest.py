from __future__ import annotations

import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import textwrap
import time

import pytest
from playwright._impl._errors import Error as PlaywrightError


# pytest 実行時にプロジェクトルートを import path に追加し、`main` などの
# ルートモジュールを確実に解決できるようにする。GitHub Actions では
# ワーキングディレクトリが tests ディレクトリではなくても先頭に入らない
# ことがあり、ModuleNotFoundError が発生していた。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def write_sample_xml(tmp_path: Path):
    """Return a helper that writes a minimal SdImportExport XML file."""

    def _writer(body: str, filename: str = "sample.sgexml") -> Path:
        xml_text = textwrap.dedent(
            f"""\
            <?xml version="1.0" encoding="utf-8"?>
            <SdImportExport>
            {body}
            </SdImportExport>
            """
        ).strip()
        sample_path = tmp_path / filename
        sample_path.write_text(xml_text, encoding="utf-8")
        return sample_path

    return _writer


FLASK_PORT = 5001
SERVER_URL = f"http://127.0.0.1:{FLASK_PORT}/?debug=1"
_SERVER_START_TIMEOUT = 15
_SYSTEM_CHROMIUM_CANDIDATES = (
    "chromium",
    "chromium-browser",
    "google-chrome",
    "google-chrome-stable",
)


def _wait_for_port(port: int, host: str = "127.0.0.1", timeout: float = _SERVER_START_TIMEOUT) -> None:
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return
            except OSError:
                time.sleep(0.2)
    raise TimeoutError(f"Unable to reach {host}:{port} within {timeout:.1f}s")


def launch_chromium(playwright, *, headless: bool = True):
    """Return a Chromium browser or skip when none is available.

    - `PLAYWRIGHT_CHROMIUM_PATH` で明示指定された実行ファイル
    - 環境にインストール済みの Chromium/Chrome
    - Playwright 同梱ブラウザ

    の順で試行し、いずれも見つからない場合は pytest.skip する。
    """

    def iter_candidate_paths():
        env_path = os.environ.get("PLAYWRIGHT_CHROMIUM_PATH")
        if env_path:
            yield env_path
        for name in _SYSTEM_CHROMIUM_CANDIDATES:
            path = shutil.which(name)
            if path:
                yield path

    for candidate in iter_candidate_paths():
        try:
            return playwright.chromium.launch(headless=headless, executable_path=candidate)
        except PlaywrightError:
            continue

    try:
        return playwright.chromium.launch(headless=headless)
    except PlaywrightError as exc:  # pragma: no cover - depends on env setup
        message = str(exc)
        if "Executable doesn't exist" in message or "playwright install" in message:
            pytest.skip(
                "Chromium が見つかりません。"
                "'python -m playwright install --with-deps chromium' または "
                "'apt-get install chromium-browser' を実行してから再試行してください。"
            )
        raise


@pytest.fixture(scope="session")
def flask_server():
    cmd = [
        sys.executable,
        "-u",
        "-c",
        "from main import create_app; create_app().run(port=5001)",
    ]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=Path(__file__).resolve().parents[1],
    )
    try:
        _wait_for_port(FLASK_PORT)
        yield
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
