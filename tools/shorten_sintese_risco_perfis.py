#!/usr/bin/env python3
"""
Enxuga o texto do badge «Síntese de risco» em cada perfil (#perfis): nível
(Baixo / Moderado / …) e complemento mínimo só quando faz diferença.
Idempotente.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HTML_DEFAULT = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

# Texto exato atual → novo (só #perfis)
MAP: dict[str, str] = {
    "Baixo a moderado — alta visibilidade na mídia": "Baixo a moderado",
    "Moderado — reputação em conteúdo de saúde e vendas": "Moderado",
    "Moderado — política e causas explícitas": "Moderado",
    "Baixo a moderado — pauta indígena e ambiental": "Baixo a moderado",
    "Poucas matérias na imprensa aberta; risco documentado parece baixo": "Baixo",
    "Baixo — atenção a humor com tema de aposta (sátira)": "Baixo — humor/aposta (sátira)",
    "Baixo a moderado — exposição em segurança pública / comunidade (mídia)": "Baixo a moderado",
    'Baixo — atenção ao sketch &quot;Bet Kids&quot; (só o título)': 'Baixo — sketch "Bet Kids"',
    "Baixo a moderado — encontro com o presidente em 2023 noticiado na imprensa (avaliar narrativa em 2026)": "Baixo a moderado",
    "Baixo — humor adulto; no X, sátira sobre apostas e política (calibrar \"bet\"; ver eixos); homônimo político na busca (só contexto)": "Baixo — X/apostas",
    "18+ moderado — pista: menores no desfile; validar audiência": "18+ moderado",
    "Moderado — pauta social + Máxima; Loterias 18+: sem público infantil predominante": "Moderado",
}

PAT = re.compile(
    r"(Síntese de risco</span><span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right[^>]+'>)([^<]+)(</span>)",
)


def apply(html: str) -> tuple[str, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        old = m.group(2)
        new = MAP.get(old, old)
        if new != old:
            n += 1
        return m.group(1) + new + m.group(3)

    chunk2 = PAT.sub(repl, chunk)
    return head + chunk2 + tail, n


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DEFAULT
    html = path.read_text(encoding="utf-8")
    html2, n = apply(html)
    if html2 == html:
        print("Nada alterado.")
        return 0
    path.write_text(html2, encoding="utf-8")
    print(f"OK: {n} sínteses enxugadas em {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
