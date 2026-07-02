# Using OrangeLion with your own Guacamole deployment

A step by step guide to install and use the OrangeLion theme on any Apache
Guacamole instance. No web app rebuild is required. The theme is a standard
Guacamole CSS extension (a `.jar`) that Guacamole loads at startup.

## 1. What you need

1. A running Apache Guacamole (version 1.5.x or 1.6.x).
2. The theme jar: `dist/guacamole-theme-orangelion.jar` from this repo (already prebuilt), or
   run `./build.sh` to produce it yourself.
3. Write access to the Guacamole extensions directory, or the ability to set
   the `GUACAMOLE_HOME` environment variable if you run the Docker image.

## 2. Know where GUACAMOLE_HOME is

Guacamole loads every `.jar` it finds in `GUACAMOLE_HOME/extensions/`.
`GUACAMOLE_HOME` is usually one of:

1. `/etc/guacamole` (common for war or Tomcat installs)
2. `~/.guacamole` (the home directory of the user running Tomcat)
3. Whatever you set the `GUACAMOLE_HOME` environment variable to

## 3. Install (choose the option that matches your setup)

### Option A: standard install (war on Tomcat, or a package install)

1. Copy the jar into the extensions directory:
   ```bash
   mkdir -p "$GUACAMOLE_HOME/extensions"
   cp dist/guacamole-theme-orangelion.jar "$GUACAMOLE_HOME/extensions/"
   ```
2. Restart Guacamole (for example, restart Tomcat).
3. Open the portal and hard refresh the browser (Ctrl+Shift+R) to clear cached
   CSS.

### Option B: official `guacamole/guacamole` Docker image

The image treats the `GUACAMOLE_HOME` environment variable as a template that it
copies into the live home on startup, next to auto installed extensions such as
LDAP or the database. Put the jar in a folder and point at it:

1. Create the folder layout on the host:
   ```bash
   mkdir -p guac-home/extensions
   cp dist/guacamole-theme-orangelion.jar guac-home/extensions/
   ```
2. Add the mount and the environment variable to your compose service:
   ```yaml
   services:
     guacamole:
       image: guacamole/guacamole:1.6.0
       environment:
         GUACAMOLE_HOME: /guac-home
         # keep your existing GUACD_HOSTNAME, database, and auth variables
       volumes:
         - ./guac-home:/guac-home:ro
   ```
3. Recreate the container:
   ```bash
   docker compose up -d --force-recreate guacamole
   ```

For orchestrated platforms (Kubernetes and OpenShift), including the OpenShift
restricted-SCC notes and ready-to-adapt manifests, see
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## 4. Verify it loaded

1. Check the logs for the load line:
   ```bash
   docker compose logs guacamole | grep "OrangeLion"
   ```
   You should see: `Extension "OrangeLion Theme" (orangelion) loaded.`
2. Open the login page. It should show the orange background, a white card, and
   the lion emoji mark.

## 5. Customize with build options (recommended)

You can restyle OrangeLion without editing any CSS. `build.sh` reads options
from environment variables, or from a `theme.config` file of `KEY=VALUE` lines
(copy `theme.config.example` to `theme.config`). Environment variables win over
the file, and with no options set `./build.sh` reproduces the standard theme
byte for byte.

| Option | Default | Effect |
| --- | --- | --- |
| `VARIANT` | `branded` | `branded` = palette + lion login mark + icons. `neutral` = palette only (see below). |
| `BRAND_COLOR` | `#FF6200` | Primary accent. The darker shades are derived from it automatically. |
| `BRAND_COLOR_DARK` | derived | Hover / darker fill shade. |
| `BRAND_COLOR_DARKER` | derived | Accessible text orange (links, outline-button labels). |
| `WORDMARK` | lion emoji | Text or emoji shown on the white login card. |
| `LOGO` | — | Path to an SVG/PNG shown instead of the wordmark (see below). |
| `APP_NAME` | — | Product name on the login page / browser tab (branded builds only). |
| `LOCALES` | `en` | Space-separated locales that `APP_NAME` is written into. |
| `OUTPUT` | `dist/…jar` | Output jar path. |

Examples:

```bash
./build.sh                                    # standard branded theme
BRAND_COLOR=#1565C0 ./build.sh                # recolour everything to blue
WORDMARK="Acme Remote" ./build.sh             # custom login wordmark
APP_NAME="Acme Remote" LOCALES="en nl de" ./build.sh
```

### Theme-only (neutral) build

`VARIANT=neutral ./build.sh` produces `dist/guacamole-theme-orangelion-neutral.jar`:
just the colour palette, with **no** OrangeLion login mark, product-name
override, or bundled icons, so Guacamole keeps its own logo and product name.
Pick this if you want the restyle but not the branding. (OrangeLion is an
unofficial, community-maintained theme, unaffiliated with Apache Guacamole,
either way.)

### Logo image instead of the wordmark

Set `LOGO` to an SVG or PNG to render a real logo, centred on the login card, in
place of the wordmark text/emoji:

```bash
LOGO=images/my-logo.svg ./build.sh
```

The image is packed into the jar and exposed as a manifest resource, and the
wordmark text is hidden. Use only artwork you have the right to use; do not ship
trademarked logos.

### More languages for the product name

`APP_NAME` sets the product name shown on the login page and browser tab. By
default it is written for English only; list more locales in `LOCALES` (using
the Guacamole locale codes, for example `en`, `nl`, `de`, `fr`) so users whose
browser is set to another language see the override too:

```bash
APP_NAME="Acme Remote" LOCALES="en nl de fr" ./build.sh
```

To ship a *different* name per language, copy the example locale files
(`translations/en.json.example`, `translations/nl.json.example`,
`translations/de.json.example`) to `translations/<locale>.json`, edit each
`APP.NAME`, then run `./build.sh` (without `APP_NAME`). The build packs every
`translations/<locale>.json` it finds and lists them in the manifest.

### Dark mode (automatic)

OrangeLion ships a dark variant that turns on by itself when the operating system
or browser is set to a dark colour scheme (a `@media (prefers-color-scheme: dark)`
block in `orangelion.css`) — there is no toggle to flip. It uses dark page and
card backgrounds, light text, and orange shades tuned for dark surfaces, all
meeting WCAG AA (see [docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md#dark-theme-prefers-color-scheme-dark)).

To preview it: switch your OS appearance to Dark and reload, or use your
browser's dev tools (Chromium: Rendering panel → *Emulate CSS media feature
prefers-color-scheme: dark*). A custom `BRAND_COLOR` recolours the light theme
only; edit the dark `@media` block if you want to recolour dark mode too.

### Editing the CSS directly

You can still hand-edit `orangelion.css` — the colours are CSS variables in the
`:root` block at the top — then rebuild. Build options are a convenience layer
over the same stylesheet.

## 6. Rebuild and reinstall after any change

1. Rebuild the jar:
   ```bash
   ./build.sh
   ```
2. Reinstall it using the same option you used in step 3, then restart or
   force recreate Guacamole and hard refresh the browser.

## 7. Uninstall

1. Remove the jar:
   ```bash
   rm "$GUACAMOLE_HOME/extensions/guacamole-theme-orangelion.jar"
   ```
   For the Docker image, remove it from `guac-home/extensions/` instead.
2. Restart or force recreate Guacamole. The default theme returns.

## Troubleshooting

1. Theme does not appear: confirm the jar is in `GUACAMOLE_HOME/extensions/` and
   that the logs show the "OrangeLion Theme loaded" line.
2. Old colors still show: the browser cached the CSS. Hard refresh, or restart
   the container so a fresh aggregated stylesheet is served.
3. Wrong GUACAMOLE_HOME: the Docker image rebuilds its home on every start, so
   use the `GUACAMOLE_HOME` template method in Option B rather than writing into
   a running container.
