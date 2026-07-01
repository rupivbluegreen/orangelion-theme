# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet. Planned changes will be listed here before the next release.

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

[Unreleased]: https://github.com/rupivbluegreen/orangelion-theme/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/rupivbluegreen/orangelion-theme/releases/tag/v1.0.0
