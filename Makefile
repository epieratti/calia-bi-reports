# Toolbox dossiês — na raiz do repositório
.PHONY: help \
	validate-dossier-squad-13 validate-dossier-squad-8 validate-dossier-squad-20260504 \
	validate-dossier-febraban validate-dossier-squad-13-strict \
	check-links-squad-13 check-links-squad-8 check-links-squad-20260504 check-links-febraban \
	build-dossier-squad-13 build-dossier-squad-8 build-dossier-squad-20260504 build-dossier-febraban \
	build-dossier-consolidado-20260511 merge-dossier-consolidado-20260511 \
	validate-dossier-minimo build-dossier-minimo-preview \
	qa-dossier-squad-13 qa-dossier-squad-8 qa-dossier-squad-20260504 qa-dossier-febraban \
	check-html-leakage check-dossier-publish-sync \
	validate-dossier-13 validate-dossier-8 validate-dossier-strict-13 \
	check-links-13 check-links-8 \
	build-loterias-13 build-loterias-8 \
	dossie-filename dossie-entregar dossie-pdf

PYTHON ?= python3
ROOT := $(abspath .)
BUILD := $(PYTHON) loterias2026/scripts/build_dossier_completo.py

help:
	@echo "Alvos úteis:"
	@echo "  make dossie-filename MD=<dossier.md> [DATE=YYYYMMDD] [SUFFIX=...] — imprime YYYYMMDD-dossie-<slug>.html"
	@echo "  make dossie-entregar MD=<dossier.md> DEST=<pasta|arquivo.html> [VARIANT=...] [DATE=...] [SUFFIX=...] [SKIP_LINKS=1]"
	@echo "       — valida + links + build + cópia em DEST + vazamento na pasta cliente"
	@echo "  make dossie-pdf HTML=<caixa/....html> OUT=<saida.pdf> — PDF (Playwright; DOSSIER_PDF_PASSWORD ou SKIP_GATE=1 interno; opcional POST_UNLOCK_WAIT=5 para Chart.js; PDF_LANDSCAPE=1; PDF_MARGIN_TIGHT=1)"
	@echo "  make validate-dossier-squad-13   — valida loterias2026/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-squad-8   — valida loterias2026/lotes/20260406/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-squad-20260504 — valida lote 04/05/2026"
	@echo "  make validate-dossier-febraban  — valida dossier_febraban_concorrencia_2026.md"
	@echo "  make validate-dossier-minimo    — valida examples/minimo/dossier_minimo_exemplo.md"
	@echo "  make build-dossier-minimo-preview — gera examples/minimo/output-preview.html (gitignored)"
	@echo "  make qa-dossier-squad-13        — validate + links + build 13 + check vazamento HTML"
	@echo "  make qa-dossier-squad-8         — idem para lote 8"
	@echo "  make qa-dossier-squad-20260504  — idem para lote 04/05/2026"
	@echo "  make qa-dossier-febraban        — validate + links + build + sync publicado"
	@echo "  make check-dossier-publish-sync — rebuild lotes modo B e compara com caixa/febraban"
	@echo "  make check-html-leakage         — vazamento em caixa/, embratur/, febraban/, outputs modo B"
	@echo "  Dicas semânticas: python3 tools/validate_dossier_source.py --hints <dossier.md>"
	@echo "  make check-links-squad-13        — HTTP check dos links no .md (13)"
	@echo "  make build-dossier-squad-13     — gera HTML squad 13 em loterias2026/output/"
	@echo "  make build-dossier-squad-8      — gera HTML squad 8 em loterias2026/lotes/20260406/output/"
	@echo "  make build-dossier-squad-20260504 — gera HTML lote 04/05 em loterias2026/lotes/20260504/output/"
	@echo "  make merge-dossier-consolidado-20260511 — merge .md dos 4 lotes → loterias2026/lotes/20260511/data/"
	@echo "  make build-dossier-consolidado-20260511 — HTML consolidado 27 perfis → output/ + caixa/"
	@echo "  make build-dossier-febraban     — gera HTML Febraban em loterias2026/output/"
	@echo "(Aliases legados: validate-dossier-13, build-loterias-13, …)"

validate-dossier-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/data/dossier_loterias2026.md

validate-dossier-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/lotes/20260406/data/dossier_loterias2026.md

validate-dossier-squad-20260504:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/lotes/20260504/data/dossier_loterias2026.md

validate-dossier-febraban:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/data/dossier_febraban_concorrencia_2026.md

validate-dossier-squad-13-strict:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py --strict loterias2026/data/dossier_loterias2026.md

check-links-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/data/dossier_loterias2026.md

check-links-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/lotes/20260406/data/dossier_loterias2026.md

check-links-squad-20260504:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/lotes/20260504/data/dossier_loterias2026.md

check-links-febraban:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/data/dossier_febraban_concorrencia_2026.md

build-dossier-squad-13:
	cd "$(ROOT)" && $(BUILD) --project-root loterias2026

build-dossier-squad-8:
	cd "$(ROOT)" && $(BUILD) --project-root loterias2026/lotes/20260406

build-dossier-squad-20260504:
	cd "$(ROOT)" && $(BUILD) --project-root loterias2026/lotes/20260504

build-dossier-febraban:
	cd "$(ROOT)" && $(BUILD) --project-root loterias2026 \
		--md loterias2026/data/dossier_febraban_concorrencia_2026.md \
		--panels loterias2026/data/dossier_febraban_concorrencia_2026_panels.yaml \
		--out loterias2026/output/20260427-dossie-febraban-concorrencia-creators-2026.html \
		--variant squad_8

validate-dossier-minimo:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py examples/minimo/dossier_minimo_exemplo.md

build-dossier-minimo-preview:
	cd "$(ROOT)" && $(BUILD) \
		--md examples/minimo/dossier_minimo_exemplo.md \
		--panels examples/minimo/dossier_minimo_exemplo_panels.yaml \
		--out examples/minimo/output-preview.html \
		--variant squad_8 --no-gate

check-html-leakage:
	cd "$(ROOT)" && $(PYTHON) tools/check_client_html_leakage.py caixa embratur febraban loterias2026/output loterias2026/lotes/20260406/output loterias2026/lotes/20260504/output loterias2026/lotes/20260511/output

merge-dossier-consolidado-20260511:
	cd "$(ROOT)" && $(PYTHON) tools/merge_loterias_consolidated_dossier.py

build-dossier-consolidado-20260511: merge-dossier-consolidado-20260511
	cd "$(ROOT)" && $(PYTHON) loterias2026/lotes/20260511/scripts/build_consolidated.py

check-dossier-publish-sync:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_publish_sync.py --build

qa-dossier-squad-13: validate-dossier-squad-13 check-links-squad-13 build-dossier-squad-13 check-html-leakage

qa-dossier-squad-8: validate-dossier-squad-8 check-links-squad-8 build-dossier-squad-8 check-html-leakage

qa-dossier-squad-20260504: validate-dossier-squad-20260504 build-dossier-squad-20260504 check-html-leakage

qa-dossier-febraban: validate-dossier-febraban check-links-febraban build-dossier-febraban check-dossier-publish-sync

# Aliases (nomes antigos; mantidos para scripts e hábitos locais)
validate-dossier-13: validate-dossier-squad-13
validate-dossier-8: validate-dossier-squad-8
validate-dossier-strict-13: validate-dossier-squad-13-strict
check-links-13: check-links-squad-13
check-links-8: check-links-squad-8
build-loterias-13: build-dossier-squad-13
build-loterias-8: build-dossier-squad-8

# Pipeline completo até pasta Pages (ver tools/dossier_publish.py).
# Ex.: make dossie-entregar MD=loterias2026/data/dossier_loterias2026.md DEST=caixa/loterias
dossie-filename:
	@test -n "$(MD)" || (echo "Defina MD= caminho/dossier_*.md"; exit 1)
	cd "$(ROOT)" && $(PYTHON) tools/dossier_html_filename.py --md "$(MD)" \
		$(if $(DATE),--date $(DATE),) \
		$(if $(SUFFIX),--suffix "$(SUFFIX)",)

dossie-entregar:
	@test -n "$(MD)" || (echo "Defina MD= e DEST= — ex.: make dossie-entregar MD=.../dossier_x.md DEST=caixa/loterias"; exit 1)
	@test -n "$(DEST)" || (echo "Defina MD= e DEST= — ex.: make dossie-entregar MD=.../dossier_x.md DEST=caixa/loterias"; exit 1)
	cd "$(ROOT)" && $(PYTHON) tools/dossier_publish.py --md "$(MD)" --dest "$(DEST)" \
		$(if $(VARIANT),--variant $(VARIANT),) \
		$(if $(DATE),--date $(DATE),) \
		$(if $(SUFFIX),--suffix "$(SUFFIX)",) \
		$(if $(SKIP_LINKS),--skip-links,)

dossie-pdf:
	@test -n "$(HTML)" || (echo "Defina HTML= caminho/arquivo.html e OUT= arquivo.pdf"; exit 1)
	@test -n "$(OUT)" || (echo "Defina OUT= arquivo.pdf"; exit 1)
	@if [ "$(SKIP_GATE)" != "1" ] && [ -z "$$DOSSIER_PDF_PASSWORD" ]; then echo "Exporte DOSSIER_PDF_PASSWORD=... (senha do gate) ou use SKIP_GATE=1 (uso interno)"; exit 1; fi
	cd "$(ROOT)" && $(PYTHON) tools/dossier_export_pdf.py --html "$(HTML)" --out "$(OUT)" \
		$(if $(SKIP_GATE),--skip-gate,) \
		$(if $(POST_UNLOCK_WAIT),--post-unlock-wait $(POST_UNLOCK_WAIT),) \
		$(if $(PDF_LANDSCAPE),--landscape,) \
		$(if $(PDF_MARGIN_TIGHT),--margin-tight,)
