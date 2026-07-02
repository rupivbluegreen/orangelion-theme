# Accessibility: WCAG contrast audit

OrangeLion targets [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) contrast:
normal-size text at **4.5:1** and UI components, borders, and focus indicators
at **3:1**. Every foreground/background pair actually used in `orangelion.css`
is listed below with its measured ratio.

Ratios are computed with the WCAG relative-luminance formula (sRGB
linearisation; `L = 0.2126·R + 0.7152·G + 0.0722·B`; contrast
`= (L1 + 0.05) / (L2 + 0.05)`). To reproduce:

```python
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def L(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)
def ratio(a, b):
    la, lb = L(a), L(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
```

## Light theme (default)

### Normal-size text — target 4.5:1

| Pair | Foreground | Background | Ratio | Result |
| --- | --- | --- | --- | --- |
| Body / connection / input text | `#333333` | `#FFFFFF` | 12.63:1 | PASS |
| Links, outline-button labels | `#C24E00` | `#FFFFFF` | 4.79:1 | PASS |
| Login labels, version, `h1` (grey) | `#767676` | `#FFFFFF` | 4.54:1 | PASS |
| Primary button label | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS *(was 3.00:1 on `#FF6200`)* |
| Primary button hover label | `#FFFFFF` | `#A84300` | 6.06:1 | PASS *(was 3.77:1 on `#E15700`)* |
| Secondary button hover label | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS *(was 3.00:1)* |
| Menu / header bar text | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS *(was 3.00:1)* |
| Menu outline-button label | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS *(was 3.00:1)* |
| Menu outline-button hover label | `#C24E00` | `#FFFFFF` | 4.79:1 | PASS *(was 3.00:1)* |

### Large text — target 3:1

| Pair | Foreground | Background | Ratio | Result |
| --- | --- | --- | --- | --- |
| Header `h2` | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS |

### UI components, borders, focus — target 3:1

| Pair | Foreground | Background | Ratio | Result |
| --- | --- | --- | --- | --- |
| Input resting border | `#8C8C8C` | `#FFFFFF` | 3.36:1 | PASS *(was 1.41:1 on `#D9D9D9`)* |
| Menu outline-button border | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS *(was 2.53:1 at 85% alpha)* |
| Focus ring (`:focus-visible`) | `#C24E00` | `#FFFFFF` | 4.79:1 | PASS |
| Focus ring on the menu bar | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS |
| Input focus border | `#FF6200` | `#FFFFFF` | 3.00:1 | PASS *(at threshold — see note)* |
| Secondary / outline button border | `#FF6200` | `#FFFFFF` | 3.00:1 | PASS *(at threshold — see note)* |

**Note on the `#FF6200` borders.** The brand orange is exactly 3.0004:1 on
white, meeting the 3:1 minimum for UI-component boundaries. Keyboard focus does
not depend on it: the primary focus indicator is the 3px `:focus-visible`
outline in `#C24E00` (4.79:1). The bright `#FF6200` is retained here, on the
login backdrop gradient, and on the lion mark to keep the brand identity.

### Disabled controls — WCAG-exempt

| Pair | Foreground | Background | Ratio | Result |
| --- | --- | --- | --- | --- |
| Disabled button label | `#333333` | `#F2B48A` | 7.02:1 | Exempt *(improved from 1.80:1 white)* |

Disabled/inactive controls are excluded from WCAG SC 1.4.3 and 1.4.11. The label
was switched from white to charcoal anyway, purely for legibility.

## Dark theme (`prefers-color-scheme: dark`)

The dark variant re-tunes the palette for dark surfaces. Same targets: text
4.5:1, UI/borders/focus 3:1. All pairs pass.

| Pair | Foreground | Background | Ratio | Result |
| --- | --- | --- | --- | --- |
| Body / connection text | `#E6E6E6` | `#1A1A1A` | 13.94:1 | PASS |
| Links | `#FFA366` | `#1A1A1A` | 8.85:1 | PASS |
| Card / notification text | `#E6E6E6` | `#242424` | 12.44:1 | PASS |
| Muted labels, field headers | `#A8A8A8` | `#242424` | 6.53:1 | PASS |
| Input text | `#E6E6E6` | `#303030` | 10.57:1 | PASS |
| Primary button label | `#1A1A1A` | `#FF8A3D` | 7.42:1 | PASS |
| Primary hover label | `#1A1A1A` | `#FF9E52` | 8.51:1 | PASS |
| Secondary button label | `#FFA366` | `#242424` | 7.90:1 | PASS |
| Menu / header bar text | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS |
| Menu hover label | `#C24E00` | `#FFFFFF` | 4.79:1 | PASS |
| Input resting border | `#7A7A7A` | `#303030` | 3.07:1 | PASS |
| Input focus border | `#FFA366` | `#303030` | 6.71:1 | PASS |
| Focus ring | `#FFA366` | `#1A1A1A` | 8.85:1 | PASS |
| Menu focus ring | `#FFFFFF` | `#C24E00` | 4.79:1 | PASS |
| Secondary / notification accent | `#FF8A3D` | `#242424` | 6.62:1 | PASS |
| Disabled label *(exempt)* | `#8F8F8F` | `#3A3A3A` | 3.52:1 | PASS |

White-on-bright-orange cannot reach 4.5:1, so dark mode splits it the same way
the light theme does: button fills use dark text on bright orange (7.4:1+), while
the menu bar keeps white text and deepens to `#C24E00` (4.79:1). A custom
`BRAND_COLOR` recolours the light theme only; the dark block keeps this palette.

## Custom brand colours

Recolouring the theme with `BRAND_COLOR` (see
[INSTRUCTIONS.md](../INSTRUCTIONS.md#5-customize-with-build-options-recommended))
derives the darker shades automatically, but the resulting contrast depends on
the colour you pick. If you choose a light brand colour, set `BRAND_COLOR_DARKER`
to a shade that reaches 4.5:1 with white for links and outline-button labels,
and re-check the pairs above with the snippet at the top of this file.
