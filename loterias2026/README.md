# Always ON Loterias 2026 — Brand Safety

## Dossiê HTML completo

- **Fonte estruturada:** `data/dossier_loterias2026.yaml` (governança, painéis IG/TT/YT/X, síntese Proposta P, 13 perfis).
- **Evidências com URLs:** `research/FONTES_BRAND_SAFETY_LOTERIAS2026.md`
- **Metodologia:** `research/METODO_BRAND_SAFETY_LOTERIAS2026.md`
- **Handles do squad:** `data/influencers.yaml`

**Gerar o HTML:**

```bash
cd loterias2026
python scripts/build_dossier_completo.py
```

Saída: `output/20260401-dossie-squad-always-on-loterias-2026.html`

**No ar (GitHub Pages, pasta `caixa/`):** após o deploy em `main`, use  
https://epieratti.github.io/calia-bi-reports/caixa/20260401-dossie-squad-always-on-loterias-2026.html  
(senha **apenas** `caixa2026`). Copie o HTML atualizado para `caixa/` ao publicar.

**Acesso:** proteção client-side — somente **`caixa2026`** (SHA-256 no script), alinhado ao box do dossiê 20260326, sem alias.

Após alterar métricas ou textos, edite o YAML e **regenere** o HTML para manter uma única fonte da verdade estruturada.

## Pipeline opcional (Apify)

Ver `requirements.txt` e `.github/workflows/loterias2026-brand-safety.yml` — exige `APIFY_TOKEN`; gera outro HTML heurístico em `output/dossie-brand-safety-loterias-2026.html`.
