# calia-bi-reports

O dossiê principal da Embratur fica em **`embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html`**. Relatórios da **Caixa** ficam na pasta **`caixa/`** (mesmo padrão; ver `caixa/README.md`).

- **URL direta do dossiê Embratur:** https://epieratti.github.io/calia-bi-reports/embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html  
- **Dossiê CAIXA (personalidades):** https://epieratti.github.io/calia-bi-reports/caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html — senha **`caixa2026`** (proteção client-side; ver `caixa/README.md`).
- **URL da raiz do site:** https://epieratti.github.io/calia-bi-reports/ — o arquivo **`index.html`** na raiz redireciona para o mesmo dossiê em `embratur/`.  
- **Acesso:** o HTML do dossiê inclui **proteção por senha no navegador** (hash SHA-256). A senha usada no projeto é **`embratur2026`** (altere no próprio HTML se precisar).  
- **Novos relatórios Embratur:** adicione mais `.html` em **`embratur/`** conforme necessário (não é obrigatório ter `index.html` dentro de `embratur/`).
- **Novos relatórios Caixa:** use a pasta **`caixa/`**.
- **Loterias 2026 (Brand Safety):** pesquisa em `loterias2026/research/`; dossiê HTML gerado com `python loterias2026/scripts/build_dossier_completo.py` → `loterias2026/output/20260401-dossie-brand-safety-loterias-2026-completo.html` (senhas `caixa2026` / `embratur2026`). Ver `loterias2026/README.md`.

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
