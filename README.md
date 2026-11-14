# OmniSight: Multi-Surface Spatial Perception & UI Self-Healing

**OmniSight** gives Hermes autonomous spatial vision across Chrome DevTools Protocol (CDP), responsive viewport hierarchies, and native UI boundaries.

It solves layout regressions and accessibility collisions by inspecting rendered DOM quads, linking on-screen pixels directly to source AST code lines, and generating interactive Before/After drag-sliders in Hermes Desktop.

---

## 🚀 Capabilities

1. **Multi-Surface Perception**: Connects to CDP (`ws://127.0.0.1:9222`) or headless synthetic layout trees to capture rendered layouts and responsive viewports.
2. **Defect Geometry Detection**: Automatically flags element overlap collisions, viewport overflow blowouts, and undersized mobile touch targets (<48px).
3. **AST-to-Pixel Source Mapping**: Bi-directional linking between rendered screen coordinates and source component files (`data-hermes-source`).
4. **Interactive Before/After Split-Slider**: Renders a draggable split-view card (`::omnisight-diff`) in Hermes Desktop transcripts with 1-click fix approval.

---

## 🛠️ Tools

* `omnisight_inspect_surface(target_url, viewport, scene)`: Inspects UI surface layout. Pass `scene='demo'` to inspect a synthetic sample scene. Live CDP DOM inspection is not yet implemented (returns an explicit error).
* `omnisight_resolve_pixel_to_ast(x, y)`: Maps screen coordinate to exact source code line from inspected elements.
* `omnisight_verify_layout(expected_clean)`: Validates that responsive collisions are resolved.
* `omnisight_generate_diff_slider(before_count, after_count)`: Creates interactive desktop comparison directive.

---

## 📄 License

MIT © 2026 Arjun Bagga
