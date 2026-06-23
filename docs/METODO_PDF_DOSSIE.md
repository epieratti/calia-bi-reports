# Metodologia — PDF a partir do HTML do dossiê

Texto operacional em **pt-BR**. Descreve o fluxo usado na entrega **Caixa — Isadora Cruz** (`caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html` → `.pdf`) e generaliza para **qualquer** dossiê HTML com gate no repositório.

**Governança** (senha em canal seguro, commit público, dados sensíveis): [`docs/GOVERNANCA_ENTREGA.md`](GOVERNANCA_ENTREGA.md).

**Implementação e flags do script:** [`tools/dossier_export_pdf.py`](../tools/dossier_export_pdf.py) e secção **PDF** em [`tools/README.md`](../tools/README.md).

---

## 1. Objetivo

- Gerar um **PDF** com aparência próxima ao HTML (cores, cards, tipografia), para **anexo**, **impressão** ou cliente que **não** consiga usar o gate no navegador.
- O PDF usa **`@media print`** do próprio HTML: o que estiver com classe `no-print` **não** entra no papel (ex.: sumário, notas “só tela”).
- **Não** substitui o HTML publicado no GitHub Pages: o PDF é **artefato adicional** quando combinado na entrega.

---

## 2. Pré-requisitos (máquina do agente)

Na **raiz** do repositório:

```bash
pip install -r tools/requirements-pdf.txt
playwright install chromium
```

---

## 3. HTML pronto antes do export

1. **HTML publicado ou validado localmente** — gate, links externos com `target="_blank"` quando aplicável, conteúdo autocontido.
2. **`@media print`** no `<style>` do dossiê — margens, tipos menores se quiseres versão compacta, ocultar blocos só para papel.
3. **Chart.js (se existir):**
   - Inicialização **após** desbloquear o gate (ex.: `initCharts()` no submit ou com `--skip-gate`).
   - **Títulos** dos gráficos preferencialmente em **HTML** (fora do plugin `title` do Chart.js) para libertar área do canvas no PDF.
   - Layout do painel: **flex** com `justify-content: center` e largura máxima consistente entre gráficos (evita “tudo à direita” de um `grid` de duas colunas que empurra o segundo gráfico para a metade direita da página).
4. **Anti-vazamento** no texto visível:

```bash
python3 tools/check_client_html_leakage.py caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html
```

(Ajusta o caminho à pasta do cliente: `caixa`, `embratur`, `febraban`, etc.)

---

## 4. Servidor HTTP e caminhos relativos

O script **`tools/dossier_export_pdf.py`** sobe um **HTTP server na raiz do repositório** (não só na pasta do `.html`). Assim resolvem-se URLs relativas como `../assets/brand/logo-white.svg` e qualquer recurso referenciado a partir da raiz.

---

## 5. Comando canônico (exemplo Isadora Cruz)

**Uso interno** (sem digitar senha no terminal — o script esconde o gate e chama `initCharts()`):

```bash
python3 tools/dossier_export_pdf.py \
  --html caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html \
  --out caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf \
  --skip-gate \
  --post-unlock-wait 5
```

- **`--skip-gate`:** uso **interno**; não expor em issues públicas como substituto de política de acesso. Para fluxo com senha, omitir esta flag e usar `--password` ou `DOSSIER_PDF_PASSWORD` (ver governança).
- **`--post-unlock-wait`:** segundos a esperar **depois** do conteúdo visível e **antes** de mudar para `print` — dá tempo ao **Chart.js** desenhar os canvas. Para vários gráficos, **4–5 s** é um valor seguro; podes subir se algum canvas sair vazio no PDF.
- **`--landscape`:** gera **A4 paisagem** no Playwright (mais área útil para tabelas lado a lado).
- **`--margin-tight`:** margens **≈4 mm** em todos os lados no `page.pdf()` (em conjunto com CSS `@media print` compacto, útil para caber em **2 páginas**).

**Com senha** (sem `--skip-gate`):

```bash
export DOSSIER_PDF_PASSWORD='…'   # preferível a colar a senha na linha de comandos
python3 tools/dossier_export_pdf.py \
  --html caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html \
  --out caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf \
  --post-unlock-wait 5
```

**Make** (com senha no ambiente; opcional **`POST_UNLOCK_WAIT`** e **`SKIP_GATE=1`** só interno — ver `Makefile`):

```bash
export DOSSIER_PDF_PASSWORD='…'
make dossie-pdf HTML=caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html OUT=caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf POST_UNLOCK_WAIT=5
```

**Make sem senha** (uso interno; equivale a `--skip-gate`):

```bash
make dossie-pdf HTML=caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html OUT=caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf SKIP_GATE=1 POST_UNLOCK_WAIT=5
```

---

## 6. O que o script faz (ordem interna — importante para Chart.js)

1. Arranca o servidor HTTP na **raiz** do repo e abre o `.html` no Chromium (Playwright).
2. **Desbloqueia** o conteúdo: ou com **`--skip-gate`** (esconde `#access-gate`, mostra `#dossier-root`, chama `initCharts()`), ou preenche a senha e submete o formulário.
3. Espera **`max(0,8 s, --post-unlock-wait)`** — tempo para os gráficos renderizarem em modo **ecrã**.
4. Aplica **`emulate_media('print')`** — passam a valer as regras **`@media print`** (altura dos `.chart-container`, colunas, etc.).
5. Dispara **`resize`** na janela e, em **cada** `<canvas>`, `Chart.getChart(canvas).resize()` — **obrigatório** porque, após o passo 4, as caixas dos gráficos mudam de tamanho; sem este passo o canvas pode **sobrepor texto** no PDF.
6. Espera **~0,55 s** e gera o **PDF** (A4, `print_background`, margens compactas no script).

Se você alterar o CSS de impressão dos gráficos, **regenere** o PDF e reabra o arquivo para confirmar que não há sobreposição.

---

## 7. QA rápido do PDF gerado

- [ ] Abrir o `.pdf` e percorrer **todas** as páginas.
- [ ] **Gráficos** completos, sem cortar títulos do dossiê nem legendas; sem “manchas” sobre parágrafos.
- [ ] **Links** clicáveis (se o leitor de PDF suportar).
- [ ] Se o PDF for para o **cliente** e o HTML tiver gate: confirmar se a política permite PDF **sem** gate ou se o envio é canal fechado apenas.

---

## 8. Git e GitHub Pages

Quando o PDF (e/ou o HTML) for entregue no **site público**:

1. `git status` → `git add` só os arquivos relevantes.
2. `git commit` com mensagem em **pt-BR** (imperativo ou descrição clara).
3. `git push` ao branch acordado — para artefatos em `caixa/`, `febraban/`, etc., o remoto deve ficar alinhado para o **GitHub Pages** refletir o arquivo (incluindo URL **raw** do `.pdf` se aplicável).

---

## 9. Resumo ultra-curto (colar no checklist interno)

1. `check_client_html_leakage.py` no `.html`  
2. `dossier_export_pdf.py` com `--post-unlock-wait 4` ou `5` se houver Chart.js; **`--skip-gate`** só interno  
3. Abrir o PDF e validar gráficos + quebras  
4. Commit + push se for entrega no ar  

---

## 10. Referência de arquivos (Isadora)

| Artefato | Caminho |
|----------|---------|
| HTML | `caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html` |
| PDF | `caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf` |
| Índice Caixa (link HTML) | `caixa/index.html`, `caixa/README.md` |

PDFs de Isadora e Rodolfo: regenerar com `make dossie-pdf` antes de publicar link no índice (ver [`docs/INVENTARIO_DOSSIES.md`](INVENTARIO_DOSSIES.md)).

Para outro dossiê, troca os caminhos mantendo o **mesmo fluxo** de comandos e QA.
