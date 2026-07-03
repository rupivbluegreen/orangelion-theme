#!/usr/bin/env python3
"""Build the OrangeLion Guacamole theme extension jar.

Invoked by ``build.sh``. Reads configuration from a ``theme.config`` file
(KEY=VALUE lines) and from environment variables (environment wins), then packs
a ``.jar`` (a ``.zip``) containing the manifest, the optionally-templated CSS,
icons, and any assets, at the archive root.

Design invariant: with no configuration the default build reproduces the
standard branded theme exactly. ``guac-manifest.json`` is byte-for-byte
identical to the committed source; ``orangelion.css`` is identical apart from
the build-time ``/* @orangelion:... */`` marker comments, which are stripped
(nothing that renders changes).

Configuration keys (all optional):

  VARIANT             ``branded`` (default) or ``neutral``. Neutral is palette
                      only: it drops the login mark, the product-name override,
                      and the bundled icons, so Guacamole keeps its own logo and
                      name (issue #9).
  BRAND_COLOR         primary accent hex           (default #FF6200)
  BRAND_COLOR_DARK    hover / darker fill hex      (default #E15700, derived
                      from BRAND_COLOR when only BRAND_COLOR is set)
  BRAND_COLOR_DARKER  accessible text orange hex   (default #C24E00, derived)
  WORDMARK            login-mark text or emoji     (default: the lion emoji in
                      orangelion.css) (issue #1)
  LOGO                path to an SVG/PNG logo image shown instead of the mark;
                      packed into the jar and exposed as a manifest resource
                      (issue #2)
  APP_NAME            product name on the login page / browser tab; written into
                      a translation override for each locale in LOCALES
                      (branded builds only) (issue #8)
  LOCALES             space-separated locales for APP_NAME   (default "en")
  OUTPUT              output jar path
"""

import argparse
import colorsys
import json
import os
import re
import sys
import zipfile

DEFAULTS = {
    "VARIANT": "branded",
    "BRAND_COLOR": "#FF6200",
    "BRAND_COLOR_DARK": "#E15700",
    "BRAND_COLOR_DARKER": "#C24E00",
    "WORDMARK": "",
    "LOGO": "",
    "APP_NAME": "",
    "LOCALES": "en",
    "OUTPUT": "",
}

VARIANT_CHOICES = ("branded", "neutral", "theme-only", "theme")
NEUTRAL_VARIANTS = ("neutral", "theme-only", "theme")
NEUTRAL_IGNORED_KEYS = ("WORDMARK", "LOGO", "APP_NAME", "LOCALES")
LOCALE_TOKEN = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")

OPTION_REFERENCE = """Configuration keys (theme.config or environment):
  VARIANT             branded (default) or neutral. theme-only/theme are
                      accepted aliases for neutral.
  BRAND_COLOR         primary accent hex (default #FF6200)
  BRAND_COLOR_DARK    hover / darker fill hex (default #E15700, derived
                      from BRAND_COLOR when only BRAND_COLOR is set)
  BRAND_COLOR_DARKER  accessible text orange hex (default #C24E00, derived)
  WORDMARK            login-mark text or emoji (branded builds only)
  LOGO                SVG/PNG logo path (branded builds only)
  APP_NAME            product name translation override (branded builds only)
  LOCALES             space-separated locales for APP_NAME (default "en")
  OUTPUT              output jar path
"""

# Literal brand values that live outside the CSS variables and so are recoloured
# by hand when a custom palette is requested.
BASE_PRIMARY = "#FF6200"
GRADIENT_TINTS = ["#FF7A2E", "#FF8C42"]   # lighter login-backdrop stops
DISABLED_TINTS = ["#F2B48A", "#E0A070"]   # muted disabled-button fill / border

MIME = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}

MARKER_START = "/* @orangelion:branding-start */"
MARKER_END = "/* @orangelion:branding-end */"
MARKER_DARK = "/* @orangelion:darkmode */"

LOGO_CSS = """
/* Configured logo image (build option: LOGO). Overrides the login mark. */
.login-ui .login-dialog .logo {{
    background-image: url("{url}") !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: contain !important;
    width: 220px !important;
    height: 96px !important;
    max-width: 80% !important;
}}

.login-ui .login-dialog .logo::after {{
    content: "" !important;
}}
"""


def load_config(root):
    cfg = dict(DEFAULTS)
    provided = set()
    path = os.path.join(root, "theme.config")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key in cfg:
                    cfg[key] = val
                    provided.add(key)
    for key in cfg:
        env = os.environ.get(key)
        if env:
            cfg[key] = env
            provided.add(key)
    # Normalise and validate colour options: empty means "use the default",
    # anything else must be a #RGB / #RRGGBB hex value (this also rejects
    # trailing junk such as an inline comment).
    for key in ("BRAND_COLOR", "BRAND_COLOR_DARK", "BRAND_COLOR_DARKER"):
        val = cfg[key].strip()
        if not val:
            cfg[key] = DEFAULTS[key]
        elif re.fullmatch(r"#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})", val):
            cfg[key] = val
        else:
            sys.exit("build: invalid {} {!r} (expected a hex colour like "
                     "#FF6200)".format(key, cfg[key]))
    validate_config(cfg, provided)
    return cfg, provided


def validate_config(cfg, provided):
    variant = cfg["VARIANT"].strip().lower() or DEFAULTS["VARIANT"]
    if variant not in VARIANT_CHOICES:
        sys.exit("build: invalid VARIANT {!r} (expected one of: {})".format(
            cfg["VARIANT"], ", ".join(VARIANT_CHOICES)))
    cfg["VARIANT"] = "neutral" if variant in NEUTRAL_VARIANTS else "branded"

    locale_tokens(cfg)
    if cfg["APP_NAME"] and not cfg["LOCALES"].split():
        sys.exit("build: LOCALES must include at least one locale when "
                 "APP_NAME is set")

    if is_neutral(cfg):
        for key in NEUTRAL_IGNORED_KEYS:
            if key in provided and cfg[key].strip():
                print("build: warning: {} is ignored when VARIANT=neutral".format(key),
                      file=sys.stderr)


def is_neutral(cfg):
    return cfg["VARIANT"] == "neutral"


def locale_tokens(cfg):
    tokens = cfg["LOCALES"].split()
    bad = [loc for loc in tokens if not LOCALE_TOKEN.fullmatch(loc)]
    if bad:
        sys.exit("build: invalid LOCALES token {!r} (expected values like "
                 "en, en-US, or pt_BR)".format(bad[0]))
    return tokens


# --------------------------------------------------------------- colour maths --

def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _hls(value):
    r, g, b = (c / 255 for c in hex_to_rgb(value))
    return colorsys.rgb_to_hls(r, g, b)


def _hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, min(1.0, max(0.0, l)), min(1.0, max(0.0, s)))
    return "#{:02X}{:02X}{:02X}".format(round(r * 255), round(g * 255), round(b * 255))


def derive(original, new_base, old_base=BASE_PRIMARY):
    """Re-express ``original`` (defined relative to ``old_base``) relative to
    ``new_base``, preserving its hue/lightness/saturation offsets. Used to keep
    the gradient and disabled tints coherent when the brand colour changes."""
    ho, lo, so = _hls(original)
    hb, lb, sb = _hls(old_base)
    hn, ln, sn = _hls(new_base)
    return _hex(hn + (ho - hb), ln + (lo - lb), sn + (so - sb))


# ------------------------------------------------------------------------- CSS --

def strip_markers(lines):
    return [ln for ln in lines if ln.strip() not in (MARKER_START, MARKER_END)]


def drop_branding(lines):
    out, skipping = [], False
    for ln in lines:
        stripped = ln.strip()
        if stripped == MARKER_START:
            skipping = True
            continue
        if stripped == MARKER_END:
            skipping = False
            continue
        if not skipping:
            out.append(ln)
    return out


def css_escape(text):
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return text.replace("\r", " ").replace("\n", " ")


def _recolour(css, prim, dark, darker):
    """Apply the palette substitutions to a chunk of CSS (the light theme)."""
    css = re.sub(r"(--brand-orange:\s*)#[0-9A-Fa-f]{3,8}(;)",
                 lambda m: m.group(1) + prim + m.group(2), css)
    css = re.sub(r"(--brand-orange-dark:\s*)#[0-9A-Fa-f]{3,8}(;)",
                 lambda m: m.group(1) + dark + m.group(2), css)
    css = re.sub(r"(--brand-orange-darker:\s*)#[0-9A-Fa-f]{3,8}(;)",
                 lambda m: m.group(1) + darker + m.group(2), css)
    # The deep hover shade has no env knob; derive it from the primary.
    css = re.sub(r"(--brand-orange-deep:\s*)#[0-9A-Fa-f]{3,8}(;)",
                 lambda m: m.group(1) + derive("#A84300", prim) + m.group(2), css)
    # Literal accents not behind the variables.
    css = re.sub(r"#FF6200\b", prim, css, flags=re.IGNORECASE)
    r, g, b = hex_to_rgb(prim)
    css = re.sub(r"rgba\(\s*255\s*,\s*98\s*,\s*0\s*,",
                 "rgba({}, {}, {},".format(r, g, b), css)
    for orig in GRADIENT_TINTS + DISABLED_TINTS:
        css = re.sub(re.escape(orig), derive(orig, prim), css, flags=re.IGNORECASE)
    return css


def transform_css(root, cfg):
    """Return (css_text, logo_asset) where logo_asset is (src_path, arcname) or
    None. With no overrides css_text equals the committed CSS with the
    build-time marker comments removed (rendering is unchanged)."""
    with open(os.path.join(root, "orangelion.css"), encoding="utf-8") as fh:
        lines = fh.readlines()

    neutral = is_neutral(cfg)
    lines = drop_branding(lines) if neutral else strip_markers(lines)
    css = "".join(lines)
    if neutral:
        css = re.sub(r"\n{3,}", "\n\n", css)

    default = {k: DEFAULTS[k].upper() for k in
               ("BRAND_COLOR", "BRAND_COLOR_DARK", "BRAND_COLOR_DARKER")}
    given = {k: cfg[k].upper() for k in default}
    recolor = any(given[k] != default[k] for k in default)

    if recolor:
        prim = cfg["BRAND_COLOR"]
        dark = (cfg["BRAND_COLOR_DARK"]
                if given["BRAND_COLOR_DARK"] != default["BRAND_COLOR_DARK"]
                else derive(DEFAULTS["BRAND_COLOR_DARK"], prim))
        darker = (cfg["BRAND_COLOR_DARKER"]
                  if given["BRAND_COLOR_DARKER"] != default["BRAND_COLOR_DARKER"]
                  else derive(DEFAULTS["BRAND_COLOR_DARKER"], prim))
        # Recolour only the light theme; the dark-mode block after the marker is
        # tuned for dark surfaces, so it is left as-is.
        head, sep, tail = css.partition(MARKER_DARK)
        css = _recolour(head, prim, dark, darker) + sep + tail

    # The dark-mode marker is a build-time comment; strip it from every jar.
    css = re.sub(r"[ \t]*" + re.escape(MARKER_DARK) + r"\n?", "", css)

    logo_asset = None
    if cfg["LOGO"] and not neutral:
        logo_path = cfg["LOGO"]
        if not os.path.isabs(logo_path):
            logo_path = os.path.join(root, logo_path)
        if not os.path.exists(logo_path):
            sys.exit("build: LOGO not found: {}".format(cfg["LOGO"]))
        arc = "images/" + os.path.basename(logo_path)
        logo_asset = (logo_path, arc)
        css += LOGO_CSS.format(url=arc)
    elif cfg["WORDMARK"] and not neutral:
        # Use a function replacement so re.sub does not re-process backslashes
        # in the (already CSS-escaped) wordmark.
        mark = 'content: "' + css_escape(cfg["WORDMARK"]) + '";'
        css = re.sub(r'content:\s*"\\1F981";', lambda _: mark, css, count=1)

    return css, logo_asset


# -------------------------------------------------------------- translations --

def build_translations(root, cfg):
    """Return a list of (arcname, bytes) locale files. Empty for the default
    (byte-for-byte) build and for neutral builds."""
    if is_neutral(cfg):
        return []
    files, seen = [], set()
    if cfg["APP_NAME"]:
        payload = {"APP": {"NAME": cfg["APP_NAME"]}}
        blob = (json.dumps(payload, indent=4, ensure_ascii=False) + "\n").encode("utf-8")
        for loc in dict.fromkeys(locale_tokens(cfg)):
            arc = "translations/{}.json".format(loc)
            files.append((arc, blob))
            seen.add(arc)
    tdir = os.path.join(root, "translations")
    if os.path.isdir(tdir):
        for name in sorted(os.listdir(tdir)):
            if not name.endswith(".json") or name.endswith(".example"):
                continue
            arc = "translations/{}".format(name)
            if arc in seen:
                continue
            with open(os.path.join(tdir, name), "rb") as fh:
                files.append((arc, fh.read()))
            seen.add(arc)
    return files


# ------------------------------------------------------------------ manifest --

def build_manifest(root, cfg, translation_arcs, logo_arc):
    """Return manifest text. When nothing is added it is the committed manifest
    verbatim, preserving byte-for-byte output."""
    with open(os.path.join(root, "guac-manifest.json"), encoding="utf-8") as fh:
        raw = fh.read()
    data = json.loads(raw)
    modified = False

    if is_neutral(cfg):
        for key in ("smallIcon", "largeIcon"):
            if key in data:
                del data[key]
                modified = True
    if translation_arcs:
        data["translations"] = translation_arcs
        modified = True
    if logo_arc:
        resources = data.get("resources", {})
        ext = os.path.splitext(logo_arc)[1].lower()
        resources[logo_arc] = MIME.get(ext, "application/octet-stream")
        data["resources"] = resources
        modified = True

    if not modified:
        return raw
    return json.dumps(data, indent=4) + "\n"


# ---------------------------------------------------------------------- main --

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Build the OrangeLion Guacamole theme extension jar.",
        epilog=OPTION_REFERENCE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    default_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    parser.add_argument(
        "root",
        nargs="?",
        default=default_root,
        help="repository root containing guac-manifest.json and orangelion.css",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print resolved config, output path, and archive entries without writing a jar",
    )
    return parser.parse_args(argv)


def resolve_output(root, cfg, neutral):
    out = cfg["OUTPUT"]
    if not out:
        name = ("guacamole-theme-orangelion-neutral.jar" if neutral
                else "guacamole-theme-orangelion.jar")
        out = os.path.join(root, "dist", name)
    if not os.path.isabs(out):
        out = os.path.join(root, out)
    return out


def build_plan(root, cfg):
    neutral = is_neutral(cfg)

    css_text, logo_asset = transform_css(root, cfg)
    translations = build_translations(root, cfg)
    logo_arc = logo_asset[1] if logo_asset else None
    manifest_text = build_manifest(root, cfg, [t[0] for t in translations], logo_arc)

    out = resolve_output(root, cfg, neutral)
    packed = ["guac-manifest.json", "orangelion.css"]
    if not neutral:
        packed.extend(["images/lion-64.png", "images/lion-144.png"])
    if logo_asset:
        packed.append(logo_asset[1])
    packed.extend(arc for arc, _ in translations)

    return {
        "root": root,
        "out": out,
        "neutral": neutral,
        "css_text": css_text,
        "logo_asset": logo_asset,
        "translations": translations,
        "manifest_text": manifest_text,
        "packed": packed,
    }


def print_dry_run(plan, cfg):
    print("dry-run: no jar written")
    print("root: {}".format(plan["root"]))
    print("output: {}".format(plan["out"]))
    print("resolved config:")
    for key in DEFAULTS:
        print("  {}={}".format(key, json.dumps(cfg[key], ensure_ascii=False)))
    print("archive entries:")
    for name in plan["packed"]:
        print("  {}".format(name))


def write_archive(plan):
    root = plan["root"]
    out = plan["out"]
    neutral = plan["neutral"]
    logo_asset = plan["logo_asset"]
    translations = plan["translations"]

    os.makedirs(os.path.dirname(out), exist_ok=True)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("guac-manifest.json", plan["manifest_text"])
        z.writestr("orangelion.css", plan["css_text"])
        if not neutral:
            for img in ("images/lion-64.png", "images/lion-144.png"):
                z.write(os.path.join(root, img), img)
        if logo_asset:
            z.write(logo_asset[0], logo_asset[1])
        for arc, blob in translations:
            z.writestr(arc, blob)

    print("built {} [{}] with {}".format(out, "neutral" if neutral else "branded",
                                          plan["packed"]))


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = os.path.abspath(args.root)
    cfg, _provided = load_config(root)
    plan = build_plan(root, cfg)
    if args.dry_run:
        print_dry_run(plan, cfg)
        return
    write_archive(plan)


if __name__ == "__main__":
    main()
