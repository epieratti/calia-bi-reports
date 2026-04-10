# Prompts para agentes de IA (Calia BI Reports)

Use com o repositório aberto. Idioma da **resposta ao usuário:** **pt-BR**. **Conteúdo do dossiê:** **pt-BR** salvo pedido explícito em contrário.

**Coordenação entre agentes:** ver [`MULTI_AGENTES.md`](MULTI_AGENTES.md). **Calibragem de qualidade:** [`CALIBRAGEM_QUALIDADE.md`](CALIBRAGEM_QUALIDADE.md).

---

## 0. Briefing do cliente + pipeline obrigatório (colar no início)

```
[Cole aqui o bloco CONTRATO completo de docs/INICIO_AGENTE.md §7]

[Briefing bruto do cliente abaixo]
```

---

## 1. Fechar briefing a partir de texto solto

```
Com base no PLAYBOOK_DOSSIES.md §1, extraia um briefing estruturado desta mensagem.
Marque o que falta nos itens (E) e (C) e faça as perguntas mínimas ao usuário.
Não invente pasta, senha ou modo A/B/C. Não execute pesquisa pesada antes disso.
```

---

## 2. Síntese crítica pós-coleta (etapa 4b)

```
Leia o material que coletei (colar ou caminhos dos arquivos). Segundo PLAYBOOK_DOSSIES.md
«Síntese crítica e arquitetura da entrega», devolva:
(1) o que entra no dossiê vs fora de escopo,
(2) ordem das seções,
(3) se precisa gráfico ou painel executivo,
(4) riscos de credibilidade ou homônimo.
Em bullets, antes de escrever o .md final.
```

---

## 3. Humanizar parágrafo sem perder fatos

```
Reescreva o parágrafo abaixo para o público planejamento/atendimento/cliente:
humanizado, sucinto, completo e autocontido (sem exigir clique em link).
Mantenha todos os fatos e datas; se houver URL, mantenha como markdown [rótulo](url).
```

---

## 4. Checagem de evidência

```
Para cada afirmação sensível abaixo, diga se falta (a) data (b) fonte nomeada (c) hyperlink
quando existir URL. Liste só o que estiver incompleto segundo PLAYBOOK_DOSSIES.md
«Documento autocontido e links».
```

---

## 5. Desambiguação de homônimo

```
Nome: [X]. Handles candidatos: [lista]. Briefing: [contexto].
Segundo METODO_DESCOBERTA_PERFIS_CREATORS.md, quais checks faltam para confirmar
que é a mesma pessoa? Que perguntas devo fazer ao usuário?
```

---

## 6. Montar comando de entrega

```
Gere o comando exato: make dossie-entregar MD=... DEST=...
a partir do briefing (caminhos relativos à raiz do repo calia-bi-reports).
Inclua VARIANT squad_13 ou squad_8 se aplicável.
```

---

## 7. Preencher calibragem no front matter (modo B)

```
Com base no briefing abaixo, escreva o bloco YAML `quality_calibration` e `briefing.perfis_institucionais`
conforme docs/CALIBRAGEM_QUALIDADE.md. Texto plano nas strings. Se for revisão, inclua delta_vs_entrega_anterior.

[Briefing ou bullet points do cliente]
```

---

## 8. Advogado do diabo (QA por perfil)

```
Para o perfil «NOME» neste trecho do dossiê:
[Colar síntese de risco + os 3 eixos]

Liste 3 argumentos que um crítico usaria CONTRA contratar esta pessoa.
Para cada um, diga se o texto atual sustenta o risco (sim/não) e o que falta (fonte, data, nuance).
Idioma: pt-BR.
```

---

## 9. Reconciliar painel (métricas) com narrativa

```
Instagram (ou outra rede) mostra: [colar linha do painel ou números].
A narrativa diz: [colar frase].

Escreva UMA frase de reconciliação para o eixo ou nota de rodapé, ou diga qual texto está errado e como corrigir.
```
