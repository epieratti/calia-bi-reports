# Primeiro dia — dossiê modo B (checklist curto)

1. Ler **`PLAYBOOK_AGENTES.md`** (5 min) e abrir **`docs/INDICE_METODOS.md`** quando precisar de um método.
2. **Briefing fechado** — use o template de issue em **GitHub → New issue → Briefing — novo dossiê** ou copie o modelo em `PLAYBOOK_DOSSIES.md` §1.
3. **Novo par de arquivos:** na pasta do lote (ex.: `loterias2026/data/`):
   - `python3 loterias2026/scripts/new_creator_dossier.py …` **ou** copiar `loterias2026/data/dossier_TEMPLATE.md` + renomear + criar `*_panels.yaml` ao lado.
4. **Preencher** narrativa no `.md` e **só números** no `*_panels.yaml`.
5. **Validar:** `python3 tools/validate_dossier_source.py caminho/dossier_*.md` — opcional `--hints` para dicas de lacunas.
6. **Publicar:** `make dossie-entregar MD=… DEST=caixa/loterias` (ou `caixa/`, `embratur/`) — gera nome `YYYYMMDD-dossie-<slug>.html`, roda links e anti-vazamento.
7. **Git:** `git add` → `commit` em pt-BR → **`git push origin main`** (Pages).
8. **Validar vendo no ar:** abrir a URL do Pages com a senha — ver [`GOVERNANCA_ENTREGA.md`](GOVERNANCA_ENTREGA.md).
9. **PDF (opcional):** após aprovar o HTML, `make dossie-pdf` com `DOSSIER_PDF_PASSWORD` exportada (ou `python3 tools/dossier_export_pdf.py`).
10. **Índice:** se a pasta do cliente tiver **`index.html`**, acrescente o link do novo `.html`.

**Mais de um agente no mesmo projeto:** leia [`MULTI_AGENTES.md`](MULTI_AGENTES.md) antes de dividir tarefas.
