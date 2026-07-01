# Security Policy

## Scope

OrangeLion is an unofficial, community-maintained CSS theme extension for Apache Guacamole.
It ships only a stylesheet (CSS) and a small extension manifest. It contains no server code,
no scripts, and no build-time execution beyond packaging the assets into a JAR.

Because of this, the realistic risk surface is limited to CSS or UI rendering issues, for
example styling that could obscure controls, reduce readability, or otherwise affect how the
Guacamole web interface is presented. The theme cannot access credentials, sessions, or
server-side data, and it does not add any network behavior.

## Supported versions

Security fixes are provided for the latest released version only. The current supported
line is 1.0.x, which receives fixes. Older releases and unreleased or pre-release builds
do not receive backported fixes.

| Version            | Supported          |
| ------------------ | ------------------ |
| 1.0.x              | Yes                |
| Older than 1.0.x   | No                 |
| Unreleased / pre-release | No           |

## Reporting a vulnerability

Please report suspected security issues privately using GitHub's private vulnerability
reporting:

1. Go to the repository's **Security** tab.
2. Select **Report a vulnerability**.
3. Provide a clear description, affected version, and steps to reproduce.

Please do not open a public issue for sensitive reports, as this can expose the problem
before a fix is available. Public issues are fine for general, non-sensitive questions.

GitHub's private vulnerability reporting (the repository **Security** tab, **Report a
vulnerability**) is the sole channel for reporting security issues. There is no separate
email or other intake. Do not open a public issue for sensitive reports; use the private
reporting flow above so the problem is not exposed before a fix is available.

## Response expectations

This is a small, community-maintained project, so responses are made on a best-effort basis
by volunteers. We aim to acknowledge a valid report within a reasonable time, confirm whether
it is in scope, and, if a fix is warranted, address it in the latest release. Timelines are
not guaranteed and may vary with maintainer availability.

Thank you for helping keep the project and its users safe.
