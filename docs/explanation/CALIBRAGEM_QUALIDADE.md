# Calibragem de qualidade dos dossiês

Complemento a **`PLAYBOOK_DOSSIES.md`** → *Qualidade da redação* e *Calibragem de qualidade*. Objetivo: **decisão confiável** e **calibragem explícita** entre projetos e redatores.

---

## 1. Definição de prova por eixo (por cliente)

Sem isto, “concorrência” e “política” viram **opinião média**.

**No briefing**, responda em texto plano (ou use `quality_calibration.definicoes_prova` no front matter):

| Eixo | Perguntas-guia |
|------|-----------------|
| **Concorrência** | O que conta como **conflito real**? (Publi paga / parceria explícita vs menção casual / evento educativo?) Bet no **nome do curso** vs publi de **casa de aposta**? |
| **Polêmicas** | O que é **relevante para imagem** vs ruído de internet? Denúncia com matéria vs comentário anônimo? |
| **Política** | **Filiação partidária** explícita vs **pauta sensível** vs humor/piada pontual? |

**Checklist antes de fechar:** cada **alto/moderado** no texto está alinhado a estas definições?

---

## 2. Janela de tempo e delta

- **`meta.periodo`** — vigência da leitura (“Março–abril/2026”, “Coleta em DD/MM/AAAA”).
- **Revisão:** parágrafo curto **“O que mudou desde a versão anterior”** — novos nomes, novos fatos, só métricas, correção de homônimo.  
  Campos: `quality_calibration.delta_vs_entrega_anterior` ou bloco em `consolidated_narrative` / `executive_summary`.

---

## 3. Segunda leitura — advogado do diabo (QA)

Na etapa **6 — QA** (ou no fim do **4b**), por perfil com risco não trivial:

> *Se eu tivesse que **impedir** a contratação deste nome, que **frases** deste dossiê eu usaria? Estão **sólidas** (data + fonte + escopo) ou **vagas**?*

Corrigir frases que dependem de “parece”, “talvez”, “pode gerar” **sem** o porquê na mesma respiração.

---

## 4. Nível de confiança em afirmações sensíveis

Onde o fato **não** for óbvio ou houver **uma** fonte só, acrescentar **uma frase curta**:

- **Alta** — duas fontes independentes ou documento inequívoco.  
- **Média** — uma matéria séria ou padrão claro nas redes.  
- **Baixa** — rumor, fórum, ou leitura inferida.

Ex.: *“Confiança: média — uma matéria de veículo X; não achamos segunda fonte.”*

---

## 5. Perfil institucional (página/marca) vs pessoa física

- Listar nomes em **`briefing.perfis_institucionais`** no front matter (array).
- Na **narrativa** ou no **pedido**, uma linha: *“Para páginas institucionais, ‘política’ refere-se a …; não exige filiação individual.”*

Evita comparar **Catraca Livre** com **influenciador pessoa física** no mesmo critério sem aviso.

---

## 6. “Não consta” com método (no corpo)

Quando o vazio for **sensível** (ex.: polêmica em nome grande), **não** basta “não achamos”.

Incluir **uma linha**: o que foi tentado — *“Busca em IG/TT + nome + ‘aposta’ até DD/MM; imprensa com `site:` veículos parceiros.”*

---

## 7. Painéis (métricas) vs narrativa

Se **número** e **texto** parecem contraditórios:

- **Reconciliar** numa frase (*“Engajamento alto em formato de vídeo curto; no eixo de polêmica ‘quieto’ = sem episódio imprensa no período.”*), **ou**  
- **Corrigir** o texto que estava errado.

Não deixar divergência sem comentário — o cliente nota.

---

## 8. Tom por bloco

| Bloco | Objetivo de leitura |
|-------|---------------------|
| **Leitura rápida** | Decisão e ordem de prioridade em **~60 s** — bullets fortes, pouca nuance. |
| **Perfis** | **Prova + nuance** — parágrafos, eixos, exceções. |
| **Tabela resumo** | **Scan** — não repetir o perfil inteiro; complementar. |

---

## 9. Pós-entrega — glossário vivo

A cada projeto ou trimestre, perguntar a **atendimento/cliente**:

> *Qual **frase** ou **termo** quase foi **mal interpretado**?*

Registrar em nota interna (`research/` ou wiki): *“Neste cliente, ‘bet’ no nome do produto ≠ publi de casa de apostas.”* — alimenta o **próximo** dossiê.

---

## Referência rápida no `.md` (YAML opcional)

```yaml
quality_calibration:
  data_corte_coleta: "DD/MM/AAAA"
  delta_vs_entrega_anterior: "Primeira entrega." # ou texto de revisão
  definicoes_prova:
    concorrencia: "…"
    polemicas: "…"
    politica: "…"
briefing:
  perfis_institucionais: []
```

O gerador **não** precisa destes campos para renderizar; servem para **briefing documentado** e para **agentes** seguirem o mesmo padrão.
