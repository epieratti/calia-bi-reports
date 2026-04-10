# Governança de entrega — senha, validação, PDF, escalação

Texto operacional para **Calia BI Reports** (dossiês em HTML no GitHub Pages). Ajuste com **jurídico** e **cliente** quando necessário.

---

## 1. Senha do gate — **não** colar em canal público

- **Issues públicas, comentários em PR, tickets abertos:** use só **“igual ao dossiê / arquivo: `…html`”** ou **“envio senha por [Slack/1Password/e-mail interno]”** — **não** escreva o texto da senha.
- **Repositório Git:** o que vai para o remoto é **hash SHA-256** no front matter (`password_sha256_hex`), não a senha em claro.
- **Quem precisa da senha para PDF local:** use **`DOSSIER_PDF_PASSWORD`** no ambiente ou passe **`--password`** num terminal privado (evita histórico: `read -s` e export).

---

## 2. Validação humana **vendo** o relatório (fluxo “publicar primeiro”)

Objetivo: **você precisa abrir o HTML real** (layout, links, gate) antes de dar como fechado.

1. **Build + push** do HTML para a **URL do Pages** (mesmo que seja “revisão”), com **senha** já configurada.
2. Você **abre a URL**, testa **senha** e **navegação** (sumário, painel, tabelas, mobile se importar).
3. Se houver ajuste: novo commit/push; repetir até OK.
4. **Opcional:** gerar **PDF** para arquivo/arquivo ao cliente (`tools/dossier_export_pdf.py`) **depois** de aprovado o HTML.

**“Aprovação”** aqui significa: **vi o relatório publicado e está correto** — não um passo separado “antes de publicar”, se o teu processo exige ver o artefato no ar.

---

## 3. PDF com UI digna (export local)

- O HTML do modo B já inclui estilos **`@media print`**: fundo branco, **gate oculto**, conteúdo visível, **URLs após links** para auditoria no PDF, filtro do painel executivo oculto na impressão.
- **Gerar:** `python3 tools/dossier_export_pdf.py --html <caminho>.html --out <saida>.pdf` com senha (ver `tools/README.md`).
- Depende de **Playwright + Chromium** (`tools/requirements-pdf.txt`). O script sobe um **servidor HTTP local** para o gate funcionar (`crypto.subtle` em contexto seguro).

**Não** commitar PDF com dados sensíveis no repo **público** sem alinhamento com política de dados.

---

## 4. Escalação quando o achado é grave

Use como **roteiro**; preencha nomes/canais da tua organização.

| Gravidade (exemplo) | Ação mínima |
|---------------------|-------------|
| **Alto** — risco claro à marca, crime, violência, discurso extremo com evidência | **Parar** uso do nome na campanha até revisão; **avisar** direção de atendimento + contato cliente **em horário útil**; registrar data e fonte no dossiê. |
| **Moderado** — credibilidade, polêmica recorrente, concorrência ambígua | Marcar na **síntese de risco** e na **tabela resumo**; **reunião** planejamento + atendimento; cliente decide com **jurídico** se necessário. |
| **Baixo / não consta** | Seguir fluxo normal de entrega; manter **data da coleta** explícita. |

- **Não** substituir parecer **jurídico** por opinião do modelo de IA.
- **Evidência:** link estável no corpo do dossiê (playbook: autocontido + hyperlink).

---

## 5. Checklist rápido antes de “fechado”

- [ ] URL do Pages abre; senha correta; sem vazamento de caminhos do repo no texto visível (`check_client_html_leakage.py`).
- [ ] `index.html` da pasta atualizado se existir.
- [ ] PDF gerado só se for entrega combinada — e armazenamento conforme política.
