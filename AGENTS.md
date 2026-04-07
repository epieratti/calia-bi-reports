# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

Static HTML site (GitHub Pages) with self-contained BI audit dossiers for two clients: **Embratur** and **Caixa**. No build step, no backend, no package manager. All CSS/JS loaded from CDNs (Tailwind, Chart.js, Google Fonts).

### Running locally

```bash
python3 -m http.server 8000
```

Then open in browser:
- **Embratur:** `http://localhost:8000/embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html` — password: `embratur2026`
- **Caixa:** `http://localhost:8000/caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html` — password: `caixa2026`
- **Root redirect:** `http://localhost:8000/` redirects to the Embratur dossier.

### Lint / test / build

- **No linter, test framework, or build system configured.** The HTML files are static and self-contained.
- Validation is visual: open the reports in a browser, enter the password, and confirm charts (Chart.js) and styles (Tailwind) render correctly.

### Optional Python research script

`embratur/scripts/penetracao_mercados.py` collects Google Trends + Wikipedia data. Requires `pip install pytrends requests`. Not part of the served product — see `embratur/research/README.md` for details.
