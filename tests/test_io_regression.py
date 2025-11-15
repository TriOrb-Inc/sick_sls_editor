from __future__ import annotations

import json
from pathlib import Path

import main

_DATA_DIR = Path(__file__).parent / "data"
_SAMPLE_XML = _DATA_DIR / "io_sample.sgexml"
_EXPECTED_JSON = _DATA_DIR / "io_expected.json"


def _collect_io_payloads() -> dict:
    fieldsets_payload, triorb_shapes, triorb_source = main.load_fieldsets_and_shapes()
    return {
        "menu_items": main.load_menu_items(),
        "fileinfo_fields": main.load_fileinfo_fields(),
        "root_attributes": main.load_root_attributes(),
        "scan_planes": main.load_scan_planes(),
        "casetable_payload": main.load_casetable_payload(),
        "fieldsets_payload": fieldsets_payload,
        "triorb_shapes": triorb_shapes,
        "triorb_source": triorb_source,
    }


def test_io_payloads_match_snapshot(monkeypatch):
    monkeypatch.setattr(main, "SAMPLE_XML", _SAMPLE_XML)

    actual = _collect_io_payloads()
    expected = json.loads(_EXPECTED_JSON.read_text(encoding="utf-8"))

    assert actual == expected
