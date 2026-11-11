"""Smoke test suite for OmniSight spatial perception and AST resolution."""

from __future__ import annotations

import json

from omnisight.engine import (
    OmniSightEngine,
    handle_omnisight_generate_diff_slider,
    handle_omnisight_inspect_surface,
    handle_omnisight_resolve_pixel_to_ast,
    handle_omnisight_verify_layout,
)


def test_collision_and_overflow_detection():
    engine = OmniSightEngine()
    inspection = engine.inspect_surface(viewport="mobile_393x852", scene="broken")

    assert inspection["status"] == "defects_detected"
    assert inspection["defect_count"] >= 2
    types = [d["type"] for d in inspection["defects"]]
    assert "COLLISION" in types or "OVERFLOW" in types


def test_ast_pixel_bidirectional_resolution():
    engine = OmniSightEngine()
    # Click near the checkout button (bounds 24, 14, 120, 40)
    res = engine.resolve_pixel_to_ast(x=40.0, y=20.0)

    assert res["found"] is True
    assert res["element"] == "button"
    assert "CheckoutModal.tsx" in res["source_loc"]
    assert res["line"] == 42


def test_verify_layout_and_diff_directive():
    engine = OmniSightEngine()
    verify_res = engine.verify_layout(expected_clean=True)

    assert verify_res["verified"] is True
    assert verify_res["remaining_defects"] == 0
    assert "::omnisight-diff" in verify_res["directive"]
    assert 'status="healed"' in verify_res["directive"]


def test_tool_handlers():
    insp_raw = handle_omnisight_inspect_surface({"viewport": "mobile_393x852"})
    assert isinstance(insp_raw, str)
    insp = json.loads(insp_raw)
    assert "defect_count" in insp

    ast_raw = handle_omnisight_resolve_pixel_to_ast({"x": 20.0, "y": 20.0})
    assert isinstance(ast_raw, str)
    ast_res = json.loads(ast_raw)
    assert "source_loc" in ast_res

    ver_raw = handle_omnisight_verify_layout({"expected_clean": True})
    assert isinstance(ver_raw, str)
    ver = json.loads(ver_raw)
    assert ver["verified"] is True

    diff_raw = handle_omnisight_generate_diff_slider({"before_count": 3, "after_count": 0})
    assert isinstance(diff_raw, str)
    diff = json.loads(diff_raw)
    assert "directive" in diff
