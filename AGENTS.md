# Instruções para agentes (calia-bi-reports)

**Novo agente / primeiro uso neste repo:** leia **[`docs/tutorials/INICIO_AGENTE.md`](docs/tutorials/INICIO_AGENTE.md)** — start do pipeline, primeira mensagem e **CONTRATO** (§7) para colar junto ao briefing e reduzir desvio do fluxo.

**Ao receber briefing:** seguir **`PLAYBOOK_AGENTES.md`** regra **0** — checar (E)/(C), plano visível, **depois** executar (não pular para pesquisa/build sem isso).

**Idioma deste guia e da comunicação com o usuário:** **português do Brasil (pt-BR)** — vocabulário e ortografia brasileiros, **não** português de Portugal (pt-PT). Ex.: *usuário*, *arquivo* (não “utilizador”, “ficheiro”).

Este repositório contém **relatórios e dossiês em HTML** publicados via **GitHub Pages** (`https://epieratti.github.io/calia-bi-reports/`). O **modelo principal** documentado no playbook é dossiê de **brand safety / vetting de creators / disaster check**; o trabalho típico é editar ou gerar esse HTML, scripts Python auxiliares e notas de pesquisa — não é uma aplicação web com build único na raiz.

**Idioma (regra primordial — dossiê):** todo o conteúdo do **dossiê** entregue ao cliente (fonte `.md`, painéis, HTML) deve estar em **pt-BR**, salvo o **usuário** pedir **explicitamente** outro idioma — ver `PLAYBOOK_DOSSIES.md` → *Idioma do dossiê*.

**Redação:** textos finais **humanizados**, **claros**, **sucintos** e **completos** para **planejamento, atendimento e cliente** — ver `PLAYBOOK_DOSSIES.md` → *Qualidade da redação*.

**Autocontido e fontes:** o dossiê **não** pode exigir clique em link para entender a análise; **e** toda fonte web com URL deve aparecer com **link** no HTML — ver `PLAYBOOK_DOSSIES.md` → *Documento autocontido e links*.

**Ordem de leitura sugerida:** `PLAYBOOK_AGENTES.md` → `docs/tutorials/PRIMEIRO_DIA.md` → `PLAYBOOK_DOSSIES.md` → `docs/reference/INDICE_METODOS.md` → README da pasta (`caixa/`, `projects/…`). Prompts: `docs/reference/PROMPTS_IA_AGENTES.md`. Multi-agente: `docs/how-to/MULTI_AGENTES.md`.

**Motor dossiê (modo B):** `engine/core/` · `engine/cli/build_dossier.py` · `make dossie-entregar`.

## Estrutura principal

| Área | Caminho | Notas |
|------|---------|--------|
| Marca (SVG) | `assets/brand/logo-white.svg` | Logo Calia |
| Superfície publicada | `caixa/`, `caixa/loterias/`, `febraban/`, `embratur/` | HTML no GitHub Pages |
| Fonte editável | `projects/` | `.md` + YAML + `manifest.yaml` — **não** publicado |
| Motor | `engine/` | Build, QA, PDF |
| Métodos | `methods/` | Brand safety, descoberta de @ |
| Caixa institucional | `caixa/` (raiz) | Auditorias, cartão |
| Caixa Loterias | `caixa/loterias/` | Always ON, squads |
| Lote referência modo B | `projects/caixa/loterias/always-on-20260401/` | Squad 13 perfis |

Para dossiês Loterias modo **B**, a fonte está em `projects/caixa/loterias/always-on-*/data/`; o HTML canônico em `caixa/loterias/`. Ver `caixa/README.md` e `projects/README.md`.

## Proteção por senha (client-side)

Vários HTML usam **hash SHA-256 no `<script>`** (ex.: `PASSWORD_SHA256_HEX_SET`). As senhas de referência estão documentadas em `README.md`, `caixa/README.md` e `febraban/README.md` (**não** as exponha em issues públicas desnecessariamente). Ao alterar lógica de acesso, mantenha o comportamento alinhado ao que o cliente já usa.

## Git e publicação

- Mensagens de commit em **português do Brasil**, claras (imperativo ou descrição direta do que mudou).
- Após implementar alterações pedidas: `git status` → `git add` (só o relevante) → `git commit` → push conforme o fluxo do branch em uso.
- Alterações em **`caixa/`**, **`caixa/loterias/`**, **`febraban/`**, **`embratur/`** exigem push ao remoto (Pages).

## Boas práticas para mudanças

- **Escopo mínimo:** altere só o necessário; evite refatorações amplas não solicitadas.
- **Consistência:** siga o estilo e o padrão dos HTML e scripts existentes na mesma pasta.
- **Documentação:** não crie arquivos `.md` novos por iniciativa própria, exceto quando o pedido pedir documentação **ou** forem notas de pesquisa em `research/` / atualizações a métodos já listados em `docs/reference/INDICE_METODOS.md`.

## Referência rápida

- Entrega automatizada (nome `YYYYMMDD-dossie-<slug>.html` + pipeline): `engine/cli/publish_dossier.py`, `make dossie-entregar` — ver `engine/README.md` e `make help`.
- PDF com layout próximo ao HTML: **[`docs/how-to/METODO_PDF_DOSSIE.md`](docs/how-to/METODO_PDF_DOSSIE.md)** · `engine/cli/export_pdf.py` / `make dossie-pdf` · [`docs/how-to/GOVERNANCA_ENTREGA.md`](docs/how-to/GOVERNANCA_ENTREGA.md) (senha por env, não em issue pública).
- Calibragem editorial (prova, delta, institucional): `docs/explanation/CALIBRAGEM_QUALIDADE.md`; front matter `quality_calibration` no modo B.
- Playbook de dossiês (raiz): `PLAYBOOK_DOSSIES.md`
- Índice métodos: `docs/reference/INDICE_METODOS.md`
- Visão geral e URLs: `README.md`
- Caixa (índice, senhas, dossiês): `caixa/README.md`
- Pipeline Loterias 2026: `projects/caixa/loterias/always-on-20260401/README.md`
