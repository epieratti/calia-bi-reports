# Exemplo mínimo (1 perfil) — modo B

Uso: copiar e renomear para um novo slug ou usar como referência de estrutura sem carregar o lote completo de 8/13 perfis.

- `dossier_minimo_exemplo.md` + `dossier_minimo_exemplo_panels.yaml`

Build de teste (na raiz):

```bash
cd loterias2026
python3 scripts/build_dossier_completo.py \
  --md ../examples/minimo/dossier_minimo_exemplo.md \
  --panels ../examples/minimo/dossier_minimo_exemplo_panels.yaml \
  --out ../examples/minimo/output-preview.html \
  --variant squad_8
```

Validar:

```bash
python3 tools/validate_dossier_source.py examples/minimo/dossier_minimo_exemplo.md
```
