# Contributing to OrangeLion

Thanks for your interest in improving OrangeLion, an unofficial Apache Guacamole theme that restyles the interface into the orange palette. This project is community maintained and is not affiliated with any organisation.

This guide is intentionally short and practical. Please read it before opening an issue or a pull request.

## Prerequisites

- `python3` (used by `build.sh` to pack the extension archive)
- A running Apache Guacamole instance for local testing (1.5.5 and 1.6.0 are known good)
- A text editor and basic familiarity with CSS

## Building

The build script packs the theme into a distributable `.jar`:

```bash
./build.sh
```

This produces `dist/guacamole-theme-orangelion.jar`. The script only requires `python3`, so there is no toolchain to install. If the script is not executable, run `chmod +x build.sh` first.

## Testing locally

1. Build the jar (see above), or use the prebuilt `dist/guacamole-theme-orangelion.jar`.
2. Install it in one of two ways:
   - Copy the jar into your `GUACAMOLE_HOME/extensions/` directory.
   - For the official Docker image, mount a folder that contains `extensions/guacamole-theme-orangelion.jar` and set `GUACAMOLE_HOME` to that folder.
3. Restart Guacamole.
4. Hard refresh your browser (Ctrl+Shift+R, or Cmd+Shift+R on macOS) to clear cached CSS.
5. Confirm the theme loaded by checking the Guacamole log for this line:

   ```
   Extension "OrangeLion Theme" (orangelion) loaded.
   ```

If you do not see the log line, the extension was not picked up. Check that the jar is in the extensions directory and that `GUACAMOLE_HOME` points where you expect.

## Project layout

| Path | Purpose |
| --- | --- |
| `guac-manifest.json` | Extension manifest (namespace `orangelion`, name, css entry) |
| `orangelion.css` | Palette variables and all login, button, menu, and connection-list styling |
| `build.sh` | Packs the jar into `dist/guacamole-theme-orangelion.jar` |
| `dist/guacamole-theme-orangelion.jar` | Prebuilt extension, ready to drop in |
| `translations/en.json.example` | Optional `APP.NAME` override to rename the product on the login page |
| `INSTRUCTIONS.md` | Detailed install, customise, and uninstall guide |
| `screenshots/` | Reference images of the themed pages |

## Coding and style conventions

- Define colours as CSS variables near the top of `orangelion.css`, then reference them. The main brand colour is orange (`#FF6200`). Do not hard-code the same colour value in multiple places.
- Keep selectors specific so the theme targets the intended elements and does not leak into unrelated parts of the interface.
- Prefer not to use `!important`. Reach for it only where it is genuinely needed to beat the bundled Guacamole theme, and keep those cases to a minimum.
- Match the existing formatting and grouping in the CSS so related rules stay together.
- Do not add trademarked assets. The login mark is a Unicode lion emoji, not a logo image.

## Proposing changes

- For anything larger than a small fix, open an issue first so the change can be discussed before you spend time on it.
- For small, self-contained fixes, a pull request on its own is fine.
- Keep pull requests focused on a single change. Smaller diffs are easier to review.
- Test your change locally and confirm the load log line before submitting.

## Commit messages

- Write a short, clear summary line in the imperative mood, for example "Fix header contrast on the connection list".
- Keep the summary under about 72 characters.
- Add a body when the change needs context, explaining what changed and why.

## Screenshots

When your change affects the appearance of any page, update the relevant images in `screenshots/` (`login.png`, `connections.png`, `users.png`, `groups.png`) so they reflect the current look. Mention in the pull request which screenshots you updated.

## Licence

By contributing, you agree that your contributions are licensed under the MIT Licence, the same licence that covers this project.
