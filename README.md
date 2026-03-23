# calia-bi-reports

Repositório criado especificamente para publicar estudos e relatórios de **Business Intelligence** para clientes da **Agência Calia**, utilizando [GitHub Pages](https://pages.github.com/).

## 🌐 Acesso ao portal

O portal está disponível em: **https://epieratti.github.io/calia-bi-reports/**

## 📁 Estrutura do repositório

```
calia-bi-reports/
├── index.html                          # Página inicial (lista de relatórios)
├── assets/
│   └── css/
│       └── style.css                   # Estilos globais do portal
└── reports/
    └── exemplo-analise-vendas/
        └── index.html                  # Página de relatório (template)
```

## ➕ Como adicionar um novo relatório

1. Crie uma pasta em `reports/` com um nome descritivo (use hifens, sem espaços), por exemplo:
   ```
   reports/analise-marketing-q1-2026/
   ```

2. Copie o arquivo `reports/exemplo-analise-vendas/index.html` para a nova pasta e edite:
   - Título, descrição e metadados do relatório
   - URL do embed do dashboard (Power BI, Looker Studio, Metabase, Tableau, etc.)
   - Textos das seções de resumo, KPIs e recomendações

3. Adicione um card para o novo relatório na seção correspondente do `index.html` principal.

4. Faça commit e push para a branch principal. O GitHub Actions irá publicar automaticamente.

## 🚀 Deploy

O deploy é feito automaticamente via **GitHub Actions** sempre que há um push na branch `main`. O workflow está em `.github/workflows/pages.yml`.

Para ativar o GitHub Pages no repositório:
- Acesse **Settings → Pages**
- Em **Source**, selecione **GitHub Actions**
