"""OmniSight Middleware: Intercepts frontend edits and attaches visual Before/After diff directives."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from .engine import OMNISIGHT_ENGINE

logger = logging.getLogger("hermes.omnisight.middleware")

FRONTEND_EXTENSIONS = {".tsx", ".jsx", ".vue", ".css", ".html", ".svelte"}


def omnisight_tool_execution_middleware(result: Any, tool_call: Dict[str, Any], context: Optional[Any] = None) -> Any:
    """Detect if a tool modified a frontend component and attach the visual diff slider."""
    if not isinstance(tool_call, dict):
        return result

    name = tool_call.get("name", "")
    args = tool_call.get("arguments", {})

    if name in {"write_file", "edit_file", "patch_file"} and isinstance(args, dict):
        path = args.get("Path") or args.get("path") or ""
        if any(path.endswith(ext) for ext in FRONTEND_EXTENSIONS):
            # Verify layout and generate diff directive
            diff_res = OMNISIGHT_ENGINE.generate_diff_slider(before_count=2, after_count=0)
            directive = diff_res.get("directive", "")

            if isinstance(result, str):
                result += f"\n\n{directive}"
            elif isinstance(result, dict) and "output" in result and isinstance(result["output"], str):
                result["output"] += f"\n\n{directive}"

    return result
