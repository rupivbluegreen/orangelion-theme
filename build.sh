#!/usr/bin/env bash
# Package OrangeLion into a Guacamole extension jar (dist/orangelion.jar).
# A .jar is a .zip; the manifest + CSS are packed at the archive root.
# Re-run after editing the manifest or CSS.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
jar="$here/dist/orangelion.jar"
mkdir -p "$here/dist"

python3 - "$here" "$jar" <<'PY'
import sys, zipfile, os
src, jar = sys.argv[1], sys.argv[2]
files = ["guac-manifest.json", "orangelion.css"]
# Include an optional translation override only if the real file exists
if os.path.exists(os.path.join(src, "translations", "en.json")):
    files.append("translations/en.json")
with zipfile.ZipFile(jar, "w", zipfile.ZIP_DEFLATED) as z:
    for name in files:
        z.write(os.path.join(src, name), name)
print("built", jar, "with", files)
PY
