# Metodologia — descobrir perfis do creator em todas as redes

Uso quando a entrada é **só o nome** da pessoa ou **nome + um único @** (Instagram, TikTok, YouTube ou X). Objetivo: mapear **todos os perfis públicos relevantes** para o dossiê (IG, TikTok, YouTube, X), com **confiança documentada** e **homônimos descartados**.

Este ficheiro é **processo**; anotar handles confirmados e dúvidas no `dossier_*.md` (handles) e, se preciso, em nota de `research/`.

---

## Princípios

1. **Um perfil = uma prova** — Não copiar @ de agregador sem abrir o perfil e confirmar **bio, foto, nome exibido, tom de conteúdo** (e, se existir, link “oficial” na bio).
2. **Homônimo** — Nome comum ou creator com clone: registrar **“descartado: @… (motivo)”** na pesquisa interna; no dossiê, no máximo uma linha se for risco de confusão para o cliente.
3. **Âncora** — Se veio **um @**, tratar essa rede como **fonte primária**: ler bio, links, menções cruzadas e posts que citam outras redes.
4. **Só nome** — Começar por **busca web** + **busca nativa em cada rede** com variações (nome completo, apelido, nome + “influencer”, nome + cidade/nicho se souber do briefing).
5. **Snapshot** — Guardar **data** da verificação; perfis mudam de @ ou somem.
6. **ToS** — Respeitar termos das plataformas; scraping agressivo não substitui confirmação humana no browser.

---

## Fluxo resumido

```
Entrada (nome OU nome + 1 @)
    → Ficha rápida: nome civil?, apelido?, projeto?, cidade?, squad/campanha?
    → Se houver @ âncora: extrair da bio/links/posts tudo que apontar para outras redes
    → Busca web (queries abaixo) + busca in-app por rede
    → Para cada candidato: checklist de confirmação
    → Preencher ### Handles no .md; lacunas explícitas (“sem perfil público encontrado em …”)
```

---

## Quando já existe um @ (rede âncora)

1. Abrir o perfil **na rede dada** e copiar:
   - Nome exibido, @ exato, bio completa.
   - **Link na bio** (Linktree, Beacons, “meu Instagram”, canal, site) — seguir e anotar cada destino.
2. Procurar **nos próprios posts/fixados** menções explícitas: “me segue no TikTok @…”, “YouTube: …”.
3. **Inverter busca:** no Google/Bing, `"@handle"` ou `site:instagram.com` + parte do nome (para achar **outras** contas do mesmo humano, não só clones).
4. Repetir o **checklist de confirmação** (secção abaixo) para cada nova rede encontrada.

---

## Quando só existe o nome

1. **Briefing mínimo** — Se possível, obter: profissão/nicho (humor, música, esportes), cidade/região, programa (ex-BBB), marca/agência, **outro talento do mesmo squad** para cruzar listas oficiais.
2. **Busca web (queries úteis)** — Ajustar aspas e ano:
   - `"Nome Sobrenome" Instagram`
   - `"Nome Sobrenome" TikTok oficial`
   - `"Nome Sobrenome" YouTube canal`
   - `"Nome Sobrenome" Twitter` ou `site:x.com` / `site:twitter.com`
   - `"Nome Sobrenome" link na bio` / `linktree` / `beacons`
3. **Busca dentro de cada app/site** (logado ou não, conforme permitido):
   - **Instagram:** busca por nome; abrir candidatos e comparar bio/foto/conteúdo.
   - **TikTok:** idem; atenção a **@ parecidos** (underscore, números).
   - **YouTube:** busca por nome; validar **canal oficial** (inscritos, “About”, links).
   - **X:** busca por nome e por variações do @ (sem acento, nome+sobrenome colado).
4. **Fontes secundárias (com critério)** — Matérias, **página do reality**, **release de agência**, **Famous Birthdays / similar**: só como **pista** até abrir o perfil e confirmar; não usar como única prova.
5. **Cross-check** — Se achou IG e TT, ver se **mesma foto de perfil** ou **mesmo link** na bio em ambos; se um canal YouTube cita o @ do TT, subir confiança.

---

## Checklist de confirmação (por candidato a perfil)

Marcar mentalmente ou em nota interna:

| Critério | OK? |
|----------|-----|
| Nome ou apelido coerente com o briefing | |
| Foto / estética alinhada com outras redes já confirmadas | |
| Bio ou link aponta para outra rede já confirmada ou para site oficial do projeto | |
| Número de seguidores e tipo de conteúdo fazem sentido para o “tamanho” esperado do talento | |
| Não é fã-clube, paródia, homônimo de outro estado/país | |

Se **2 ou mais** critérios falham, **não** usar sem evidência extra.

---

## Por rede — o que registrar no dossiê

| Rede | O que procurar | Se não achar |
|------|----------------|--------------|
| **Instagram** | @ oficial; às vezes igual ao TT | “Sem IG público identificado” ou “conta privada — não entra no painel SB” |
| **TikTok** | @ (pode diferir do IG) | Idem |
| **YouTube** | @handle ou nome do canal + URL | Canal inexistente ou só reuploads de terceiros — documentar |
| **X** | @; seguidores + ativo/inativo (ver playbook / README métricas) | Conta inexistente, só homônimo político, etc. |

Handles vazios no `### Handles` do `.md` são aceitáveis se a nota no perfil ou na pesquisa explicar o porquê.

---

## Registo no repositório

- **`dossier_*.md`** → `### Handles` com os @ **confirmados**; na **Narrativa** ou **eixo**, uma frase sobre **homônimos** ou **lacunas** se for relevante para o cliente.
- **`research/`** (opcional) → ficheiro curto `HANDLES_NOME_creator.md` com URLs visitadas e data, para auditoria interna.

---

## Relação com outros documentos

- **Brand safety e busca aberta:** `METODO_BRAND_SAFETY_LOTERIAS2026.md`
- **OSINT suplementar** (yt-dlp, Sherlock, etc.): mesma pasta, secção *Ferramentas open source* no método Brand Safety
- **Playbook geral:** `PLAYBOOK_DOSSIES.md` (raiz) — fluxo de entrega e métricas (SB, Upfluence, X manual)
