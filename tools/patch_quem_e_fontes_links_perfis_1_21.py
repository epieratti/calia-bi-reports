#!/usr/bin/env python3
"""Insere links dossier-source-link nos intros dos perfis 1–27 e alinha o bloco Redes do lote 3.

- Perfis 1–21: textos com duas fontes públicas cada (idempotente).
- Perfis 22–27: mesma convenção, preenchendo intros que estavam sem links.
- Raquel Real, Morgana Camila e Paulo Victor Freitas: remove rodapés longos
  dos cards do snapshot local (Redes · handles), alinhando ao padrão visual
  dos perfis anteriores (números permanecem; detalhes seguem em Métricas).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HTML_DEFAULT = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"
DIV_MARKER = "<div class='text-sm text-slate-600 mb-6 leading-relaxed space-y-3 text-pretty'>"
GRID = "</div><div class='grid md:grid-cols-2 gap-4'>"
P = "<p class='m-0 leading-relaxed text-slate-600'>"


def L(url: str, label: str) -> str:
    return (
        f'<a class="dossier-source-link" href="{url}" '
        f'target="_blank" rel="noopener noreferrer">{label}</a>'
    )


INNER_1_21: dict[str, str] = {
    "giovanna-pitel": f"{P}Influenciadora e apresentadora; a passagem pelo {L('https://gshow.globo.com/realities/bbb/bbb-24/participantes/giovanna-pitel/', 'BBB 24 — página no Gshow')} consolidou voz crítica com formação em Serviço Social, hoje entre realities na TV e campanhas de consumo e causas. Alta exposição na mídia — ver também {L('https://gshow.globo.com/artistas/giovanna-pitel/', 'ficha de artista no Gshow')}; convém cruzar falas e publicidades com agenda oficial do talento na data da veiculação.</p>",
    "rafael-gratta": f"{P}Médico com canal no {L('https://www.youtube.com/@rafaelgratta', 'YouTube (@rafaelgratta)')} sobre saúde mental e performance (ansiedade, foco e hábitos), cursos digitais e obra com a {L('https://intrinseca.com.br/autor/rafael-gratta/', 'Intrínseca — página do autor')}. Entre os maiores alcances do squad; mensagens sobre saúde e resultados exigem checagem de promessas e de matérias de reputação antes da peça.</p>",
    "indio-behn": f"{P}Humorista e ator, conhecido por personagens como a Dra. Rosângela; reportagem do {L('https://www.correiodopovo.com.br/cadernodesabado/%C3%ADndio-behn-fen%C3%B4meno-dos-personagens-do-feed-e-do-palco-1.879228', 'Correio do Povo')} resume a trajetória e o {L('https://www.indiobehn.com.br/', 'site oficial')} consolida agenda pública. Participa de podcasts de massa; pauta é entretenimento com crítica leve de comportamento, com público misto inclusive famílias.</p>",
    "megh-melry": f"{P}Criadora de humor familiar (incluindo a figura da avó) que consolidou base forte no vídeo curto; o {L('https://meghmelry.com.br/', 'site da criadora')} descreve formato e parcerias, e matéria no {L('https://www.opovo.com.br/vidaearte/2023/03/31/webserie-sobre-rio-sao-francisco-estreia-sabado-no-canal-da-fdr.html', 'O Povo')} contextualiza projetos na mídia. Nos painéis o TikTok pesa mais que o YouTube institucional — validar canal prioritário em Métricas nas redes.</p>",
    "cleane-sampaio": f"{P}Cantora e compositora de forró e cena nordestina; a passagem pelo {L('https://gshow.globo.com/realities/the-voice-brasil/2020/noticia/cleane-sampaio-conta-o-que-sentiu-ao-vencer-a-votacao-do-publico-meu-coracao-quase-saiu-pela-boca.ghtml', 'The Voice Brasil — Gshow')} serve como âncora pública, com ficha em {L('https://gshow.globo.com/artistas/cleane-sampaio/', 'Gshow Artistas')}. Humor, sotaque e parcerias regionais com marcas de alimento e cultura aparecem em imprensa local e releases.</p>",
    "ivan-baron": f"{P}Pedagogo e ativista por inclusão da pessoa com deficiência, recorrente em campanhas públicas e eventos nacionais; a {L('https://pt.wikipedia.org/wiki/Ivan_Baron', 'Wikipédia')} resume a trajetória e o {L('https://g1.globo.com/rn/rio-grande-do-norte/noticia/2023/01/02/quem-e-ivan-baron-conheca-o-influencer-potiguar-que-subiu-a-rampa-do-planalto-com-lula.ghtml', 'G1 (RN)')} documenta exposição política reconhecida. Ler o eixo Política na veiculação.</p>",
    "mila-costa": f"{P}Criadora do <strong class=\"font-semibold text-slate-900\">No Caso Mila</strong>: humor sobre vida adulta, maternidade e contraste regional; texto no {L('https://diariodonordeste.verdesmares.com.br/estilo-de-vida/sisi/de-concurseira-a-influencer-conheca-mila-costa-a-cearense-que-mostra-seu-dia-a-dia-com-humor-1.3088698', 'Diário do Nordeste')} apresenta a persona e o {L('https://g1.globo.com/podcast/escuta-que-o-filho-e-teu/noticia/2022/05/26/o-grande-diferencial-do-pai-e-da-mae-e-o-descanso-mental-diz-mila-costa.ghtml', 'podcast do G1')} ajuda a homologar tom. Em geral, baixo risco de polêmica política em peças neutras.</p>",
    "cristian-wariu": f"{P}Comunicador Xavante (MT) focado em povos originários; a {L('https://www.bbc.com/portuguese/brasil-46427800', 'BBC News Brasil')} registrou o trabalho de combate a estereótipos e a {L('https://pt.wikipedia.org/wiki/Cristian_Wariu', 'Wikipédia')} consolida biografia pública. Parcerias institucionais pedem sensibilidade a ataques de ódio e coerência de mensagem ambiental.</p>",
    "cereja": f"{P}Criadora baiana de humor e rotina ligada a Salvador; matérias como a do {L('https://www.bahianoticias.com.br/cultura/noticia/38708-perfis-baianos-de-humor-fazem-sucesso-no-instagram-durante-a-pandemia', 'Bahia Notícias')} e o {L('https://letsgobahia.com.br/noticia/default/influencer-cereja-percorre-ruas-de-salvador-atras-de-noticias-positivas', 'Let’s Go Bahia')} descrevem o formato de “notícias boas”. Alcance menor que megafenômenos do squad — confirmar carteira se o briefing exigir.</p>",
    "aline-costa": f"{P}Persona <strong class=\"font-semibold text-slate-900\">Aline com Certeza</strong>: humor e desafios em um dos maiores TikToks do squad nos painéis; o {L('https://pt.famousbirthdays.com/people/aline-com-certeza.html', 'Famous Birthdays (referência)')} agrega biografia agregada e o {L('https://www.threads.com/@comcertezaaline', 'Threads (@comcertezaaline)')} espelha o handle homologado em produto Meta. Homologar sempre com canal oficial deste dossiê e CPF, não com busca só por nome.</p>",
    "davi": f"{P}Talento digital conhecido como <strong class=\"font-semibold text-slate-900\">davizoa</strong>; âncoras públicas no {L('https://www.youtube.com/@davizoa', 'YouTube (@davizoa)')} e no {L('https://www.tiktok.com/@davizoa', 'TikTok (@davizoa)')} sustentam tração com pouca matéria de imprensa na proporção do alcance. Para peça institucional, reunir bio, histórico de publi e dados para buscas adicionais com segurança.</p>",
    "paula-mineira": f"{P}Criadora de humor com forte âncora em Minas Gerais; a {L('https://www.portalondasul.com.br/tag/paula-mineira/', 'tag no Portal Onda Sul')} reúne matérias locais e o {L('https://jornaldebrasilia.com.br/blogs-e-colunas/analice-nicolau/minas-se-destaca-com-sua-nova-safra-de-humoristas/', 'Jornal de Brasília')} cita humor mineiro em ascensão. Perfil adequado a campanhas regionais no Sudeste com linguagem leve.</p>",
    "catraca-livre": f"{P}Página digital de notícias e cultura urbana: o {L('https://www.catracalivre.com.br/', 'site da Catraca Livre')} apresenta a marca; para o ecossistema de apostas, há exemplos como o {L('https://catracalivre.com.br/noticias/uplinko-fashion-tv-guia-completo-2025/', 'guia Uplinko (2025)')}. Avaliar compatibilidade com produto de loteria antes de vincular.</p>",
    "julia-ferrari": f"{P}Atriz e criadora de humor de cotidiano; o {L('https://viralizou.net/internet/quem-e-julia-ferrari/', 'Viralizou — perfil')} sintetiza a carreira e o {L('https://gshow.globo.com/cultura-pop/viralizou/noticia/apos-viralizar-julia-ferrari-investe-na-carreira-de-atriz-e-cita-fase-de-incerteza-nao-era-niguem.ghtml', 'Gshow (quadro Viralizou)')} cobre a virada para atuação. Tratar audiência e publicidade com base nos quatro eixos deste dossiê.</p>",
    "joao-vitor-mello": f"{P}Criador de humor ligado ao ecossistema {L('https://play9.com.br/', 'Play9 (produtora)')}; a {L('https://capricho.abril.com.br/entretenimento/estes-sao-os-truques-de-enzo-baracho-e-joao-vitor-mello-para-engajar-mais', 'matéria na Capricho (Abril)')} descreve rotina e formatos. Validar handles e portfólio em Métricas nas redes.</p>",
    "lorena-rufino": f"{P}Criadora de humor e vida pessoal; a {L('https://www.correio24horas.com.br/entretenimento/influenciadora-lore-rufis-viaja-para-europa-e-brilha-em-campanha-global-0824', 'matéria no Correio 24 Horas')} documenta campanha Fanta/Europa, e a {L('https://hugogloss.uol.com.br/tag/lorena-rufino/', 'tag Hugo Gloss (UOL)')} agrega entrevistas. Checar conflitos de categoria com o briefing da peça.</p>",
    "barbara-coura": f"{P}Humor em vídeo curto; referência de mercado no {L('https://www.favikon.com/pt/blog/who-is-barbara-coura', 'Favikon')} e reportagem do {L('https://g1.globo.com/mg/minas-gerais/podcast/frango-com-quiabo/noticia/2024/04/01/com-quase-15-milhoes-de-seguidores-barbara-coura-quer-mergulhar-na-carreira-de-atriz.ghtml', 'G1 MG (2024)')} citam escala e marcas. Ao aproximar de loteria, monitorar eixo Concorrência.</p>",
    "raphael-vicente": f"{P}Humor em vídeo ligado à <strong class=\"font-semibold text-slate-900\">Maré</strong> (RJ); a {L('https://gutenberg.elastica.abril.com.br/especiais/raphael-vicente-tiktok-familia-entrevista/', 'entrevista na Elástica (Abril)')} contextualiza estilo e o {L('https://g1.globo.com/rj/rio-de-janeiro/noticia/2021/08/05/influenciador-da-mare-bomba-nas-redes-com-a-familia-em-campanha-contra-a-covid.ghtml', 'G1 RJ (2021)')} registra campanha de saúde na comunidade. Rever o eixo de segurança pública/comunidade na veiculação.</p>",
    "rafael-saraiva": f"{P}Integrante do {L('https://portadosfundos.com.br/elenco/rafael-saraiva/', 'Porta dos Fundos — elenco')} e com atuação em novela da Globo; o {L('https://diariogaucho.clicrbs.com.br/entretenimento/noticia/2024/07/cria-do-porta-dos-fundos-rafael-saraiva-celebra-estreia-em-novelas-clz01tz3v00jb0143texofqlx.html', 'Diário Gaúcho (RBS)')} cobre a estreia em telenovela. O ponto sensível costuma ser humor com jogos/apostas em títulos de sketches — ver eixo Concorrência.</p>",
    "pedro-ottoni": f"{P}Criador de humor com foco em streaming e cultura pop; o {L('https://www.uol.com.br/splash/noticias/2024/09/27/pedro-ottoni.htm', 'Splash (UOL)')} apresenta trajetória e a {L('https://f5.folha.uol.com.br/celebridades/2024/06/conheca-pedro-ottoni-que-faz-videos-sobre-vida-na-favela-e-usou-humor-para-chegar-a-tv.shtml', 'Folha — F5')}, parceria com streaming. Pauta leve; confirmar alinhamento de marca e faixa etária do conteúdo com a peça.</p>",
    "ademara": f"{P}Humorista com série <strong class=\"font-semibold text-slate-900\">Sem Filtro</strong> na Netflix; a {L('https://www.uol.com.br/splash/noticias/2023/03/01/ademara-vive-influencer-em-serie-da-netflix-nao-podia-ser-mais-diferente.htm', 'Splash (UOL)')} cobre o papel e a {L('https://pt.wikipedia.org/wiki/Sem_Filtro_(s%C3%A9rie)', 'Wikipédia da série')} resume enredo e elenco. Checar menções políticas recentes na imprensa ao montar o cronograma.</p>",
}

INNER_22_27: dict[str, str] = {
    "linnyke-alves": f"{P}Comediante de vídeo curto com personagens de rua e engajamento forte no TikTok e no Instagram; mobilização solidária repercutiu no {L('https://www.jornaldorap.com.br/noticias/linnyke-alves-mobiliza-redes-sociais-e-arrecada-mais-de-r-400-mil-para-realizar-o-sonho-da-casa-propria-de-crianca-carente/', 'Jornal do Rap')} e na {L('https://www.polemicaparaiba.com.br/cidades/em-joao-pessoa-humorista-cria-vaquinha-para-ajudar-crianca-que-encantou-a-internet-assista/', 'Polêmica Paraíba')}. Cuidado se a narrativa envolver menor em situação de vulnerabilidade.</p>",
    "felipe-hatori": f"{P}Comediante e roteirista representado pela Baobá; a {L('https://www.baobashows.com.br/felipehatori', 'página na Baobá Produções')} lista formatos e o {L('https://www.diariodesuzano.com.br/caderno-d/humorista-suzanense-inicia-carreira-no-stand-up-e-cria-grupo-bateu-a-nave-44211/', 'Diário de Suzano')} contextualiza grupos de humor no interior paulista. Audiência concentrada em TikTok, Instagram e YouTube — validar campanhas em Métricas nas redes.</p>",
    "julimara": f"{P}Criadora ligada ao Triângulo Mineiro (MG), com turismo e lifestyle regional; o {L('https://linktr.ee/Julimaranascimento', 'Linktree público')} concentra handles e a {L('https://www.flikta.com/influencers/uberlandia/', 'listagem Flikta (Uberlândia)')} descreve nicho e alcance. Confirmar status comercial no briefing.</p>",
    "raquel-real": f"{P}Comediante e roteirista; perfil agregado no {L('https://www.fashionbubbles.com/influencers/quem-e-raquel-real/', 'Fashion Bubbles')} e tom de humor na {L('https://www.metropoles.com/entretenimento/diaba-do-tiktok-raquel-real-usa-humor-para-criticar-bizarrices-da-web', 'Metrópoles')}. No X há sátira em torno de apostas e política; buscas por nome no estado misturam figura política homônima — homologar por handle e URL do perfil.</p>",
    "morgana-camila": f"{P}Criadora cearense do bordão <strong class=\"font-semibold text-slate-900\">Arrasa na Major</strong>, conhecida pelos desfiles cívicos; história no {L('https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html', 'O Povo')} e no {L('https://diariodonordeste.verdesmares.com.br/entretenimento/zoeira/arrasa-na-major-morgana-camila-viraliza-desfile-civico-de-maranguape-com-humor-e-originalidade-1.3275714/leia-tamb%C3%A9m-1.3275734', 'Diário do Nordeste')} cruzam viralização e produto. Pauta mistura humor, maternidade e cotidiano; menores em conteúdo de massa entra no eixo Loterias 18+.</p>",
    "paulo-victor-freitas": f"{P}Criador potiguar de humor sobre o Nordeste; o {L('https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml', 'G1 (RN)')} documenta viralização regional e a {L('https://www.nessmgt.com/casting/seu-freitaz', 'Ness — casting')} reúne dados públicos de agência. Parkour e rap na bio; homologar identidade por handle e por fontes citadas no perfil.</p>",
}

INNER_ALL = {**INNER_1_21, **INNER_22_27}

REDE_FOOTER_P = re.compile(
    r"<p class='mt-1\.5 text-\[9px\] text-slate-500(?: leading-snug)?'[^>]*>[\s\S]*?</p>"
)

REDE_STRIP_SPECS: tuple[tuple[str, str], ...] = (
    ("raquel-real", "<section id='morgana-camila'"),
    ("morgana-camila", "<section id='paulo-victor-freitas'"),
    ("paulo-victor-freitas", '<section id="tabela"'),
)


def strip_redes_footers_lote3(html: str) -> tuple[str, int]:
    """Remove rodapés verbosos dos cards do bloco Redes (snapshot) nos perfis 25–27."""
    total = 0
    for start_slug, end_needle in REDE_STRIP_SPECS:
        a = html.find(f"<section id='{start_slug}'")
        if a == -1:
            continue
        b = html.find(end_needle, a + 1)
        if b == -1:
            continue
        sec = html[a:b]
        mb = sec.find("<div class='mb-4'>")
        intro = sec.find(DIV_MARKER, mb)
        if mb == -1 or intro == -1:
            continue
        redes = sec[mb:intro]
        redes2, n = REDE_FOOTER_P.subn("", redes)
        total += n
        if redes2 != redes:
            sec2 = sec[:mb] + redes2 + sec[intro:]
            html = html[:a] + sec2 + html[b:]
    return html, total


def apply(html: str) -> tuple[str, int, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]
    n = 0
    for slug, inner in INNER_ALL.items():
        pat = re.compile(
            rf"(<section id='{re.escape(slug)}'[\s\S]*?{re.escape(DIV_MARKER)})([\s\S]*?)({re.escape(GRID)})",
        )

        def repl(_m: re.Match[str], inner=inner) -> str:
            return _m.group(1) + inner + _m.group(3)

        chunk2, c = pat.subn(repl, chunk, count=1)
        if c:
            n += c
            chunk = chunk2
    merged = head + chunk + tail
    merged2, n_strip = strip_redes_footers_lote3(merged)
    return merged2, n, n_strip


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DEFAULT
    html = path.read_text(encoding="utf-8")
    html2, n, n_strip = apply(html)
    if n != len(INNER_ALL):
        print(f"Aviso: {n} de {len(INNER_ALL)} intros substituídos.", file=sys.stderr)
    if html2 == html:
        print("Nada alterado.")
        return 0
    path.write_text(html2, encoding="utf-8")
    print(f"OK: {n} intros; {n_strip} rodapés removidos do snapshot Redes (lote 3) em {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
