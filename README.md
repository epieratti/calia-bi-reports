# calia-bi-reports

**Novo agente / como começar:** [`docs/tutorials/INICIO_AGENTE.md`](docs/tutorials/INICIO_AGENTE.md).

**Como criar / entregar dossiês (qualquer cliente):** **`PLAYBOOK_AGENTES.md`** (guia curto) e **`PLAYBOOK_DOSSIES.md`** (referência completa; modos A/B/C), centrados em **brand safety / vetting de creators / disaster check**. **`docs/tutorials/PRIMEIRO_DIA.md`** — checklist; **`docs/PROMPTS_IA_AGENTES.md`** — prompts para IA; **GitHub → New issue → Briefing — novo dossiê** para pedidos estruturados. **`docs/reference/INDICE_METODOS.md`** — atalhos; **`methods/README.md`** — métodos reutilizáveis; **`docs/EXEMPLOS_BRIEFINGS.md`** — padrões de briefing. *Loterias 2026* no repo é **exemplo** do modo B. **Toolbox:** `make help` e `tools/`; exemplo mínimo em **`projects/_template/`**. **Após publicar** um HTML novo numa pasta com **`index.html`**, atualize o índice com o link do arquivo. **Vários agentes no mesmo dossiê:** [`docs/how-to/MULTI_AGENTES.md`](docs/how-to/MULTI_AGENTES.md). **Senha, validar no Pages, PDF e escalação:** [`docs/how-to/GOVERNANCA_ENTREGA.md`](docs/how-to/GOVERNANCA_ENTREGA.md). **Calibragem de qualidade do conteúdo:** [`docs/explanation/CALIBRAGEM_QUALIDADE.md`](docs/explanation/CALIBRAGEM_QUALIDADE.md). **PDF** (HTML → PDF, metodologia Caixa Isadora + Chart.js): [`docs/how-to/METODO_PDF_DOSSIE.md`](docs/how-to/METODO_PDF_DOSSIE.md) · `engine/cli/export_pdf.py` / `make dossie-pdf` (Playwright; `engine/requirements/pdf.txt`).

O dossiê principal da Embratur fica em **`embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html`**. Relatórios da **Caixa** ficam na pasta **`caixa/`** (mesmo padrão; ver `caixa/README.md`). Dossiês do cliente **Febraban** ficam em **`febraban/`** (ver `febraban/README.md`).

- **URL direta do dossiê Embratur:** https://epieratti.github.io/calia-bi-reports/embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html  
- **Dossiê CAIXA (personalidades):** https://epieratti.github.io/calia-bi-reports/caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html — senha **`caixa2026`** (proteção client-side; ver `caixa/README.md`).
- **URL da raiz do site:** https://epieratti.github.io/calia-bi-reports/ — o arquivo **`index.html`** na raiz redireciona para o mesmo dossiê em `embratur/`.  
- **Acesso:** o HTML do dossiê inclui **proteção por senha no navegador** (hash SHA-256). A senha usada no projeto é **`embratur2026`** (altere no próprio HTML se precisar).  
- **Novos relatórios Embratur:** adicione mais `.html` em **`embratur/`** conforme necessário (não é obrigatório ter `index.html` dentro de `embratur/`).
- **Novos relatórios Caixa:** use a pasta **`caixa/`**.
- **Febraban:** HTML em **`febraban/`** — exemplo https://epieratti.github.io/calia-bi-reports/febraban/20260427-dossie-febraban-concorrencia-creators-2026.html — senha **`febraban2026`** (ver `febraban/README.md`).
- **Loterias 2026 (Brand Safety):** pesquisa em `loterias2026/research/`; fonte do dossiê em `projects/caixa/loterias/always-on-20260401/data/dossier_loterias2026.md` + `dossier_loterias2026_panels.yaml`; HTML com `python3 loterias2026/scripts/build_dossier_completo.py` → `loterias2026/output/` (copiar para `caixa/` ao publicar). Senha **`caixa2026`**. Ver `projects/caixa/loterias/always-on-20260401/README.md`.

## Ativar GitHub Pages (obrigatório para sair do 404)

No repositório no GitHub: **Settings** → **Pages** → em **Build and deployment**:

### Opção A — mais simples (recomendada)

- **Source:** *Deploy from a branch*
- **Branch:** `main`, pasta **`/ (root)`**
- Salve e aguarde alguns minutos.

### Opção B — GitHub Actions

- **Source:** *GitHub Actions*
- Salve, depois em **Actions** execute de novo o workflow **Deploy GitHub Pages** (ou faça um push em `main`).

Se o Pages foi ativado **depois** de uma execução que falhou, o site só sobe quando houver **pelo menos um deploy com sucesso** (novo push em `main` ou *Re-run* do workflow). Sem isso, a URL pode continuar em 404.

Enquanto o Pages não estiver ativado com uma dessas fontes, a URL acima mostra *“There isn’t a GitHub Pages site here”*.

## Pesquisa complementar (opcional)

Em **`embratur/scripts/`** e **`embratur/research/`** há script e notas sobre proxy de penetração (Trends/Wikipedia); ver `embratur/research/README.md`.
