# CYBERWIND / visual system

Dark navy #060A12, panel #081625, wind blue #42BFFF, cyan #63E9FF, text #DDF8FF. Each illustration owns its background for both GitHub themes. Cards use a consistent 620×240 canvas, 28px inset and numbered labels. Animatter takes the first full-width slot; complementary tools form a Markdown table. Small screens may scroll the table; all project descriptions remain available as real text.

## Reproduce

Python 3.12: `pip install -r scripts/requirements.txt`, then `python scripts/generate_banner.py`, `python scripts/generate_cards.py`, `python scripts/verify.py`.

The avatar is downloaded from the authenticated account's public GitHub avatar (user ID 170068203), archived losslessly as PNG and base64 for transport. The source character belongs to its respective rights holders; this is personal profile use, not a claim of character ownership. To refresh explicitly replace avatar.b64 and remove avatar.png before rendering.

The original deterministic city uses three architectural layers, chamfered roofs, aligned window bays, antennae and directional ground reflections. No stock imagery or commercial generation service is required.

The renderer samples both real avatar pixels and the city into a 200×67 grid. Color, luminance, gradient magnitude, alpha/spatial mask, coordinates, region and depth are archived in pixel-grid.npz. Edge and brightness control reconstruction order; depth delays the city; unresolved pixels follow a curved displacement field. Color-sampled transmission particles travel toward the skyline. Local scan-line offsets supply brief glitch frames. A reversible envelope returns continuously to the initial low-energy state while branding remains readable. The subject mask is spatial rather than semantic segmentation; source background is intentionally retained.

96 frames at 90ms, 1200×400, indexed GIF with one shared 256-color palette. Static SVG embeds the full-resolution raster snapshot for identical appearance; it is not a fully vectorized illustration. PNG fallback is included. Fonts use Consolas on Windows or DejaVu Sans Mono on Linux; geometry and input sampling are deterministic but glyph rasterization differs by platform.

CI installs pinned dependencies, regenerates and validates files, then commits only generated assets. Path filters exclude generated outputs and the built-in workflow token does not recursively trigger new push workflows. No scheduled updates, secrets or external stats dependencies.

Project descriptions were checked against public READMEs on 2026-10-31. They describe source capabilities, not independent game-runtime acceptance or release verification.
