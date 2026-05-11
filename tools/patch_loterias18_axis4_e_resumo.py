#!/usr/bin/env python3
"""Insere o eixo 4 Loterias 18+ nos perfis 1–21 (estava ausente) e atualiza a coluna
Loterias 18+ da Tabela resumo com achados por creator (idempotente)."""

from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

# (eixo 4 — parágrafo no perfil, célula curta na tabela resumo)
DATA: list[tuple[str, str, str]] = [
    (
        "giovanna-pitel",
        "Ex-BBB e realities na TV aberta, com marcas de consumo adulto. Na coleta (abr./2026) não apareceu formato voltado a crianças nem indício de que menores componham parcela relevante da audiência-alvo para loterias; manter checagem na data da veiculação.",
        "Realities e marcas adultas; coleta abr./2026 sem indício de público infantil predominante.",
    ),
    (
        "rafael-gratta",
        "Canal massivo sobre saúde mental, hábitos e infoprodutos para adultos. Na coleta não há foco infantil nem sinal de que menores sejam fração relevante da audiência no critério Loterias 18+.",
        "Saúde/hábitos para adultos; coleta sem formato infantil nem audiência infantil relevante.",
    ),
    (
        "indio-behn",
        "Humor e personagens adultos (podcasts, TV). Na coleta não surgiu apelo sistemático a menores nem evidência de público infantil predominante.",
        "Humor adulto/personagens; coleta sem indício de audiência infantil predominante.",
    ),
    (
        "megh-melry",
        "Humor que envolve família e avó em cena; não é canal infantil. Painéis com base ampla e engajamento alto não indicam, por si, público infantil predominante — na coleta não houve sinal desse perfil para o critério loterias.",
        "Humor familiar em cena adulta; coleta sem sinal de público infantil predominante.",
    ),
    (
        "cleane-sampaio",
        "Forró e cena musical adulta; reality musical entre adultos. Na coleta não apareceu formato infantil nem indício de menores como fração relevante da audiência.",
        "Música/reality adulto; coleta sem apelo infantil relevante no critério 18+.",
    ),
    (
        "ivan-baron",
        "Pedagogia, acessibilidade e causas sociais com tom adulto; parcerias institucionais. Na coleta não surgiu produção voltada a criança como público-alvo nem audiência infantil predominante.",
        "Causas e público adulto; coleta sem foco infantil nem demos infantis relevantes.",
    ),
    (
        "mila-costa",
        "Humor sobre vida adulta e maternidade; crianças podem aparecer em rotina familiar sem configurar canal infantil. Na coleta não houve indício de público infantil predominante para loterias.",
        "Humor adulto/maternidade; coleta sem audiência infantil predominante.",
    ),
    (
        "cristian-wariu",
        "Comunicação sobre povos originários, território e direitos; público informado/adulto. Na coleta não surgiu formato infantil nem sinal de menores como fração relevante da audiência no critério 18+.",
        "Pauta originária/adulta; coleta sem público infantil predominante.",
    ),
    (
        "cereja",
        "Humor e cotidiano urbano (Salvador) para público jovem-adulto. Na coleta não apareceu apelo a menores como núcleo da audiência.",
        "Humor urbano adulto; coleta sem indício de audiência infantil predominante.",
    ),
    (
        "aline-costa",
        "Desafios e humor viral em TikTok; escala jovem. Na coleta não houve evidência de público infantil predominante nem de menores como fração relevante no critério loterias.",
        "Humor viral jovem; coleta sem público infantil predominante.",
    ),
    (
        "davi",
        "Humor em TikTok/YouTube com tração jovem. Na coleta não surgiu formato infantil nem indício de que crianças componham parcela relevante da audiência para campanha 18+.",
        "Humor jovem em redes; coleta sem audiência infantil predominante.",
    ),
    (
        "paula-mineira",
        "Humor regional e rotina adulta (Minas). Na coleta não apareceu foco em crianças como público-alvo nem sinal de audiência infantil predominante.",
        "Humor regional adulto; coleta sem público infantil predominante.",
    ),
    (
        "catraca-livre",
        "Marca editorial de notícias e cultura — alcance amplo na internet. Menores consomem notícias, mas o produto não mira criança como público central nem adota formatos infantis; na coleta o risco do critério Loterias 18+ por composição infantil da audiência permanece baixo frente ao restante do vetting.",
        "Notícias/cultura para público geral; coleta: baixo risco 18+ por audiência infantil (ver outros eixos).",
    ),
    (
        "julia-ferrari",
        "Atriz e humor de cotidiano adulto; parcerias de consumo. Na coleta não surgiu canal infantil nem indício de menores como fração relevante da audiência.",
        "Humor/cotidiano adulto; coleta sem público infantil predominante.",
    ),
    (
        "joao-vitor-mello",
        "Humor e cultura jovem-adulto (Play9). Na coleta não apareceu formato voltado a crianças nem sinal de audiência infantil predominante.",
        "Humor/cultura jovem; coleta sem público infantil predominante.",
    ),
    (
        "lorena-rufino",
        "Humor e vida pessoal adulta; campanhas de marca generalistas. Na coleta não houve foco infantil nem evidência de menores como fração relevante no critério 18+.",
        "Humor adulto; coleta sem audiência infantil predominante.",
    ),
    (
        "barbara-coura",
        "Humor curto com temas adultos; atenção a piadas sobre aposta (sátira — eixo Concorrência). Na coleta não surgiu apelo a menores como núcleo da audiência.",
        "Humor adulto; coleta sem público infantil predominante (calibrar apostas no brief).",
    ),
    (
        "raphael-vicente",
        "Humor ligado à comunidade da Maré e pautas urbanas adultas. Na coleta não apareceu formato infantil nem indício de público infantil predominante.",
        "Humor/comunidade adulta; coleta sem audiência infantil predominante.",
    ),
    (
        "rafael-saraiva",
        "Sketch com título \"Bet Kids\" (Porta dos Fundos) é ficção/humor adulto — não equivale a publi de aposta nem a canal infantil. Na coleta não houve sinal de menores como fração relevante da audiência no critério loterias.",
        "Sátira \"Bet Kids\" (adulto); coleta sem público infantil predominante.",
    ),
    (
        "pedro-ottoni",
        "Humor e streaming com referências adultas (UOL Splash). Na coleta não surgiu foco em crianças como público-alvo nem audiência infantil predominante.",
        "Humor adulto/streaming; coleta sem público infantil predominante.",
    ),
    (
        "ademara",
        "Humor e entretenimento com séries adultas (Netflix etc.); registro político na imprensa não muda o recorte 18+. Na coleta não apareceu formato infantil nem indício de menores como fração relevante da audiência.",
        "Humor/séries adultas; coleta sem público infantil predominante.",
    ),
    (
        "linnyke-alves",
        "Amostra mai./2026 (miniaturas TikTok + trecho Instagram): menores em várias miniaturas e séries recorrentes; possível tração de atenção juvenil — calibrar criativo e validar demos na veiculação.",
        "Miniaturas com menores recorrentes (mai./2026); validar demos na veiculação.",
    ),
    (
        "felipe-hatori",
        "Amostra mai./2026 (TikTok): sem menor em destaque nas miniaturas; humor adulto urbano; evento listado 18+ (Guia Floripa).",
        "TikTok mai./2026: sem menor em destaque; humor adulto; show 18+ citado.",
    ),
    (
        "julimara",
        "Amostra mai./2026 (TikTok): turismo/lifestyle; sem menor em destaque nas miniaturas.",
        "TikTok mai./2026: lifestyle; sem menor em destaque nas miniaturas.",
    ),
    (
        "raquel-real",
        "Humor adulto e podcast familiar no YouTube (não canal infantil). Amostra no X (11/05/2026): tom adulto; sem incentivo a jogo para menores.",
        "Humor adulto; YouTube familiar não infantil; X 11/05/2026 sem apelo a menores.",
    ),
    (
        "morgana-camila",
        "Desfile cívico com escolas (O Povo) — menores em material público que viralizou; YouTube com tom familiar. Eixo ganha peso com pista de cenário/audiência — validar demos.",
        "Menores no desfile (O Povo) + tom familiar; validar demos (moderado).",
    ),
    (
        "paulo-victor-freitas",
        "Humor adulto (g1); parkour/rap (Ness + g1) apontam jovem adulto, não público infantil. Na coleta não houve sinal de parcela relevante de menores na audiência.",
        "Humor adulto; apelo jovem (parkour/rap); coleta sem público infantil predominante.",
    ),
]

AXIS4_BLOCK = (
    "<div class='rounded border border-slate-200 p-4 bg-white'>"
    "<p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+ (audiência)</p>"
    "<p class='text-sm text-slate-700 leading-relaxed'>{inner}</p></div>"
)

END_MARK = "</p></div></div></section>"
INSERT_END = "</p></div>"  # fecha célula 3; depois vem nova célula + fecha grid + section


def inject_axis4(html: str) -> str:
    for sid, inner, _ in DATA[:21]:
        marker = f"<section id='{sid}'"
        a = html.find(marker)
        if a == -1:
            raise SystemExit(f"secção não encontrada: {sid}")
        b = html.find("<section id='", a + len(marker))
        if b == -1:
            raise SystemExit(f"fim de secção não encontrado: {sid}")
        sec = html[a:b]
        if "4. Loterias 18+" in sec:
            continue
        if sec.count(END_MARK) != 1:
            raise SystemExit(f"marcador final ambíguo em {sid}")
        block = AXIS4_BLOCK.format(inner=inner)
        sec2 = sec.replace(END_MARK, INSERT_END + block + "</div></section>", 1)
        html = html[:a] + sec2 + html[b:]
    return html


def patch_table(html: str) -> str:
    anchor = "Uma linha por creator"
    pos = html.find(anchor)
    if pos == -1:
        raise SystemExit("âncora da tabela não encontrada")
    t0 = html.find("<tbody>", pos)
    t1 = html.find("</tbody>", t0)
    if t0 == -1 or t1 == -1:
        raise SystemExit("tbody da resumo não encontrado")
    body = html[t0 : t1 + len("</tbody>")]
    rows = re.findall(r"<tr>(.*?)</tr>", body, flags=re.S)
    if len(rows) != len(DATA):
        raise SystemExit(f"esperadas {len(DATA)} linhas, encontrei {len(rows)}")
    new_rows: list[str] = []
    for row_html, (_, _, cell) in zip(rows, DATA, strict=True):
        tds = re.findall(r"(<td[^>]*>)(.*?)(</td>)", row_html, flags=re.S)
        if len(tds) != 6:
            raise SystemExit("linha sem 6 colunas")
        open0, inner0, close0 = tds[0]
        parts = [f"<tr>{open0}{inner0}{close0}"]
        for i in range(1, 5):
            o, inn, c = tds[i]
            parts.append(f"{o}{inn}{c}")
        o5, _, c5 = tds[5]
        # idempotência: se já não for o texto genérico, só reescreve se ainda tiver o boilerplate antigo
        parts.append(f"{o5}{cell}{c5}")
        new_rows.append("".join(parts) + "</tr>")
    new_body = "<tbody>" + "".join(new_rows) + "</tbody>"
    return html[:t0] + new_body + html[t1 + len("</tbody>") :]


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    html2 = inject_axis4(html)
    html3 = patch_table(html2)
    HTML_PATH.write_text(html3, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
