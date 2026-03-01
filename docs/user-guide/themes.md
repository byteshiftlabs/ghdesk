# Themes and Customization

ghdesk includes multiple color themes to suit your preferences.

---

## Available Themes

| Theme | Description |
|-------|-------------|
| **Dark** (Default) | Dark background optimized for low-light environments |
| **Light** | Bright theme for well-lit environments |
| **Nord** | Based on the [Nord color palette](https://www.nordtheme.com/), cool arctic aesthetic |
| **Dracula** | Based on the [Dracula theme](https://draculatheme.com/), popular among developers |
| **Monokai** | Inspired by the classic Monokai color scheme from Sublime Text |

---

## Changing Themes

1. Locate the theme dropdown in the toolbar
2. Click to expand the list of available themes
3. Select your preferred theme
4. The theme applies immediately

The selected theme is applied for the current session.

---

## Theme Architecture

ghdesk themes are implemented as Qt stylesheets (QSS), providing comprehensive styling for all widgets.

Each theme is defined in a separate module under `ui/themes/`:

```
ui/themes/
├── __init__.py     # Theme loader and exports
├── dark.py         # Dark theme stylesheet
├── light.py        # Light theme stylesheet
├── nord.py         # Nord theme stylesheet
├── dracula.py      # Dracula theme stylesheet
└── monokai.py      # Monokai theme stylesheet
```

---

## Next Steps

- [Architecture](../development/architecture.md) — Understand how themes integrate with the UI layer
- [Code Style](../development/code-style.md) — Follow code conventions when adding themes
