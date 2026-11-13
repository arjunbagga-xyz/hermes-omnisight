"""OmniSight Middleware: Intercepts frontend edits and attaches visual Before/After diff directives."""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional

from .engine import OMNISIGHT_ENGINE

logger = logging.getLogger("hermes.omnisight.middleware")

FRONTEND_EXTENSIONS = {".tsx", ".jsx", ".vue", ".css", ".html", ".svelte"}


def omnisight_tool_execution_middleware(
    tool_name: Optional[str] = None,
    args: Optional[Dict[str, Any]] = None,
    next_call: Optional[Callable[..., Any]] = None,
    **kwargs: Any,
) -> Any:
    """
    Hermes tool_execution middleware contract:
    (tool_name: str, args: dict, next_call: callable, **kwargs)
    """
    name = tool_name or kwargs.get("name", "")
    tool_args = args if args is not None else kwargs.get("arguments", {})
    result = next_call(tool_args if args is not None else kwargs) if next_call else None

    if name in {"write_file", "patch"} and isinstance(tool_args, dict):
        path = str(tool_args.get("path") or tool_args.get("Path") or "")
        if any(path.endswith(ext) for ext in FRONTEND_EXTENSIONS):
            diff_res = OMNISIGHT_ENGINE.generate_diff_slider(before_count=2, after_count=0)
            directive = diff_res.get("directive", "")
            if isinstance(result, str):
                result += f"\n\n{directive}"
            elif isinstance(result, dict) and "output" in result and isinstance(result["output"], str):
                result["output"] += f"\n\n{directive}"

    return result
