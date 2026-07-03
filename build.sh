#!/usr/bin/env bash
# Package OrangeLion into a Guacamole extension jar
# (dist/guacamole-theme-orangelion.jar).
#
# A .jar is a .zip; the manifest + CSS (+ icons and any assets) are packed at
# the archive root. Re-run after editing the manifest, CSS, or configuration.
#
# With no configuration this reproduces the standard branded theme (identical
# rendering; the manifest byte-for-byte, the CSS apart from stripped build-time
# marker comments). Configure the build with environment variables or theme.config
# (see theme.config.example). Examples:
#
#   ./build.sh                                   # standard branded theme
#   VARIANT=neutral ./build.sh                   # palette only, no branding
#   BRAND_COLOR=#1565C0 ./build.sh               # recolour the whole theme
#   WORDMARK=Acme ./build.sh                      # custom login wordmark
#   LOGO=images/logo.svg ./build.sh              # logo image instead of the mark
#   APP_NAME="Acme Remote" LOCALES="en nl de" ./build.sh
#
# The build itself only requires python3; the logic lives in tools/build.py.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$here/tools/build.py" "$here" "$@"
