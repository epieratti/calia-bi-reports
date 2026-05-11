#!/usr/bin/env python3
"""Reescreve intro + eixos dos 25 perfis (exceto Raquel e Paulo, já feitos).

Combina substituições de texto seguras (regex que não tocam em atributos)
com o condensador por fragmento HTML de condense_dossier_framework_full.

Uso: python3 tools/apply_profile_rewrites_25.py
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"
EXTRACT_DIR = ROOT / "fragments" / "_extract"

# Carrega condense_html_fragment do módulo existente
_spec = importlib.util.spec_from_file_location(
    "_cond", ROOT / "condense_dossier_framework_full.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
condense_html_fragment = _mod.condense_html_fragment

SKIP = {"raquel-real", "paulo-victor-freitas"}

# Cortes de texto em HTML (padrões só em texto visível, não em atributos).
TEXT_SUBS: list[tuple[str, str]] = [
    (r" no que vimos\.", " na coleta."),
    (r" no que vimos;", " na coleta;"),
    (r" no que vimos,", " na coleta,"),
    (r" nas fontes que vimos", " na coleta"),
    (r" nas fontes consultadas", " na coleta"),
    (r" nas fontes desta coleta", " na coleta"),
    (r" nas fontes abertas", " na imprensa aberta"),
    (r"Não achamos publi", "Sem publi"),
    (r"Não achamos ligação", "Sem ligação"),
    (r"Não achamos engajamento", "Sem engajamento"),
    (r"Não achamos posicionamento", "Sem posicionamento"),
    (r"Não achamos contrato", "Sem contrato"),
    (r"Não achamos vínculo", "Sem vínculo"),
    (r"Não achamos episódio", "Sem episódio"),
    (r"Não achamos marcas", "Sem marcas"),
    (r"Não achamos campanhas", "Sem campanhas"),
    (r"Não achamos publicidade", "Sem publicidade"),
    (r"Não localizada publi", "Sem publi"),
    (r"Não há filiação", "Sem filiação"),
    (r"Não há ", "Sem "),
    (r"Nada de polêmica", "Sem polêmica"),
    (r" — nada que ", "; nada que "),
    (r" — temas que ", "; temas que "),
    (r" — relevante se ", "; relevante se "),
    (r" — o risco ", "; o risco "),
    (r" — perfil de alta visibilidade, onde", "; alta visibilidade;"),
    (r"perfil de alta visibilidade, onde", "alta visibilidade;"),
    (r"Nos painéis de mercado", "Nos painéis"),
    (r"Nos painéis há", "Nos painéis,"),
    (r"Antes de fechar peça institucional, a agência deve entregar", "Para peça institucional, convém reunir"),
    (r"Qualquer checagem de identidade deve cruzar", "Checagens jurídicas devem cruzar"),
    (r" — lacuna comum", "; lacuna comum"),
    (r" — o peso real ", "; o peso real "),
    (r" — parceria com anunciante", "; parceria com anunciante"),
    (r" — validar contratos", "; validar contratos"),
    (r" — isso pode ser vantagem", "; pode ser vantagem"),
    (r" — o tom é ", "; o tom é "),
    (r" — não militância", "; sem militância"),
    (r" — comercial e donos da marca\.", ", comercial e donos da marca."),
    (r" — exemplo documentado:", ":"),
    (r" — relevante se o cliente", "; relevante se o cliente"),
    (r" — inclui séries", "; inclui séries"),
    (r" — não um caso isolado", "; não é caso isolado"),
    (r" — vários posts\)", "; vários posts)"),
]

TEXT_RES = [(re.compile(a, flags=re.IGNORECASE), b) for a, b in TEXT_SUBS]


def apply_text_subs(html: str) -> str:
    t = html
    for rx, rep in TEXT_RES:
        t = rx.sub(rep, t)
    return t


def pipeline_fragment(html: str) -> str:
    return condense_html_fragment(apply_text_subs(html))


def replace_section_content(html: str, sid: str, new_intro: str, new_axes: list[str]) -> str:
    m = re.search(rf"(<section id='{re.escape(sid)}'[\s\S]*?)(</section>)", html)
    if not m:
        raise SystemExit(f"secção não encontrada: {sid}")
    sec = m.group(1)
    # intro
    m_intro = re.search(
        r"(<p class='text-sm text-slate-600 mb-6[^']*'[^>]*>)([\s\S]*?)(</p>)", sec
    )
    if not m_intro:
        raise SystemExit(f"intro não encontrada: {sid}")
    sec2 = sec[: m_intro.start(2)] + new_intro + sec[m_intro.end(2) :]
    # eixos: substituir na ordem cada <p class='text-sm text-slate-700 leading-relaxed'>…</p>
    parts = new_axes[:]
    out_sec = sec2

    def repl_one(mo: re.Match[str]) -> str:
        if not parts:
            return mo.group(0)
        inner = parts.pop(0)
        return mo.group(1) + inner + mo.group(3)

    out_sec = re.sub(
        r"(<p class='text-sm text-slate-700 leading-relaxed'>)([\s\S]*?)(</p>)",
        repl_one,
        out_sec,
        count=len(new_axes),
    )
    if parts:
        raise SystemExit(f"sobraram eixos para {sid}: {len(parts)}")
    # Manter o sufixo após o </section> do perfil (o match não cobre o restante do arquivo).
    return html[: m.start(1)] + out_sec + m.group(2) + html[m.end() :]


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    for path in sorted(EXTRACT_DIR.glob("*.json")):
        sid = path.stem
        if sid in SKIP:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        intro = pipeline_fragment(data["intro"])
        axes = [pipeline_fragment(a) for a in data["axes"]]
        html = replace_section_content(html, sid, intro, axes)
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
