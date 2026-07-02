# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Login card top edge. Removed the 6px orange `border-top` accent stripe from the login card in both the light and dark rules, and gave the card a card-coloured 1px border so the orange page backdrop can no longer bleed a hairline anti-aliasing seam at the card's rounded edge. The card top is now clean in both light and dark mode. (#24)
- Dark-mode connection list. Connection/group/user names and their protocol icons were dark-on-dark and nearly invisible: the base theme colours `.list-item .name` directly (so an inherited colour couldn't override it), and the icons are dark SVG background images that `color` can't touch. The dark block now recolours the labels (`.list-item .name`/`.usage`) and inverts the row icons (`filter: invert(1)`), so the home connection list and the Settings list tables are legible in dark mode; light mode is unchanged. (#26)
- Connection-list row hover. The base theme paints the row hover on the caption (`.list-item:not(.selected) .caption:hover { background: #cda }`), an off-brand khaki that the theme's row-level hover rule never overrode; in dark mode the light label was also low-contrast on it. The hover rule now includes that selector in both schemes, so the row hover is an orange brand tint that stays dark enough in dark mode to keep the label and icon legible. (#28)

## [1.3.0] - 2026-07-02

### Added

- Build-time configuration. `build.sh` is now a thin wrapper over `tools/build.py` and reads options from environment variables or a `theme.config` file (see `theme.config.example`). `BRAND_COLOR` recolours the whole theme (darker shades, the login-backdrop gradient, and rgba accents are derived automatically), `WORDMARK` changes the login mark, and `OUTPUT` sets the jar path. With no options set, the build reproduces the standard theme (identical rendering; the manifest byte-for-byte and the CSS apart from stripped build-time marker comments). (#1)
- Neutral, theme-only build variant. `VARIANT=neutral ./build.sh` emits `dist/guacamole-theme-orangelion-neutral.jar` with just the colour palette — no login mark, product-name override, or bundled icons — so Guacamole keeps its own logo and product name. (#9)
- Optional logo image. `LOGO=path/to/logo.svg ./build.sh` packs an SVG/PNG into the jar, exposes it as a manifest resource, and shows it on the login card in place of the wordmark. (#2)
- Multi-language product name. `APP_NAME` is written into an `APP.NAME` override for every locale in `LOCALES` (default `en`); example locale files added for Dutch and German (`translations/nl.json.example`, `translations/de.json.example`). (#8)
- Automatic dark-mode variant via a `@media (prefers-color-scheme: dark)` block: dark page and card backgrounds, light text, and orange shades tuned for dark surfaces, all meeting WCAG AA. A custom `BRAND_COLOR` recolours the light theme only. (#3)
- WCAG contrast audit documented in `docs/ACCESSIBILITY.md`, with the measured ratio and pass/fail for every foreground/background pair in both the light and dark themes. (#6)
- Guacamole version compatibility matrix in the README, recording the CI-verified load result per version (1.5.5, 1.6.0), an explanation of the `guacamoleVersion "*"` gate, and how to add a version. (#7)

### Changed

- Accessibility fixes so normal-size text meets WCAG AA (4.5:1) and UI/focus meet 3:1. White-on-orange surfaces move from `#FF6200` (3.00:1 with white) to the accessible `#C24E00` (4.79:1): primary buttons, the menu/header bars, and secondary/menu hover states. Primary-button hover uses the new `#A84300` (6.06:1); the input border darkens from `#D9D9D9` (1.41:1) to `#8C8C8C` (3.36:1); menu outline-button borders become solid white (4.79:1 on the darker bar); and disabled-button labels switch to charcoal for legibility. The bright `#FF6200` is kept for the login backdrop, the lion mark, and accent borders. (#6)
- Refreshed the screenshots (captured on a live Guacamole 1.6.0) and the GitHub Pages landing page to reflect the accessible palette, dark mode, and the configurable build.

### Removed

- The prebuilt `dist/guacamole-theme-orangelion.jar` is no longer committed and `dist/` is git-ignored. The canonical download is the CI-built asset on each tagged GitHub Release (with a SHA-256 checksum and a build-provenance attestation); build locally with `./build.sh` when working from source. The README documents the semantic-versioning policy. (#5)

## [1.2.0] - 2026-07-01

### Added

- Deployment guide (`docs/DEPLOYMENT.md`) covering Docker, Kubernetes (an initContainer that pulls the signed release, or a ConfigMap), and OpenShift (the restricted-SCC writable-HOME fix, a Route, and a BuildConfig alternative). Linked from the README, INSTRUCTIONS, and the landing page.
- A GitHub Pages landing site under `docs/`.

### Changed

- The login mark is now a lion emoji (a standard Unicode glyph) instead of the "OrangeLion" text wordmark. Screenshots updated to match.

## [1.1.0] - 2026-07-01

### Added

- Custom browser-tab favicon and app icon: an orange lion mark, set through the manifest `smallIcon` and `largeIcon` fields (`images/lion-64.png`, `images/lion-144.png`).
- Brand accent colour on native form controls (checkboxes, radio buttons, range inputs) via `accent-color`, replacing the browser default blue.
- Visible keyboard focus ring on interactive elements (WCAG 2.4.7), branded visited links, and disabled-button styling.
- Documentation: a README table of contents, live build, release, and downloads badges, copy-paste install commands with a success check, a CSS variable reference table with a recolor recipe, and an FAQ.
- Project health: a Code of Conduct, a Security policy, a pull request template, CODEOWNERS, and a go-to-market kit in `docs/promotion.md`.
- Continuous integration: a build workflow that lints (actionlint, shellcheck, stylelint) and smoke-tests the extension against Guacamole 1.5.5 and 1.6.0 with pinned action SHAs, plus a release job that publishes a SHA-256 checksum and a SLSA build-provenance attestation for the jar.

### Changed

- Text-sized orange now uses the darker `#C24E00` for links and outline-button labels, meeting WCAG AA contrast on white. The brighter `#FF6200` is retained for fills, borders, and the wordmark.

### Compatibility

- Tested on Guacamole 1.5.5 and 1.6.0.

## [1.0.0] - 2026-07-01

Initial public release of OrangeLion, an unofficial Apache Guacamole theme in the orange palette. This project is not affiliated with any organisation.

### Added

- orange (`#FF6200`) theme for Apache Guacamole, packaged as a drop-in CSS extension (`.jar`).
- Restyled login page: orange background, white login card, and an "OrangeLion" text wordmark (no trademarked lion image).
- Themed menu and header bars in the orange palette.
- Themed buttons across the interface.
- Themed connection list with orange header bars.
- Themed admin settings pages, including Settings > Users and Settings > Groups.
- Prebuilt extension at `dist/guacamole-theme-orangelion.jar`, ready to copy into `GUACAMOLE_HOME/extensions/`.
- `build.sh` build script that packs the extension into `dist/guacamole-theme-orangelion.jar`.
- `guac-manifest.json` with namespace `orangelion`, name "OrangeLion Theme", and CSS entry `orangelion.css`.
- `orangelion.css` containing the palette CSS variables plus login, button, menu, and connection list styling.
- Optional `translations/en.json.example` to override `APP.NAME` and rename the product on the login page.
- `INSTRUCTIONS.md` with a detailed install, customise, and uninstall guide.
- Screenshots of the login page, connection list, admin Users page, and admin Groups page.

### Compatibility

- `guacamoleVersion` set to `*`. Tested on Guacamole 1.5.5 and 1.6.0.

[Unreleased]: https://github.com/rupivbluegreen/orangelion-theme/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/rupivbluegreen/orangelion-theme/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/rupivbluegreen/orangelion-theme/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/rupivbluegreen/orangelion-theme/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/rupivbluegreen/orangelion-theme/releases/tag/v1.0.0
