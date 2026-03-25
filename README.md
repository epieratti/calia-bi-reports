# calia-bi-reports

O dossiê fica na pasta **`embratur/`** do repositório (pasta real no GitHub, não só redirecionamento).

- **URL do dossiê:** https://epieratti.github.io/calia-bi-reports/embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html  
- Novos relatórios: adicione mais `.html` em **`embratur/`** no repositório (sem `index.html` na pasta).  
- A raiz do site (`/`) redireciona para o dossiê atual em `embratur/`.  
- O caminho antigo na raiz (`/20260323-…html`) existe como página mínima que redireciona para `embratur/`.

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