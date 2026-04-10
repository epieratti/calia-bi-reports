# Toolbox dossiês — na raiz do repositório
.PHONY: help \
	validate-dossier-squad-13 validate-dossier-squad-8 validate-dossier-squad-13-strict \
	check-links-squad-13 check-links-squad-8 \
	build-dossier-squad-13 build-dossier-squad-8 \
	validate-dossier-minimo build-dossier-minimo-preview \
	qa-dossier-squad-13 qa-dossier-squad-8 check-html-leakage \
	validate-dossier-13 validate-dossier-8 validate-dossier-strict-13 \
	check-links-13 check-links-8 \
	build-loterias-13 build-loterias-8 \
	dossie-filename dossie-entregar dossie-pdf

PYTHON ?= python3
ROOT := $(abspath .)

help:
	@echo "Alvos úteis:"
	@echo "  make dossie-filename MD=<dossier.md> [DATE=YYYYMMDD] [SUFFIX=...] — imprime YYYYMMDD-dossie-<slug>.html"
	@echo "  make dossie-entregar MD=<dossier.md> DEST=<pasta|arquivo.html> [VARIANT=...] [DATE=...] [SUFFIX=...] [SKIP_LINKS=1]"
	@echo "       — valida + links + build + cópia em DEST + vazamento na pasta cliente"
	@echo "  make dossie-pdf HTML=<caixa/....html> OUT=<saida.pdf> — PDF após gate (precisa Playwright + chromium; senha em DOSSIER_PDF_PASSWORD)"
	@echo "  make validate-dossier-squad-13   — valida loterias2026/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-squad-8   — valida loterias2026-20260406/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-minimo    — valida examples/minimo/dossier_minimo_exemplo.md"
	@echo "  make build-dossier-minimo-preview — gera examples/minimo/output-preview.html (gitignored)"
	@echo "  make qa-dossier-squad-13        — validate + links + build 13 + check vazamento HTML"
	@echo "  make qa-dossier-squad-8         — idem para lote 8"
	@echo "  make check-html-leakage         — vazamento em caixa/, embratur/, outputs modo B"
	@echo "  Dicas semânticas: python3 tools/validate_dossier_source.py --hints <dossier.md>"
	@echo "  make check-links-squad-13        — HTTP check dos links no .md (13)"
	@echo "  make build-dossier-squad-13     — gera HTML squad 13 em loterias2026/output/"
	@echo "  make build-dossier-squad-8      — gera HTML squad 8 em loterias2026-20260406/output/"
	@echo "(Aliases legados: validate-dossier-13, build-loterias-13, …)"

validate-dossier-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/data/dossier_loterias2026.md

validate-dossier-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026-20260406/data/dossier_loterias2026.md

validate-dossier-squad-13-strict:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py --strict loterias2026/data/dossier_loterias2026.md

check-links-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/data/dossier_loterias2026.md

check-links-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026-20260406/data/dossier_loterias2026.md

build-dossier-squad-13:
	cd "$(ROOT)/loterias2026" && $(PYTHON) scripts/build_dossier_completo.py

build-dossier-squad-8:
	cd "$(ROOT)/loterias2026-20260406" && $(PYTHON) scripts/build_dossier_completo.py

validate-dossier-minimo:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py examples/minimo/dossier_minimo_exemplo.md

build-dossier-minimo-preview:
	cd "$(ROOT)/loterias2026" && $(PYTHON) scripts/build_dossier_completo.py \
		--md ../examples/minimo/dossier_minimo_exemplo.md \
		--panels ../examples/minimo/dossier_minimo_exemplo_panels.yaml \
		--out ../examples/minimo/output-preview.html \
		--variant squad_8 --no-gate

check-html-leakage:
	cd "$(ROOT)" && $(PYTHON) tools/check_client_html_leakage.py caixa embratur loterias2026/output loterias2026-20260406/output

qa-dossier-squad-13: validate-dossier-squad-13 check-links-squad-13 build-dossier-squad-13 check-html-leakage

qa-dossier-squad-8: validate-dossier-squad-8 check-links-squad-8 build-dossier-squad-8 check-html-leakage

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
	@test -n "$$DOSSIER_PDF_PASSWORD" || (echo "Exporte DOSSIER_PDF_PASSWORD=... (senha do gate) antes do make"; exit 1)
	cd "$(ROOT)" && $(PYTHON) tools/dossier_export_pdf.py --html "$(HTML)" --out "$(OUT)"
