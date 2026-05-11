#!/usr/bin/env python3
"""
Substitui o bloco introdutório (texto, não só estrutura) de cada um dos 27
perfis do dossiê squad por redações manuais alinhadas em tom e extensão.
Uma única execução esperada; idempotente se o HTML já estiver igual.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HTML_DEFAULT = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

DIV_MARKER = "<div class='text-sm text-slate-600 mb-6 leading-relaxed space-y-3 text-pretty'>"
GRID = "</div><div class='grid md:grid-cols-2 gap-4'>"

P = "<p class='m-0 leading-relaxed text-slate-600'>"

# Uma frase + uma frase; tom institucional, pt-BR; sem listas longas.
NEW_INNER: dict[str, str] = {
    "giovanna-pitel": f"{P}Influenciadora e apresentadora; trajetória no BBB com voz crítica e formação em Serviço Social, hoje entre realities na TV e campanhas de consumo e causas. Alta exposição na mídia de celebridades — convém cruzar falas e publicidades com agenda oficial do talento na data da veiculação.</p>",
    "rafael-gratta": f"{P}Médico com canal de saúde mental e performance (ansiedade, foco e hábitos), cursos digitais e livro de grande circulação. Entre os maiores alcances do squad; mensagens sobre saúde e resultados exigem checagem de promessas e de matérias de reputação antes da peça.</p>",
    "indio-behn": f"{P}Humorista e ator, conhecido por personagens como a Dra. Rosângela, em tom satírico sobre costumes e “good vibes”. Participa de podcasts de massa; pauta é entretenimento com crítica leve de comportamento, com público misto inclusive famílias.</p>",
    "megh-melry": f"{P}Criadora de humor familiar (incluindo a figura da avó) que consolidou base forte no vídeo curto; nos painéis o TikTok pesa mais que o YouTube institucional. Perfil de lifestyle e entretenimento leve — validar canal prioritário e números em Métricas nas redes.</p>",
    "cleane-sampaio": f"{P}Cantora e compositora de forró e cena nordestina, com passagem por reality musical e presença em shows e redes. Humor, sotaque e parcerias regionais com marcas de alimento e cultura aparecem em imprensa local e releases.</p>",
    "ivan-baron": f"{P}Pedagogo e ativista por inclusão da pessoa com deficiência, recorrente em campanhas públicas e eventos nacionais, com conteúdo sobre vida com paralisia cerebral amplamente citado na imprensa. Exposição alta em diversidade; há posicionamento político explícito nas redes — ler o eixo Política na veiculação.</p>",
    "mila-costa": f"{P}Criadora do <strong class=\"font-semibold text-slate-900\">No Caso Mila</strong>: humor sobre vida adulta, maternidade e contraste regional (Cearense em Recife). Colunas e parcerias com marcas e veículos no Nordeste; audiência engajada no Instagram, em geral com baixo risco de polêmica política em peças neutras.</p>",
    "cristian-wariu": f"{P}Comunicador Xavante (MT) focado em povos originários, território e combate a estereótipos, presente em debates ambientais e de direitos humanos. Voz visível da pauta indígena online; parcerias institucionais pedem sensibilidade a ataques de ódio e coerência de mensagem ambiental.</p>",
    "cereja": f"{P}Criadora baiana de humor e rotina ligada a Salvador e a “notícias boas”. Alcance menor que megafenômenos do squad, o que pode servir a campanhas regionais ou de nicho — confirmar carteira e exclusividades se o briefing exigir.</p>",
    "aline-costa": f"{P}Persona <strong class=\"font-semibold text-slate-900\">Aline com Certeza</strong>: humor e desafios em um dos maiores TikToks do squad nos painéis. Há homônimos e jornalistas com nome parecido — homologar com canal oficial deste dossiê e CPF, não com busca só por nome.</p>",
    "davi": f"{P}Talento digital conhecido como <strong class=\"font-semibold text-slate-900\">davizoa</strong>; tração concentrada em TikTok e YouTube com pouca matéria de imprensa na proporção do alcance, padrão comum de micro viral. Para peça institucional, reunir bio, histórico de publi e dados para buscas adicionais com segurança.</p>",
    "paula-mineira": f"{P}Criadora de humor com forte âncora em Minas Gerais, rotina e identidade regional. Imprensa local cita parcerias com comércio, eventos e prêmios de influência — perfil adequado a campanhas regionais no Sudeste com linguagem leve.</p>",
    "catraca-livre": f"{P}Página digital de notícias e cultura urbana: fala a marca e a redação, não uma pessoa física. Histórico público cobre ecossistema de apostas e posicionamento editorial claro — avaliar compatibilidade com produto de loteria e risco de marca antes de qualquer vinculação.</p>",
    "julia-ferrari": f"{P}Atriz e criadora de humor de cotidiano; entrevistas especializadas citam parcerias com marcas de massa. Tratar audiência e publicidade com base no material linkado no perfil e nos quatro eixos deste dossiê.</p>",
    "joao-vitor-mello": f"{P}Criador de humor e cultura digital com presença em vídeos e projetos do ecossistema <strong class=\"font-semibold text-slate-900\">Play9</strong>. Pauta é entretenimento; validar handles ativos e portfólio de publi no corpo do perfil e em Métricas nas redes.</p>",
    "lorena-rufino": f"{P}Criadora de humor e vida pessoal com campanhas documentadas na imprensa (incluindo Fanta/Europa) e menção em conteúdo acadêmico sobre creators. Checar disponibilidade e conflitos de categoria com o briefing da peça.</p>",
    "barbara-coura": f"{P}Humor em vídeo curto; matérias e painéis citam parcerias com grandes marcas de streaming, beleza e varejo. Ao aproximar de loteria, monitorar humor que brinca com temas sensíveis no eixo Concorrência.</p>",
    "raphael-vicente": f"{P}Humor em vídeo ligado à <strong class=\"font-semibold text-slate-900\">Maré</strong> (RJ); listagens e matérias citam marcas nacionais em telecom, consumo e apps. Pauta mistura entretenimento e periferia — rever o eixo de segurança pública/comunidade na veiculação.</p>",
    "rafael-saraiva": f"{P}Integrante do <strong class=\"font-semibold text-slate-900\">Porta dos Fundos</strong> e com atuação em novela da Globo. O ponto sensível costuma ser humor com jogos/apostas em títulos de sketches — ver eixo Concorrência.</p>",
    "pedro-ottoni": f"{P}Criador de humor com foco em streaming e cultura pop; veículos de entretenimento resumem parcerias com plataformas. Pauta leve; confirmar alinhamento de marca e faixa etária do conteúdo com a peça.</p>",
    "ademara": f"{P}Humorista com série documental <strong class=\"font-semibold text-slate-900\">Sem Filtro</strong> na Netflix e presença em produtos do ecossistema Globoplay/Play9. Alto reconhecimento em entretenimento; checar menções políticas recentes na imprensa ao montar o cronograma.</p>",
    "linnyke-alves": f"{P}Comediante de vídeo curto com personagens de rua, com forte engajamento no TikTok e no Instagram. Houve destaque na imprensa por mobilização solidária em 2024 — cuidado se a narrativa envolver menor em situação de vulnerabilidade.</p>",
    "felipe-hatori": f"{P}Comediante e roteirista; audiência concentrada em TikTok, Instagram e YouTube, com stand-up próprio. Portfólio público associa o nome a campanhas com grandes marcas financeiras, tecnologia e bebidas — validar conflitos de categoria e exclusividades no briefing.</p>",
    "julimara": f"{P}Criadora do <strong class=\"font-semibold text-slate-900\">Triângulo Mineiro</strong> (MG), com foco em turismo, trilhas e lifestyle regional. Alcance maior no Instagram, com TikTok e canal temático no YouTube; perfil regional — confirmar status comercial e janelas de publi no briefing.</p>",
    "raquel-real": f"{P}Comediante e apresentadora cearense, com trabalhos em humor premium e currículo agregado em listas da moda e entretenimento. No X há sátira sobre apostas e política; buscas por nome no estado misturam figura política homônima — homologar sempre por handle e URL do perfil.</p>",
    "morgana-camila": f"{P}Criadora cearense conhecida por <strong class=\"font-semibold text-slate-900\">Arrasa na Major</strong>, com crônicas em veículos regionais e entrevistas longas em YouTube. Pauta mistura humor, maternidade e cotidiano; eventual menção a menores em conteúdo de massa entra no eixo Loterias 18+.</p>",
    "paulo-victor-freitas": f"{P}Criador potiguar de humor sobre o Nordeste; biografia pública associa parkour, rap e publicidade (casting e matérias nacionais). Há menções à sociedade de vigilância eletrônica e variação de grafia do nome na imprensa — consolidar identidade por handle e fontes citadas no perfil.</p>",
}


def apply(html: str) -> tuple[str, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]
    n = 0
    for slug, inner in NEW_INNER.items():
        pat = re.compile(
            rf"(<section id='{re.escape(slug)}'[\s\S]*?{re.escape(DIV_MARKER)})([\s\S]*?)({re.escape(GRID)})",
        )

        def repl(_m: re.Match[str], inner=inner) -> str:
            return _m.group(1) + inner + _m.group(3)

        chunk2, c = pat.subn(repl, chunk, count=1)
        if c:
            n += c
            chunk = chunk2
    return head + chunk + tail, n


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DEFAULT
    html = path.read_text(encoding="utf-8")
    html2, n = apply(html)
    if n != len(NEW_INNER):
        print(f"Aviso: substituídos {n} de {len(NEW_INNER)} perfis.", file=sys.stderr)
    if html2 == html:
        print("Nada alterado.")
        return 0
    path.write_text(html2, encoding="utf-8")
    print(f"OK: {n} textos introdutórios reescritos em {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
