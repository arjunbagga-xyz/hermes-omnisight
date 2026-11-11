"""FastAPI web router for OmniSight surface inspection and diff stream endpoints."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from ..engine import LAST_OMNISIGHT_CACHE, OMNISIGHT_ENGINE

router = APIRouter()


@router.get("/status")
def get_omnisight_status() -> Dict[str, Any]:
    """Return active OmniSight inspection state and defect telemetry."""
    return {
        "plugin": "omnisight",
        "status": "active",
        "cdp_port": OMNISIGHT_ENGINE.cdp_port,
        "latest_inspection": LAST_OMNISIGHT_CACHE.get("latest_inspection"),
        "latest_diff": LAST_OMNISIGHT_CACHE.get("latest_diff"),
    }


@router.get("/inspect")
def get_inspect_surface(viewport: str = "mobile_393x852") -> Dict[str, Any]:
    """Trigger on-demand surface inspection."""
    return OMNISIGHT_ENGINE.inspect_surface(viewport=viewport)
