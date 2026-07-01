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

## 5. Customize (optional)

All colors are CSS variables at the top of `orangelion.css`:

1. Edit the palette, for example `--brand-orange: #FF6200;`.
2. Change the login wordmark by editing the `.login-ui .login-dialog .logo::after`
   rule (the `content` value, currently a lion emoji), or point `.logo` at a real image.
3. Rename the product on the login page and browser tab: copy
   `translations/en.json.example` to `translations/en.json`, edit `APP.NAME`,
   and rebuild. The build script includes that file automatically when present.

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
