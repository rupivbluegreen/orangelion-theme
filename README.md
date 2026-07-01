<div align="center">

<h1>🦁</h1>

<h1>OrangeLion</h1>

**A drop-in orange theme for Apache Guacamole**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Guacamole](https://img.shields.io/badge/Guacamole-1.5.x%20%7C%201.6.x-blue.svg)](https://guacamole.apache.org/)
[![extension](https://img.shields.io/badge/extension-CSS%20theme-orange.svg)](guac-manifest.json)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

OrangeLion is a CSS-only theme extension for Apache Guacamole. It repaints the login page, menus, header bars, buttons, connection list, and admin settings screens in the orange colour scheme, using a plain "OrangeLion" text wordmark instead of any trademarked logo. It ships as a single `.jar` that you drop into your Guacamole extensions folder, so it layers on top of any install without rebuilding the web app. This project is unofficial and community-maintained.

## Screenshots

| Login | Connections |
| --- | --- |
| ![Login page: orange background, white card, OrangeLion wordmark](screenshots/login.png) | ![Connection list with orange header bars](screenshots/connections.png) |

| Admin: Users | Admin: Groups |
| --- | --- |
| ![Admin Settings, Users page, fully themed](screenshots/users.png) | ![Admin Settings, Groups page, fully themed](screenshots/groups.png) |

## Features

- orange (`#FF6200`) colour palette applied across the interface.
- White login card with a clean "OrangeLion" text wordmark (no trademarked lion image).
- Themed menu, header bars, and buttons.
- Themed connection list and admin settings pages (Users, Groups, and more).
- Single-file, drop-in extension: just copy one `.jar`.
- No web-app rebuild and no source changes to Guacamole.
- Configurable through CSS variables at the top of the stylesheet.
- Optional product-name rename on the login page via a translation override.

## Install

Download the latest `guacamole-theme-orangelion.jar` from the [Releases](https://github.com/rupivbluegreen/orangelion-theme/releases) page, or use the prebuilt copy in `dist/` in this repo.

Quick version:

1. Copy `guacamole-theme-orangelion.jar` into `GUACAMOLE_HOME/extensions/`.
2. Restart Guacamole.
3. Hard refresh your browser (Ctrl+Shift+R, or Cmd+Shift+R on macOS) to clear cached CSS.

Docker note: with the official Guacamole image, mount a folder that contains `extensions/guacamole-theme-orangelion.jar` and set the `GUACAMOLE_HOME` environment variable to point at that folder, then restart the container.

For full step-by-step instructions, customisation options, and uninstall steps, see [INSTRUCTIONS.md](INSTRUCTIONS.md).

## Customize

- Palette: edit the CSS variables at the top of `orangelion.css` to adjust colours (for example the orange value) without touching the rest of the stylesheet.
- Wordmark: change the "OrangeLion" text wordmark in `orangelion.css` to your own label, or point it at a background image.
- Product name: optionally rename the product shown on the login page by supplying an `APP.NAME` override. See `translations/en.json.example` for the format.

After any change, rebuild the jar with `build.sh` (output: `dist/guacamole-theme-orangelion.jar`), then reinstall and hard refresh.

## Compatibility

The manifest declares `guacamoleVersion` `"*"`, and the theme has been tested on Guacamole 1.5.5 and 1.6.0.

## Roadmap

Planned improvements are tracked as [issues](https://github.com/rupivbluegreen/orangelion-theme/issues). Highlights include a configurable brand colour and wordmark, optional SVG logo support, a dark-mode variant, CI-built tagged releases, a WCAG contrast audit, and a documented Guacamole version compatibility matrix. Contributions toward any of these are welcome.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), then open an issue or a pull request with your ideas, fixes, or improvements. This project also follows a [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Released under the MIT License. See [LICENSE](LICENSE).
