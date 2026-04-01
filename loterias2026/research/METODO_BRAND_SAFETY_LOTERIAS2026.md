# Metodologia — Brand Safety & Due Diligence (Always ON Loterias 2026)

Documento **separado** do arquivo de **resultados** (`FONTES_BRAND_SAFETY_LOTERIAS2026.md`). Use este arquivo para processo; use FONTES apenas para **URLs, tabelas de achados e validações**.

---

## Escopo da coleta

- **Coleta:** web aberta (notícias, sites institucionais indexados). Nesta fase **não** há media kit nem acesso sistemático pago às APIs das redes. Para **ampliar** cobertura com perfil público, ver seção **Ferramentas open source e fluxo OSINT** (Instaloader, yt-dlp, Sherlock, etc.) — uso local e respeitando ToS.
- **Governança — sem dados primários das redes:** texto explícito para leitores do dossiê em `FONTES_BRAND_SAFETY_LOTERIAS2026.md` → seção **Limite do dossiê — sem dados primários das redes** (“não consta” ≠ ausência de risco; lacunas estruturais).
- **Concorrência:** distinguir parceria/publipost com operador de aposta ou loteria de menção temática (humor, espetáculo, notícia).
- **Marcas:** nesta fase só entram com **prova pública** (matéria, post arquivado, vídeo); senão ficam como “não verificado”.
- **Confiança sugerida:** Alta = várias fontes ou primário claro; Média = um veículo sólido; Baixa = agregador, rumor, SEO.
- **IA (Perplexity etc.):** só como pista; cada afirmação precisa URL ou fica refutada/não verificada.

---

## Boas práticas (pesquisa sem media kit)

1. Um fato = afirmação + URL + data + tipo de prova.
2. Hierarquia: primário > jornal com autoria > agregador > fórum.
3. Desambiguação: nome completo + @ + contexto; anotar homônimos descartados.
4. Triangulação em bet/política/saúde: duas fontes ou uma primária forte.
5. Guardar a query que funcionou (replicável).
6. Declarar snapshot (“até mar/2026”); seguidores não provam parceria.
7. “Não achei na web” ≠ “não existe”.
8. Não copiar lista de marcas só da IA.
9. “Bet” em domínio de curso: ler a página antes de marcar conflito.
10. Relatório ao cliente: risco + evidência + lacuna.

---

## Polêmicas, política e risco Caixa/loterias — termos de busca

Usar com **nome entre aspas** + ano quando fizer sentido.

### Polêmicas / reputação

Justiça: processo, denúncia, BO, MP, condenado, TSE.  
Mídia: polêmica, cancelamento, racismo, xenofobia, fake news.  
Saúde (risco institucional): TDAH, cura, automedicação, promessa (com contexto de curso).  
Fraude: golpe, pix, pirâmide, cripto.

Repetir com `site:g1.globo.com`, `site:uol.com.br`, etc., em dias diferentes se necessário.

### Política

Partido, voto, eleição, Lula, Bolsonaro — filtrar falso positivo “voto” do BBB.  
Pautas sensíveis: aborto, STF, privatização, greve, “Caixa Econômica”, CEF, FGTS.

### Concorrência / jogo (loterias)

Bet, cassino, bônus cadastro, afiliado, Tigrinho, Blaze; separar de **Detox Bet** / **Bet Cursos** (ler página).  
Jogo do bicho, banca vs. Mega-Sena/CAIXA informativo.

---

## Tentativas — media kit / hubs (registro mar/2026)

*Esta fase de pesquisa pública não usou media kit; registro abaixo é só o que foi testado.*

| Pista | Resultado |
|--------|-----------|
| PDF ViU Hub público | Não localizado na busca aberta |
| Globo Ads ViU | https://globoads.globo.com/para-o-seu-negocio/servicos/viu — sem kit por talento no acesso usado |
| Curta `.../rafaelgratta` | Host não resolveu neste ambiente de agente; validar em rede local |
| Curta Pitel (`pitelgiovanna`) | 503 / indisponível nas tentativas |
| `site:instagram.com` + marca | Ruído alto sem URL de post |

---

## Checklist pendências de identidade

- [ ] `@comcertezaaline` vs `@aliineza`
- [ ] `@davizoa` — perfil correto
- [ ] Megh Merly vs Juliana Merhy
- [ ] Homônimo Giovanna Reis ≠ Pitel
- [ ] Link cassino spam Rafael Gratta — não usar sem segunda fonte

---

## Fases futuras (fora do escopo pesquisa pública)

- Media kit Curta em DNS normal
- Lista formal ViU / assessoria (se cliente abrir fase comercial)

---

## Ferramentas open source e fluxo OSINT (quando a imprensa não cobre o handle)

**Objetivo:** enriquecer perfis “finos” na web (ex.: `@davizoa`, `@comcertezaaline`) **sem** painel proprietário de rede social — usando **perfil público**, legendas, hashtags e metadados que já são visíveis no browser.

**Avisos obrigatórios**

- **Termos de uso** das plataformas podem **proibir** automação; uso excessivo gera **bloqueio** de IP/conta. Preferir **volume baixo**, **intervalo** entre requisições e **só** o necessário para o dossiê.
- **Não** é substituto de **briefing** (nome civil, @ canônico): continua sendo a fonte mais segura para desambiguar homônimos.
- Resultado de scraper = **primário frágil**: salvar **HTML/PDF**, **timestamp** e **URL**; plataformas mudam layout e quebram ferramentas.

### Ferramentas no GitHub (ponto de partida)

| Ferramenta | Repositório | Uso típico neste projeto |
|------------|-------------|---------------------------|
| **Instaloader** | [instaloader/instaloader](https://github.com/instaloader/instaloader) | Perfil público Instagram: **bio**, posts recentes, **legendas** (caça a `#publi`, `@marca`, “cortesia”). Pode exigir **login** para amostras maiores. |
| **gallery-dl** | [mikf/gallery-dl](https://github.com/mikf/gallery-dl) | Extrator multi-site (inclui vários hosts); útil quando um post tem **permalink** e você quer **arquivo local** + legenda. |
| **yt-dlp** | [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) | **YouTube** e, quando funcional, **TikTok** público: título, descrição, comentários (se exportados), lista de vídeos do canal — bom para **concorrência** (menções a bet) e **política** (falas em vídeo). |
| **Sherlock** | [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | Mesmo **username** em dezenas de sites: achar **Twitch**, **Kwai**, **Threads**, fóruns — triangula identidade sem API paga. |
| **Maigret** (alternativa) | buscar no GitHub `maigret osint` | Similar ao Sherlock com outra lista de sites. |

### Buscas e fóruns (complemento)

- **`site:tiktok.com/@handle`** e **`site:x.com/handle`** no Google/DuckDuckGo — frequentemente trazem **snippets** que o RSS de notícias não indexa.
- **Reddit**, **threads** em português: `site:reddit.com "@" + handle` ou nome + cidade (filtrar ruído).
- **Web Archive** ([web.archive.org](https://web.archive.org)): perfil ou post que sumiu; útil para **polêmicas** apagadas.

### Fluxo sugerido para os handles “magros”

1. **Sherlock** (ou busca manual `site:`) no **`davizoa`** / variações (`davi.zoa`, etc.).
2. **yt-dlp** no canal YouTube `@davizoa` (se existir e for público): varrer **descrições** por marca/bet/política.
3. **Instaloader** ou **navegador logado** só para **amostra** de posts (legendas), exportar CSV/lista de URLs → preencher `FONTES_...md`.
4. Tudo que entrar no dossiê: **URL + data + trecho** (ou print arquivado).

### Limite deste ambiente (agente cloud)

Máquinas de CI/agente costumam levar **403**, **login wall** ou **CAPTCHA** em Instagram/TikTok. O playbook acima funciona melhor em **máquina local** ou VM com **navegador humano** quando a automação falhar.

**Execução real (31/03/2026):** `pip install -r loterias2026/research/osint_runs/requirements-osint.txt` — **Instaloader** → **403** no GraphQL do Instagram; **Sherlock** + **yt-dlp** → resultados em `loterias2026/research/osint_runs/20260331/` e resumo em `FONTES_BRAND_SAFETY_LOTERIAS2026.md` (seção **Rodada OSINT**).

**Dossiê HTML (entrega):** dados estruturados em `loterias2026/data/dossier_loterias2026.yaml`; geração: `python scripts/build_dossier_completo.py` → `output/20260401-dossie-squad-always-on-loterias-2026.html`. Manter **FONTES** como arquivo de evidências; o YAML como **camada de síntese** reprodutível.
