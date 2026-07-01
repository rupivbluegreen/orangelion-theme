# Promotion kit

Ready-to-post copy for announcing OrangeLion. Each section below is self-contained and copy-paste ready. Everything here is factual: OrangeLion is an unofficial, community-maintained CSS theme extension for Apache Guacamole, released under the MIT License, and tested on Guacamole 1.5.5 and 1.6.0. Please do not add metrics or endorsements that are not true.

Reference links used throughout:

- Repository: https://github.com/rupivbluegreen/orangelion-theme
- Latest release: https://github.com/rupivbluegreen/orangelion-theme/releases/latest
- v1.0.0 release: https://github.com/rupivbluegreen/orangelion-theme/releases/tag/v1.0.0

---

## 1. Awesome list / index entry

A single markdown bullet suitable for an awesome-guacamole, awesome-selfhosted, or similar curated index. Copy the one line below:

```markdown
- [OrangeLion](https://github.com/rupivbluegreen/orangelion-theme) - Drop-in orange CSS theme extension for Apache Guacamole, packaged as a single `.jar`. MIT, unofficial and unaffiliated.
```

---

## 2. Pull request body

Use this when submitting the entry above to an external curated list. It is short, polite, and explains what OrangeLion is and why it fits.

```markdown
### What this adds

This PR adds OrangeLion to the list.

**OrangeLion** is a drop-in orange CSS theme extension for Apache Guacamole. It repaints the login page, menus, header bars, buttons, connection list, and admin settings screens in an orange palette. It ships as a single `.jar` that you copy into your Guacamole extensions folder, so it layers on top of an existing install with no web-app rebuild and no source changes.

- Repository: https://github.com/rupivbluegreen/orangelion-theme
- License: MIT
- Tested on Guacamole 1.5.5 and 1.6.0
- Status: unofficial, community-maintained, and not affiliated with any organisation

### Why it fits

It is a small, self-hosted-friendly, open-source add-on for a tool that this list already covers, and it fills a gap that many self-hosters ask about: a simple way to reskin the Guacamole interface without patching the web app. The entry follows the existing formatting (name, one-line description, link).

Thanks for maintaining this list, and for taking a look.
```

---

## 3. Launch announcement

Suitable for the Guacamole user mailing list, r/selfhosted, and r/Guacamole. Copy the title and body below. The body is plain text so it pastes cleanly into a mailing list message or a Reddit post.

**Title:**

```
OrangeLion: a drop-in orange CSS theme for Apache Guacamole (unofficial, MIT)
```

**Body:**

```
I put together OrangeLion, a small CSS-only theme extension that gives Apache Guacamole an orange colour scheme.

What it does: it repaints the login page, menus, header bars, buttons, the connection list, and the admin settings screens (Users, Groups, and more) in an orange palette. The login page uses a lion emoji mark rather than any trademarked logo.

How it installs: it is a single drop-in .jar. You copy guacamole-theme-orangelion.jar into your GUACAMOLE_HOME/extensions/ folder, restart Guacamole, and hard refresh the browser. There is no web-app rebuild and no change to the Guacamole source. It deploys the same way on Docker, Kubernetes, and OpenShift, with ready-to-adapt manifests in the deployment guide. The palette and wordmark are configurable through CSS variables at the top of the stylesheet, and you can optionally rename the product on the login page with a translation override.

Compatibility: the extension manifest declares a version of "*", and I have tested the theme on Guacamole 1.5.5 and 1.6.0.

Licence and status: MIT. This is an unofficial, community-maintained project and is not affiliated with any organisation. Feedback, issues, and pull requests are all welcome.

Repository: https://github.com/rupivbluegreen/orangelion-theme
Latest release: https://github.com/rupivbluegreen/orangelion-theme/releases/latest
v1.0.0: https://github.com/rupivbluegreen/orangelion-theme/releases/tag/v1.0.0
```
