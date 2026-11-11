"""OmniSight: Multi-Surface Spatial Perception, AST Linking, and UI Self-Healing."""

from __future__ import annotations

from typing import Any, Dict

from .engine import (_ensure_json_str,
    DIFF_SLIDER_SCHEMA,
    INSPECT_SCHEMA,
    RESOLVE_AST_SCHEMA,
    VERIFY_LAYOUT_SCHEMA,
    handle_omnisight_generate_diff_slider,
    handle_omnisight_inspect_surface,
    handle_omnisight_resolve_pixel_to_ast,
    handle_omnisight_verify_layout,
)
from .middleware import omnisight_tool_execution_middleware


def _tool_handler(fn):
    """Wrap a dict-returning engine handler so Hermes tool_call gets a JSON string."""
    def wrapper(args=None, **kwargs):
        result = fn(args if args is not None else {})
        return _ensure_json_str(result)
    return wrapper


def on_session_start_hook(payload: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Hook invoked when a new Hermes agent session initializes."""
    return {"status": "omnisight-ready", "spatial_tracking": True}


def register(ctx: Any) -> None:
    """Register OmniSight tools, hooks, and middleware with the Hermes Plugin Context."""
    ctx.register_tool(
        name="omnisight_inspect_surface",
        toolset="omnisight",
        schema=INSPECT_SCHEMA,
        handler=_tool_handler(handle_omnisight_inspect_surface),
        is_async=False,
        emoji="👁️",
    )
    ctx.register_tool(
        name="omnisight_resolve_pixel_to_ast",
        toolset="omnisight",
        schema=RESOLVE_AST_SCHEMA,
        handler=_tool_handler(handle_omnisight_resolve_pixel_to_ast),
        is_async=False,
        emoji="🎯",
    )
    ctx.register_tool(
        name="omnisight_verify_layout",
        toolset="omnisight",
        schema=VERIFY_LAYOUT_SCHEMA,
        handler=_tool_handler(handle_omnisight_verify_layout),
        is_async=False,
        emoji="✅",
    )
    ctx.register_tool(
        name="omnisight_generate_diff_slider",
        toolset="omnisight",
        schema=DIFF_SLIDER_SCHEMA,
        handler=_tool_handler(handle_omnisight_generate_diff_slider),
        is_async=False,
        emoji="🎚️",
    )

    ctx.register_hook("on_session_start", on_session_start_hook)

    if hasattr(ctx, "register_middleware"):
        ctx.register_middleware("tool_execution", omnisight_tool_execution_middleware)
